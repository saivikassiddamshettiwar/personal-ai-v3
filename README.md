# 🤖 Personal AI V3

Personal AI V3 is an AI-powered chatbot built with **Python**, **Streamlit**, and **Ollama**. It provides a clean and interactive chat interface where users can communicate with locally running Large Language Models (LLMs) such as **Llama 3.2** without requiring any paid API keys.

---

## 🚀 Features

* 💬 Interactive chat interface
* 🧠 Local AI inference using Ollama
* ⚡ Fast response streaming
* 🎨 User-friendly Streamlit UI
* 🔒 Privacy-focused (runs locally)
* 🖥️ Simple and lightweight setup
* 🔄 Chat history support
* 🆓 No OpenAI API key required

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **Streamlit**
* **Ollama**
* **Llama 3.2**
* **Git & GitHub**

---

## 📂 Project Structure

```text
personal-ai-v3/
│── app.py                 # Streamlit application
│── chatbot.py             # AI response generation
│── requirements.txt       # Python dependencies
│── README.md              # Project documentation
│── assets/                # Images (optional)
└── venv/                  # Virtual environment (not uploaded)
```

---

## 📥 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/saivikassiddamshettiwar/personal-ai-v3.git
```

```bash
cd personal-ai-v3
```

---

### 2. Create a Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install Ollama

Download and install Ollama from:

https://ollama.com

---

### 5. Download the Llama Model

```bash
ollama pull llama3.2:3b
```

---

### 6. Start Ollama

```bash
ollama serve
```

---

### 7. Run the Application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

## 💻 Usage

1. Launch the Streamlit application.
2. Select the desired AI model.
3. Enter your prompt in the chat box.
4. Receive AI-generated responses in real time.

---

## 📸 Screenshot

<img width="1920" height="931" alt="image" src="https://github.com/user-attachments/assets/6ee2ded0-3e6a-4fbc-a004-3025ce2ff88a" />




```
assets/screenshot.png
```

Example:

```markdown
![Personal AI V3](assets/screenshot.png)
```

---

## 📋 Requirements

* Python 3.10 or higher
* Ollama
* Streamlit
* Internet connection (only for downloading the model the first time)

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature-name
```

3. Commit your changes.

```bash
git commit -m "Added new feature"
```

4. Push your branch.

```bash
git push origin feature-name
```

5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Saivikas Siddamshettiwar**

GitHub: https://github.com/saivikassiddamshettiwar

---

## ⭐ Support

If you found this project helpful, please consider giving it a ⭐ on GitHub.
