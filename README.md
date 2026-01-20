# URL & YouTube Content Summarizer 🦜📄

This project is a **LangChain-powered summarization application** built with **Streamlit** and **Groq LLMs**.  
It allows users to generate **clear, structured summaries** from **YouTube videos or web articles** by simply providing a URL.

The system intelligently selects the best loading and summarization strategy to handle both **short and long-form content** reliably.

---

## 🎯 Objective

The goal of this project is to:
- Summarize long web pages and YouTube transcripts efficiently
- Demonstrate **LLM-based document summarization pipelines**
- Handle real-world issues like loader failures and content variability
- Build a user-friendly AI summarization tool using LangChain

---

## 🚀 Key Features

### 🔗 URL-Based Summarization
- Supports **YouTube URLs** (video transcripts)
- Supports **websites / blog articles**
- Automatic URL validation

---

### 🧠 Intelligent Content Loading
- Uses multiple loaders with fallback:
  - `YoutubeLoader` for video transcripts
  - `UnstructuredURLLoader`
  - `WebBaseLoader`
- Ensures minimum meaningful content before summarization

---

### 🤖 LLM-Powered Summaries
- Powered by **Groq-hosted LLaMA 3.1 (8B Instant)**
- Low temperature for factual, concise output
- Structured summaries using bullet points

---

### 📄 Adaptive Summarization Strategy
- **Stuff chain** for short documents
- **Map-Reduce chain** for long or multi-document content
- Automatic chain selection based on content size

---

### 🖥️ Interactive Streamlit UI
- Clean input-based interface
- Sidebar-based Groq API key input
- Loading spinners and clear error messages
- Summary display with content statistics

---

## 🧠 How It Works

1. User enters a YouTube or website URL
2. URL is validated
3. Content is loaded using the most suitable loader
4. Total content length is analyzed
5. A summarization chain is selected:
   - Stuff (short content)
   - Map-Reduce (long content)
6. The LLM generates a **concise, structured summary**
7. Summary and content stats are displayed

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **LangChain**
- **Groq (LLaMA 3.1)**
- **validators**
- **Unstructured**
- **YouTube Transcript Loader**

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository
```bash
git clone <your-repo-url>
cd <repo-folder>


## 📂 Project Structure

