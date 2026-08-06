import streamlit as st
from datetime import datetime, date, timedelta
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
    delete_all_conversations,
    update_conversation_title,
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

# ---------- Modern UI Theme ----------
st.markdown(
""" <style>
.stApp {
background: linear-gradient(180deg, #0b0f17 0%, #0a0d14 100%);
color: #e5e7eb;
}

section[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #1f2937;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1100px;
}

h1, h2, h3 {
    color: #f9fafb;
    letter-spacing: -0.02em;
}

.chat-user {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    padding: 14px 18px;
    border-radius: 18px;
    margin: 10px 0;
    max-width: 82%;
    margin-left: auto;
    box-shadow: 0 8px 24px rgba(37,99,235,0.18);
}

.chat-ai {
    background: #111827;
    color: #f9fafb;
    padding: 14px 18px;
    border-radius: 18px;
    margin: 10px 0;
    max-width: 82%;
    border: 1px solid #374151;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}

.bottom-bar {
    position: sticky;
    bottom: 0;
    background: rgba(11, 15, 23, 0.92);
    backdrop-filter: blur(12px);
    border-top: 1px solid #1f2937;
    padding: 10px 0 8px 0;
    z-index: 999;
}

.stChatInputContainer {
    border-radius: 18px !important;
    border: 1px solid #374151 !important;
    background: #111827 !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.28);
}

.stButton button {
    border-radius: 14px !important;
    background: #111827 !important;
    color: #f9fafb !important;
    border: 1px solid #374151 !important;
    transition: all 0.2s ease;
}

.stButton button:hover {
    background: #1f2937 !important;
    border-color: #4b5563 !important;
    transform: translateY(-1px);
}

div[data-testid="stFileUploader"] {
    background: #111827;
    border: 1px solid #374151;
    border-radius: 16px;
    padding: 12px;
}

.stSelectbox > div > div {
    background: #111827;
    border: 1px solid #374151;
    border-radius: 12px;
}

.stTextInput > div > div > input {
    background: #111827;
    color: #f9fafb;
    border-radius: 12px;
}
</style>
""",
    unsafe_allow_html=True,
)


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


def generate_chat_title(user_prompt, assistant_reply):
    title_prompt = (
        "Generate a short conversation title (3-5 words) based on this chat. "
        "Return ONLY the title and nothing else.\n\n"
        f"User: {user_prompt}\n"
        f"Assistant: {assistant_reply}"
    )

    title = ""

    for chunk in stream_chat(
        [{"role": "user", "content": title_prompt}],
        st.session_state.selected_model,
        st.session_state.provider,
    ):
        title += chunk

    return title.strip().replace("\n", " ")[:40]


def format_conversation_group(created_at):
    try:
        created_dt = datetime.fromisoformat(created_at)
    except Exception:
        try:
            created_dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        except Exception:
            return created_at

    created_date = created_dt.date()
    today = date.today()
    if created_date == today:
        return "Today"
    if created_date == today - timedelta(days=1):
        return "Yesterday"
    return created_dt.strftime("%b %d, %Y")


def group_conversations_by_date(conversations):
    groups = {}
    order = []
    for conversation_id, title, created_at in conversations:
        group_label = format_conversation_group(created_at)
        if group_label not in groups:
            groups[group_label] = []
            order.append(group_label)
        groups[group_label].append((conversation_id, title, created_at))
    return [(label, groups[label]) for label in order]


def render_chat_history():
    if st.session_state.messages:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    else:
        st.markdown(
            """
            <div style="text-align:center;padding:90px 20px 40px 20px;">
                <div style="font-size:44px;font-weight:700;color:#f9fafb;">
                    Personal AI
                </div>
                <div style="color:#9ca3af;font-size:18px;margin-top:12px;">
                </div>
                <div style="color:#6b7280;font-size:15px;margin-top:22px;">
                    Ask questions, analyze images, chat with PDFs, search the web, or write code.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


conversations = get_conversations()

answer = None

with st.sidebar:
    st.markdown(
        """
    <div style="padding:8px 0 16px 0;">
        <div style="font-size:24px;font-weight:700;color:#f9fafb;">
            Personal AI
        </div>
        <div style="color:#9ca3af;font-size:13px;margin-top:4px;">
            Local AI assistant • Ollama
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("### Chats")

    if st.button("+ New chat", use_container_width=True):
        load_conversation(None, "New Chat")
        st.session_state.uploaded_docs = []
        st.session_state.document_texts = {}
        st.session_state.show_uploader = False
        st.rerun()

    st.markdown("---")

    for conversation_id, title, created_at in conversations:

        left, right = st.columns([6, 1])

        with left:
            if st.button(
                f"💬 {title}",
                key=f"open_{conversation_id}",
                use_container_width=True,
            ):
                load_conversation(conversation_id, title)
                st.rerun()

        with right:
            if st.button(
                "🗑️",
                key=f"delete_{conversation_id}",
                use_container_width=True,
            ):
                delete_conversation(conversation_id)

                if st.session_state.conversation_id == conversation_id:
                    load_conversation(None, "New Chat")
                    st.session_state.uploaded_docs = []
                    st.session_state.document_texts = {}

                st.rerun()

    st.markdown("---")

    if st.button("🗑️ Clear all conversations", use_container_width=True):
        delete_all_conversations()

        load_conversation(None, "New Chat")
        st.session_state.uploaded_docs = []
        st.session_state.document_texts = {}
        st.session_state.show_uploader = False

        st.rerun()

    st.markdown("---")
    st.markdown(
        f"""
    <div style="background:#111827;border:1px solid #374151;
                border-radius:16px;padding:14px 16px;">
        <div style="color:#9ca3af;font-size:12px;">Current chat</div>
        <div style="color:#f9fafb;font-weight:600;margin-top:6px;">
            {st.session_state.conversation_title}
        </div>
        <div style="color:#9ca3af;font-size:12px;margin-top:6px;">
            {len(st.session_state.messages)} messages
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    with st.expander("Settings", expanded=False):
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

if answer is not None:
    st.write(answer)

render_chat_history()

st.markdown('<div class="bottom-bar">', unsafe_allow_html=True)

left, middle, right = st.columns([1, 8, 1])

with left:
    if st.button("➕", use_container_width=True):
        st.session_state.show_uploader = not st.session_state.show_uploader

with middle:
    if st.session_state.get("uploaded_docs"):
        chips = "".join(
            f"""
            <span style="
                display:inline-flex;
                align-items:center;
                gap:6px;
                background:#111827;
                color:#f9fafb;
                padding:8px 14px;
                border-radius:18px;
                border:1px solid #374151;
                margin-right:8px;
                margin-bottom:8px;
                font-size:13px;
            ">
                📎 {name}
            </span>
            """
            for name in st.session_state.uploaded_docs
        )
        st.markdown(chips, unsafe_allow_html=True)

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

    with st.container(border=True):
        st.caption("Attach files")

        uploaded_files = st.file_uploader(
            "",
            type=[
                "pdf", "docx", "txt",
                "csv", "xlsx", "xls",
                "json", "xml",
                "png", "jpg", "jpeg", "webp"
            ],
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="attachment_uploader"
        )

        if uploaded_files:
            if "uploaded_docs" not in st.session_state:
                st.session_state.uploaded_docs = []

            if "document_texts" not in st.session_state:
                st.session_state.document_texts = {}

            for uploaded_file in uploaded_files:
                try:
                    text = extract_text(uploaded_file)

                    if text.strip():
                        add_document(text, uploaded_file.name)
                        st.session_state.document_texts[uploaded_file.name] = text

                    if uploaded_file.name not in st.session_state.uploaded_docs:
                        st.session_state.uploaded_docs.append(uploaded_file.name)

                except Exception:
                    pass

        if st.button("Done", use_container_width=True):
            st.session_state.show_uploader = False
            st.rerun()

if prompt:
    memory_text = extract_memory_text(prompt)
    if memory_text:
        save_memory(memory_text)
        ack = "Got it — I'll remember that."
        st.session_state.messages.append({"role": "assistant", "content": ack})
        if st.session_state.conversation_id is None:
            st.session_state.conversation_id = create_conversation("Memory Chat")
            st.session_state.conversation_title = "Memory Chat"
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

        document_results = search_documents(prompt)

        document_context = "\n\n".join(
        (
        f"Source: {result.get('source', 'Unknown document')}\n{result.get('text', '')}"
        if isinstance(result, dict)
        else result
        )
        for result in document_results
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
            {
                "role": "system",
                "content": get_mode_instruction(st.session_state.assistant_mode),
            }
        ]

        if document_context:
            messages_for_ai.append(
                {
                    "role": "system",
                    "content": (
                        "The user has uploaded documents. Use the following document excerpts "
                        "to answer the question. If the answer is found in the documents, answer "
                        "confidently from them.\n\n"
                        + document_context
                    ),
                }
            )

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

        if st.session_state.conversation_title in ["New Chat", prompt[:40]]:
            try:
                new_title = generate_chat_title(prompt, response)
                if new_title:
                    update_conversation_title(
                        st.session_state.conversation_id,
                        new_title
                    )
                    st.session_state.conversation_title = new_title
            except Exception:
                pass

        # speak_text(response)
        st.session_state.voice_input = None