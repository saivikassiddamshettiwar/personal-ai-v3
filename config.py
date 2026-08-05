import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------
# OpenAI
# ------------------------

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
)

# ------------------------
# Gemini
# ------------------------

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
)

# ------------------------
# Claude
# ------------------------

CLAUDE_API_KEY = os.getenv(
    "CLAUDE_API_KEY",
    ""
)