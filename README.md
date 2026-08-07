# Personal AI v3.1

A **local-first multimodal AI assistant** built with **Python, Streamlit, Ollama, Llama 3.2, LLaVA, ChromaDB, SQLite, and OCR**.

Personal AI is designed to provide a **ChatGPT-like experience entirely on your own machine**, with support for document chat, image understanding, voice interaction, web search, personal memory, and premium conversation management — all without relying on cloud AI APIs for its core functionality.

---

## Screenshots

### Main Interface

<img width="1920" height="928" alt="image" src="https://github.com/user-attachments/assets/94698820-a641-4259-98ac-b5942ad5d2ad" />


`assets/home.png`

### Sidebar & Conversation Management

<img width="374" height="933" alt="image" src="https://github.com/user-attachments/assets/95099333-85ce-42cc-97ac-0f779cea1136" />


`assets/sidebar.png`

### Attachment Workflow

<img width="1920" height="975" alt="image" src="https://github.com/user-attachments/assets/60797b1f-abc2-44c1-9319-16ca01a6f371" />

`assets/attachments.png`

### Document Chat (RAG)

Add a screenshot of PDF question answering here.

`assets/rag.png`

### Image Understanding

Add a screenshot of image analysis here.

`assets/image-analysis.png`

---

# Features

## Local AI Chat

* Powered entirely by **Ollama**
* Supports **Llama 3.2**
* Streaming responses with typing effect
* No OpenAI API required for core functionality

## Multiple Assistant Modes

Switch between specialized AI behaviors:

* General Chat
* Coding Assistant
* Debugging
* Explain Code

## Document Chat (RAG)

Chat with uploaded documents using **ChromaDB** retrieval.

### Supported Formats

* PDF
* DOCX
* TXT
* CSV
* XLSX / XLS
* JSON
* XML

### Capabilities

* Automatic document chunking
* Local embedding generation
* Semantic retrieval
* Context-aware question answering

## OCR for Scanned PDFs

Extract text from scanned certificates and image-based documents using:

* **PyMuPDF**
* **Tesseract OCR**

## Image Understanding

Analyze images locally with **LLaVA**.

Ask questions such as:

* What is in this image?
* Describe this screenshot.
* Read the text in this image.
* Explain this diagram.

## Voice Features

* Speech-to-text input
* Text-to-speech output

## Web Search

Optional web search integration that can combine retrieved information with local AI responses.

## Personal Memory

The assistant can remember user-provided information across conversations.

Examples:

* Remember my name
* Remember my college
* Remember my project details

## Premium Conversation Management

* Persistent chat history (SQLite)
* ChatGPT-style conversation sidebar
* **+ New Chat**
* Delete individual conversations
* **Clear all conversations**
* Automatic AI-generated conversation titles

## Modern Premium UI

* Dark theme
* ChatGPT-inspired layout
* Welcome screen when no conversation is active
* Collapsible settings panel
* Compact attachment drawer
* Rounded attachment chips
* Clean branded sidebar
* Improved spacing and typography

---

# Tech Stack

| Component        | Technology          |
| ---------------- | ------------------- |
| Frontend         | Streamlit           |
| LLM              | Ollama + Llama 3.2  |
| Vision Model     | LLaVA               |
| Retrieval        | ChromaDB            |
| Database         | SQLite              |
| OCR              | PyMuPDF + Tesseract |
| Image Processing | Pillow              |
| Data Analysis    | pandas              |
| Word Processing  | python-docx         |

---

# Project Structure

```text
Personal-AI/
│
├── app.py                 # Main Streamlit application
├── chatbot.py             # AI chat and image analysis
├── database.py            # Conversation database
├── memory.py              # Personal memory storage
├── rag.py                 # ChromaDB retrieval system
├── document_loader.py     # Document extraction + OCR
├── web_search.py          # Web search integration
├── voice.py               # Speech input/output
├── models.py              # Provider/model management
├── config.py              # Configuration
├── requirements.txt
├── chat_history.db
├── chroma_db/
└── assets/                # Screenshots for README
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/saivikassiddamshettiwar/personal-ai-v3.git
cd personal-ai-v3
```

## Create a virtual environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\\Scripts\\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Install Ollama

Download Ollama:

https://ollama.com

Pull the required models:

```bash
ollama pull llama3.2:3b
ollama pull llava:latest
ollama pull nomic-embed-text
```

## Run the application

```bash
streamlit run app.py
```

---

# How It Works

## Document Workflow

1. Upload a document.
2. Text is extracted.
3. The document is split into semantic chunks.
4. Chunks are embedded using **nomic-embed-text**.
5. Embeddings are stored in **ChromaDB**.
6. Relevant chunks are retrieved for each query.
7. Llama 3.2 generates a context-aware answer.

## Image Workflow

1. Upload an image.
2. LLaVA processes the image locally.
3. The assistant answers questions about the image.

---

# Current Capabilities

* Local AI chat
* Document question answering
* OCR for scanned certificates
* Image understanding
* Voice interaction
* Web search
* Personal memory
* Chat history
* Premium sidebar UI
* AI-generated conversation titles
* Individual and bulk conversation deletion
* Attachment workflow

---

# Example Use Cases

* Summarize a PDF
* Extract information from certificates
* Analyze screenshots
* Explain code
* Debug Python programs
* Remember personal preferences
* Search the web
* Chat entirely offline

---

# Performance

The application is optimized for **local execution on CPU** and works well on laptops without a dedicated GPU.

For best performance:

* Use `llama3.2:3b`
* Use `nomic-embed-text` for embeddings
* Use `llava:latest` for image understanding

---

# Roadmap

### Planned

* Conversation search
* Export chats to PDF / Markdown
* Integrated image uploads through the chat composer
* Drag-and-drop attachments
* Better RAG ranking
* Mobile-responsive layout
* Optional cloud deployment branch (Gemini)

---

# License

This project is intended for **educational, portfolio, and learning purposes**.

---

# Author

**Saivikas Siddamshettiwar**

Integrated M.Tech in Software Engineering

GitHub: https://github.com/saivikassiddamshettiwar

---

Personal AI v3.1 combines **LLM chat, document retrieval, OCR, image understanding, memory, voice interaction, and a premium AI application interface** into a single **offline-capable local AI assistant**.
