import os
import tempfile
import ollama
import pytesseract
from PIL import Image

from openai import OpenAI
import google.generativeai as genai
import anthropic

from config import (
    OPENAI_API_KEY,
    GEMINI_API_KEY,
    CLAUDE_API_KEY,
)

# ----------------------------
# Configure APIs
# ----------------------------

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

openai_client = None

if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

claude_client = None

if CLAUDE_API_KEY:
    claude_client = anthropic.Anthropic(
        api_key=CLAUDE_API_KEY
    )


# ==========================================
# Chat Response
# ==========================================

def generate_response(messages, model, provider="Ollama"):
    """
    Generate a response using the selected AI provider.
    """

    try:

        # -----------------------------
        # OLLAMA
        # -----------------------------
        if provider == "Ollama":

            stream = ollama.chat(
                model=model,
                messages=messages,
                stream=True
            )

            for chunk in stream:

                content = chunk.get(
                    "message",
                    {}
                ).get(
                    "content",
                    ""
                )

                if content:
                    yield content

        # -----------------------------
        # OPENAI
        # -----------------------------
        elif provider == "OpenAI":

            if openai_client is None:
                yield "❌ OpenAI API key not configured."
                return

            response = openai_client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True
            )

            for chunk in response:

                if (
                    chunk.choices
                    and chunk.choices[0].delta.content
                ):
                    yield chunk.choices[0].delta.content

        # -----------------------------
        # GEMINI
        # -----------------------------
        elif provider == "Gemini":

            if not GEMINI_API_KEY:
                yield "❌ Gemini API key not configured."
                return

            gemini_model = genai.GenerativeModel(model)

            prompt = "\n".join(
                f"{m['role']}: {m['content']}"
                for m in messages
            )

            response = gemini_model.generate_content(prompt)

            yield response.text

        # -----------------------------
        # CLAUDE
        # -----------------------------
        elif provider == "Claude":

            if claude_client is None:
                yield "❌ Claude API key not configured."
                return

            system_text = ""

            chat_messages = []

            for message in messages:

                if message["role"] == "system":
                    system_text += message["content"] + "\n"

                else:
                    chat_messages.append(message)

            response = claude_client.messages.create(
                model=model,
                max_tokens=2048,
                system=system_text,
                messages=chat_messages
            )

            yield response.content[0].text

        else:

            yield "❌ Unknown provider."

    except Exception as e:

        yield f"❌ {e}"
    """
    Streams the AI response from Ollama.
    """

    try:

        stream = ollama.chat(
            model=model,
            messages=messages,
            stream=True
        )

        for chunk in stream:

            if "message" in chunk:

                content = chunk["message"].get("content", "")

                if content:
                    yield content

    except Exception as e:

        yield f"❌ Error: {str(e)}"


# ==========================================
# Image Analysis
# ==========================================

def extract_text_from_image(image_path):
    """
    Extract text from an image using Tesseract OCR.
    """

    try:
        image = Image.open(image_path)

        if image.mode != "RGB":
            image = image.convert("RGB")

        text = pytesseract.image_to_string(image)

        return text.strip()

    except Exception:
        return ""


def analyze_image(image_path, question, model="llava:latest"):

    image = Image.open(image_path)

    if image.mode != "RGB":
        image = image.convert("RGB")

    image.thumbnail((384, 384))

    # OCR text extraction
    ocr_text = extract_text_from_image(image_path)

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
            temp_path = temp.name

        image.save(temp_path, "JPEG", quality=75)

        enhanced_prompt = f"""
The user asked:

{question}

OCR extracted this text from the image:

{ocr_text}

Use BOTH the OCR text and the visual appearance of the image to answer accurately.
If there is a conflict, prefer the OCR text for names, dates, certificate numbers, and course titles.
"""

        response = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": enhanced_prompt,
                    "images": [temp_path],
                }
            ],
        )

        return response["message"]["content"]

    except Exception as e:
        return f"Image Analysis Error:\n\n{e}"

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

# ==========================================
# Assistant Modes
# ==========================================

def get_mode_instruction(mode):

    prompts = {

        "General Chat": """
You are Personal AI.

You are a helpful, intelligent and friendly AI assistant.

Answer clearly.

Use Markdown formatting whenever appropriate.

If the user asks programming questions,
provide complete working examples.
""",

        "Coding Assistant": """
You are an expert software engineer.

Generate clean code.

Use best practices.

Explain the important parts.

Always use Markdown code blocks.

If there are multiple solutions,
recommend the best one.
""",

        "Debugging": """
You are an expert debugger.

Find the bug.

Explain why it occurs.

Then provide corrected code.

Do not change unrelated code.
""",

        "Explain Code": """
You are a programming teacher.

Explain code line-by-line.

Use simple language.

Use examples whenever possible.
"""

    }

    return prompts.get(
        mode,
        prompts["General Chat"]
    )