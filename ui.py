import streamlit as st

def render_header():
    st.markdown(
        """
        <div style="text-align:center; padding:36px 0 18px 0;">
            <h1 class="title-gradient">Personal AI</h1>
            <p class="small-muted">Your private local AI workspace</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar():
    with st.sidebar:
        st.markdown("# 🤖 Personal AI")
        st.caption("Offline local assistant")

        st.divider()

        new_chat = st.button("➕ New Chat", use_container_width=True)
        clear_chat = st.button("🗑️ Clear Conversation", use_container_width=True)

        st.divider()

        assistant_mode = st.selectbox(
            "Assistant Mode",
            [
                "General Chat",
                "Coding Assistant",
                "Debugging",
                "Explain Code",
            ],
        )

        model = st.selectbox(
            "Model",
            [
                "llama3.2:3b",
            ],
        )

        web_search = st.checkbox("Enable Web Search")

        return new_chat, clear_chat, assistant_mode, model, web_search

def render_message(role: str, content: str):
    if role == "user":
        st.markdown(
            f'<div class="chat-user">{content}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="chat-ai">{content}</div>',
            unsafe_allow_html=True,
        )