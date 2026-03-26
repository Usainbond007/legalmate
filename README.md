# ⚖️ LegalEase

**LegalEase** is an AI powered legal assistant that helps users understand Indian Penal Code (IPC) sections in simple natural language based on real-world situations.

It uses a custom **Retrieval-Augmented Generation (RAG)** pipeline to fetch relevant legal sections and explain them using a Large Language Model.

---
# Live Demo :https://legalmate.streamlit.app/

## 🚀 Features

* 🔍 **Smart Query Understanding**
  Enhances user input with legal keywords for better retrieval

* 📚 **Relevant IPC Retrieval**
  Uses FAISS + embeddings to fetch the most relevant IPC sections

* 🤖 **AI-Powered Explanation**
  Converts complex legal text into simple, understandable language

* 🧠 **Structured Output**
  Provides:

  * Explanation
  * Why it applies
  * Example

* 🌐 **Streamlit Web App**
  Clean UI for interactive usage

---

## 🧱 Tech Stack

* **Python**
* **Streamlit**
* **FAISS** (vector search)
* **Sentence Transformers** (embeddings)
* **Google Gemini API** (LLM)

---

## 🧠 How It Works

1. **User Input**
   User describes a situation in natural language

2. **Query Enhancement**
   Keywords related to IPC sections are added

3. **Embedding + Retrieval**

   * Query converted into vector
   * FAISS retrieves top relevant IPC sections

4. **Context Building**
   Relevant sections are formatted into context

5. **LLM Generation**
   Gemini generates a simplified explanation

---

## 📂 Project Structure

```
LegalEase/
│── app.py              # Streamlit frontend
│── rag.py              # RAG pipeline (retrieval + generation)
│── embedcheck.py       # FAISS + embedding loader
│── requirements.txt    # Dependencies
│── .gitignore
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```
git clone https://github.com/your-username/legalease.git
cd legalease
```

---

### 2. Install dependencies

```
pip install -r requirements.txt
```

---

### 3. Add API Key

#### Local (.env)

```
GEMINI_API_KEY=your_api_key
```

#### Streamlit Cloud (Secrets)

```
GEMINI_API_KEY = "your_api_key"
```

---

### 4. Run the app

```
streamlit run app.py
```

---

## ⚠️ Disclaimer

This project is for **educational purposes only** and does not constitute legal advice.
Always consult a qualified legal professional for real-world legal issues.

---

## 🌟 Future Improvements

* Better legal dataset coverage
* Case law integration
* Multi-language support
* Improved UI/UX
* Fine-tuned legal LLM

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📌 Author

Built by Ishan Chowdhury

---

## ⭐ If you found this useful, consider starring the repo!
