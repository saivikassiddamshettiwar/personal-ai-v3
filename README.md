# Personal AI v3.1

A local-first AI assistant built with **Python, Streamlit, Ollama, Llama 3.2, LLaVA, ChromaDB, SQLite, and OCR**.
The project runs entirely on your own machine without requiring OpenAI or other cloud AI APIs for its core functionality.

## Features

### AI Chat

* Local AI chat powered by **Ollama**
* Supports **Llama 3.2**
* Streaming responses with a typing effect
* Multiple assistant modes:

  * General Chat
  * Coding Assistant
  * Debugging
  * Explain Code

### Document Chat (RAG)

* Chat with uploaded documents using **ChromaDB**
* Supports:

  * PDF
  * DOCX
  * TXT
  * CSV
  * XLSX / XLS
  * JSON
  * XML
* Automatic document chunking and embedding generation
* Semantic retrieval for question answering

### OCR Support

* Extracts text from scanned PDFs and image-based documents
* Uses **PyMuPDF** and **Tesseract OCR**

### Image Understanding

* Local image analysis using **LLaVA**
* Ask questions about uploaded images
* No cloud vision API required

### Voice Features

* Voice input (speech-to-text)
* Voice output (text-to-speech)

### Web Search

* Optional web search integration
* Can combine retrieved web information with local AI responses

### Personal Memory

* Store user memories
* Retrieve remembered information across conversations

### Conversation Management

* Persistent chat history stored in **SQLite**
* ChatGPT-style conversation sidebar
* **New Chat**
* **Delete individual conversations**
* **Clear all conversations**
* Automatic conversation title generation

### Premium UI

* Modern dark theme
* ChatGPT-inspired layout
* Collapsible settings panel
* Compact attachment drawer
* Rounded attachment chips
* Clean sidebar branding
* Empty-state welcome screen

## Tech Stack

* **Python**
* **Streamlit**
* **Ollama**
* **Llama 3.2**
* **LLaVA**
* **ChromaDB**
* **SQLite**
* **PyMuPDF**
* **Tesseract OCR**
* **Pillow**
* **pandas**
* **python-docx**

## Project Structure

```
Personal-AI/
│
├── app.py                 # Main Streamlit application
├── chatbot.py             # AI chat and image analysis
├── database.py            # Conversation database
├── memory.py              # Personal memory storage
├── rag.py                 # ChromaDB retrieval system
├── document_loader.py     # Document extraction and OCR
├── web_search.py          # Web search integration
├── voice.py               # Speech input/output
├── models.py              # Provider and model management
├── config.py              # Configuration
├── requirements.txt
└── chroma_db/             # ChromaDB storage
```

## Installation

### Clone the repository

```bash
git clone https://github.com/saivikassiddamshettiwar/personal-ai-v3.git
cd personal-ai-v3
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\\Scripts\\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Install Ollama

Download Ollama from:

https://ollama.com

Pull the required models:

```bash
ollama pull llama3.2:3b
ollama pull llava:latest
ollama pull nomic-embed-text
```

### Run the application

```bash
streamlit run app.py
```

## How It Works

### Document Workflow

1. Upload a PDF, DOCX, TXT, CSV, or other supported document.
2. The text is extracted.
3. The document is split into semantic chunks.
4. Chunks are embedded using **nomic-embed-text**.
5. Embeddings are stored in **ChromaDB**.
6. User questions retrieve the most relevant chunks.
7. Llama 3.2 answers using the retrieved context.

### Image Workflow

1. Upload an image.
2. LLaVA processes the image locally.
3. The assistant answers questions about the image.

## Current Capabilities

* Local AI chat
* Document question answering
* OCR for scanned certificates
* Image understanding
* Voice interaction
* Web search
* Personal memory
* Chat history
* Premium sidebar and UI
* Automatic conversation titles

## Future Improvements

* Conversation search
* Export chats to PDF / Markdown
* Integrated image uploads through the chat composer
* Drag-and-drop attachments
* Faster retrieval and indexing
* Cloud deployment branch using Gemini
* Mobile-responsive layout

## License

This project is intended for educational and portfolio purposes.

## Author

**Saivikas Siddamshettiwar**

Integrated M.Tech in Software Engineering

GitHub: https://github.com/saivikassiddamshettiwar

---

Personal AI v3.1 is designed as a **local-first multimodal AI assistant** that combines LLM chat, document retrieval, OCR, image understanding, memory, voice interaction, and a modern AI application interface into a single offline-capable system.
