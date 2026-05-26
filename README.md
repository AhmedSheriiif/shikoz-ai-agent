# 🚗 Shikoz AI — Car Sales Agent

A bilingual (Arabic/English) AI-powered car sales agent built with 
Python, FastAPI, and Streamlit. Shikoz answers customer questions, 
provides live inventory data, books test drives, and answers 
dealership policy questions from a PDF knowledge base.

## Features
- 💬 Bilingual conversations — Arabic and English
- 🔧 Tool calling — live inventory, prices, colors from CSV
- 📄 RAG pipeline — answers policy questions from PDF documents
- 📅 Test drive booking — saves, edits, checks requests
- 🌐 REST API — FastAPI with session management
- 🖥️ Chat UI — built with Streamlit

## Tech Stack
- Python, FastAPI, Streamlit
- Groq API (llama-3.3-70b-versatile)
- ChromaDB for vector storage
- PyMuPDF for PDF processing
- LangChain text splitter

## How to Run

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your API key to `.env`: `GROQ_API_KEY=your_key`
4. Ingest the policy PDF: `python ingest.py`
5. Start the API: `uvicorn main:app --reload`
6. Start the UI: `streamlit run ui.py`

## Example Conversation
> "what cars do you have?"
> "what is the price of the Corolla?"
> "ما هي سياسة الضمان؟"
> "I'd like to book a test drive"
