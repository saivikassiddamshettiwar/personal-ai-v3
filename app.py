import streamlit as st
from chatbot import (
    generate_response as stream_chat,
    get_mode_instruction,
    analyze_image,
)
from database import (
    init_database,
    create_conversation,
    save_message,
    get_conversations,
    get_messages,
    delete_conversation,
)
from memory import (
    init_memory_database,
    save_memory,
    get_memories,
)
from voice import listen_to_voice, speak_text
from web_search import search_web

from document_loader import extract_text
from rag import add_document, search_documents

from models import (
    get_available_providers,
    get_models
)

st.set_page_config(page_title="Personal AI v3 Pro", page_icon="🤖", layout="wide")

init_database()
init_memory_database()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "selected_conversation_index" not in st.session_state:
    st.session_state.selected_conversation_index = 0

if "conversation_title" not in st.session_state:
    st.session_state.conversation_title = "Current Chat"

if "show_uploader" not in st.session_state:
    st.session_state.show_uploader = False

if "voice_input" not in st.session_state:
    st.session_state.voice_input = None

if "web_search_enabled" not in st.session_state:
    st.session_state.web_search_enabled = False

if "assistant_mode" not in st.session_state:
    st.session_state.assistant_mode = "General Chat"

if "provider" not in st.session_state:
    st.session_state.provider = "Ollama"

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "llama3.2:3b"    

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "llama3.2:3b"


def load_conversation(conversation_id, title="Current Chat"):
    if conversation_id is None:
        st.session_state.conversation_id = None
        st.session_state.messages = []
        st.session_state.conversation_title = title
        st.session_state.selected_conversation_index = 0
        return

    st.session_state.conversation_id = conversation_id
    st.session_state.conversation_title = title
    st.session_state.messages = [
        {"role": role, "content": content}
        for role, content in get_messages(conversation_id)
    ]


def extract_memory_text(prompt):
    if not prompt:
        return None

    text = prompt.strip()
    lower = text.lower()

    triggers = [
        "remember that",
        "remember this",
        "don't forget that",
        "do not forget that",
    ]

    for trigger in triggers:
        if lower.startswith(trigger):
            memory = text[len(trigger):].strip(" :.-")
            return memory if memory else None

    return None

def render_chat_history():
    st.markdown("### Chat History")
    if st.session_state.messages:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    else:
        st.info("No messages yet. Start a new chat or type a prompt below.")


conversations = get_conversations()
conversation_labels = ["New Chat"] + [f"{title} ({created_at[:10]})" for _, title, created_at in conversations]
conversation_ids = [None] + [conversation_id for conversation_id, _, _ in conversations]
conversation_titles = ["Current Chat"] + [title for _, title, _ in conversations]

with st.sidebar:
    st.title("🤖 Personal AI v3 Pro")

    selected_index = st.selectbox(
        "Saved conversations",
        range(len(conversation_labels)),
        format_func=lambda idx: conversation_labels[idx],
        index=st.session_state.selected_conversation_index,
    )

    st.divider()

    st.subheader("Image Understanding")

    uploaded_image = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg", "webp"],
        key="image_uploader"
    )

    if uploaded_image is not None:
        with open("temp_image.png", "wb") as f:
            f.write(uploaded_image.getbuffer())

        image_question = st.text_input(
            "Ask about the image",
            "What is in this image?"
        )

        if st.button("Analyze Image"):
            with st.spinner("Analyzing image..."):
                answer = analyze_image("temp_image.png", image_question)
            st.write(answer)

    if selected_index != st.session_state.selected_conversation_index:
        st.session_state.selected_conversation_index = selected_index
        selected_id = conversation_ids[selected_index]
        selected_title = conversation_titles[selected_index]
        load_conversation(selected_id, selected_title)

    if st.button("New chat", use_container_width=True):
        load_conversation(None, "New Chat")

    if st.button("Clear conversation", use_container_width=True):
        if st.session_state.conversation_id is not None:
            delete_conversation(st.session_state.conversation_id)
        load_conversation(None, "New Chat")

    st.markdown("---")
    st.subheader("Conversation")
    st.write(f"**{st.session_state.conversation_title}**")
    st.write(f"Messages: {len(st.session_state.messages)}")

    st.markdown("---")
    st.subheader("Settings")
    st.session_state.assistant_mode = st.selectbox(
        "Assistant Mode",
        ["General Chat", "Coding Assistant", "Debugging", "Explain Code"],
        index=["General Chat", "Coding Assistant", "Debugging", "Explain Code"].index(st.session_state.assistant_mode),
    )
    st.session_state.web_search_enabled = st.checkbox(
        "Enable Web Search",
        value=st.session_state.web_search_enabled,
    )
    # AI Provider
    st.session_state.provider = st.selectbox(
        "AI Provider",
        get_available_providers()
    )

    # Models
    available_models = get_models(
        st.session_state.provider
    )

    if st.session_state.selected_model not in available_models:
        st.session_state.selected_model = available_models[0]

    st.session_state.selected_model = st.selectbox(
        "Model",
        available_models
    )

    st.caption(f"Current Provider: {st.session_state.provider}")
    st.caption(f"Current Model: {st.session_state.selected_model}")

render_chat_history()

st.markdown('<div class="bottom-bar">', unsafe_allow_html=True)
left, middle, right = st.columns([1, 8, 1])
with left:
    if st.button("➕", use_container_width=True):
        st.session_state.show_uploader = not st.session_state.show_uploader
with middle:
    prompt = st.chat_input("Message Personal AI v3 Pro")
with right:
    if st.button("🎤", use_container_width=True):
        st.session_state.voice_input = listen_to_voice()
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.voice_input:
    st.success(f"Voice input captured: {st.session_state.voice_input}")
    if not prompt:
        prompt = st.session_state.voice_input

if st.session_state.show_uploader:

    uploaded_files = st.file_uploader(
        "Attach files",
        type=[
            "pdf",
            "docx",
            "txt",
            "csv",
            "xlsx",
            "xls",
            "json",
            "xml",
            "png",
            "jpg",
            "jpeg"
        ],
        accept_multiple_files=True,
    )

    if uploaded_files:

        for uploaded_file in uploaded_files:

            st.success(f"Uploaded: {uploaded_file.name}")

            try:

                text = extract_text(uploaded_file)

                if text.strip():

                    add_document(
                        text,
                        uploaded_file.name
                    )

                    st.success(
                        f"{uploaded_file.name} indexed successfully."
                    )

                else:

                    st.warning(
                        f"No readable text found in {uploaded_file.name}"
                    )

            except Exception as e:

                st.error(
                    f"Error processing {uploaded_file.name}\n\n{e}"
                )

if prompt:
    memory_text = extract_memory_text(prompt)
    if memory_text:
        save_memory(memory_text)
        ack = "Got it — I'll remember that."
        st.session_state.messages.append({"role": "assistant", "content": ack})
        if st.session_state.conversation_id is None:
            st.session_state.conversation_id = create_conversation("Memory Chat")
        save_message(st.session_state.conversation_id, "assistant", ack)
        st.session_state.voice_input = None
    else:
        if st.session_state.conversation_id is None:
            title = prompt[:40] or "New Chat"
            st.session_state.conversation_id = create_conversation(title)
            st.session_state.conversation_title = title

        st.session_state.messages.append({"role": "user", "content": prompt})
        save_message(st.session_state.conversation_id, "user", prompt)

        # Display the user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)

        memory_context = "\n".join(
            f"- {m[1]}" for m in get_memories()
        )

        web_context = ""
        if st.session_state.web_search_enabled:
            results = search_web(prompt, max_results=3)
            if results:
                formatted_results = []
                for item in results:
                    if isinstance(item, dict):
                        title = item.get("title") or item.get("query") or ""
                        body = item.get("body") or item.get("snippet") or item.get("text") or ""
                        url = item.get("link") or item.get("url") or item.get("href") or ""
                        parts = [part for part in [title, body, url] if part]
                        formatted_results.append(" | ".join(parts))
                    else:
                        formatted_results.append(str(item))
                web_context = "\n".join(formatted_results)

        messages_for_ai = [
            {"role": "system", "content": get_mode_instruction(st.session_state.assistant_mode)}
        ]

        if memory_context:
            messages_for_ai.append({"role": "system", "content": "User memories:\n" + memory_context})

        if web_context:
            messages_for_ai.append({"role": "system", "content": "Web search results:\n" + web_context})

        messages_for_ai.extend(st.session_state.messages)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            response = ""

            for chunk in stream_chat(
                messages_for_ai,
                st.session_state.selected_model,
                st.session_state.provider
            ):
                response += chunk

                placeholder.markdown(
                    f"<div class='chat-ai'>{response}▌</div>",
                    unsafe_allow_html=True
                )

            placeholder.markdown(
                f"<div class='chat-ai'>{response}</div>",
                unsafe_allow_html=True
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        save_message(
            st.session_state.conversation_id,
            "assistant",
            response
        )

        speak_text(response)

        st.session_state.voice_input = None