# Simple RAG Chatbot

A **domain-specific chatbot** built with **Retrieval-Augmented Generation (RAG)**: it answers questions about traveling to Toronto by first retrieving the most relevant passages from a local knowledge base, then grounding an OpenAI LLM's answer in that context.

Built with Python, LangChain, Streamlit, and Pinecone.

## ✨ Features

- **RAG pipeline** — retrieves relevant document chunks instead of guessing, reducing hallucinations
- **Streamlit chat UI** — clean, interactive chat interface
- **Local embeddings** — sentence-transformers run on your machine (no embedding API costs)
- **Serverless Pinecone vector store** — the index is created and filled automatically on first run
- **Fully configurable** via `.env` — API keys, model, and Pinecone region

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend / RAG | LangChain (LCEL), Python 3.11+ |
| Vector database | Pinecone (serverless) |
| Embeddings | sentence-transformers (`all-mpnet-base-v2`, 768-dim) |
| LLM | OpenAI (`gpt-4o-mini` by default) |

## 📁 Project Structure

```
Simple-RAG-Chatbot/
├── .env.example            # Template for API keys → copy to .env
├── requirements.txt        # Pinned, tested dependencies
├── src/
│   ├── RAG_ChatBot.py      # Chatbot: load, split, embed, store, retrieve, chain
│   ├── streamlitMain.py    # Streamlit user interface
│   └── materials/          # Knowledge base documents
├── report/                 # Project report (PDF)
└── video/                  # Demo video
```

## 🚀 Getting Started

### 1. Prerequisites

- Python **3.11+** (tested on 3.14)
- An [OpenAI](https://platform.openai.com) account
- A [Pinecone](https://www.pinecone.io) account

### 2. Install

```bash
git clone https://github.com/MayankSharma/Simple-RAG-Chatbot.git
cd Simple-RAG-Chatbot

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Set up your API keys

```bash
cp .env.example .env           # Windows: copy .env.example .env
```

Open `.env` and fill in your keys — see [Getting Your API Keys](#-getting-your-api-keys) below.

### 4. Run

```bash
streamlit run src/streamlitMain.py
```

Open **http://localhost:8501** and start chatting about Toronto!

## 🔑 Getting Your API Keys

### OpenAI

1. Go to **https://platform.openai.com/api-keys** and sign in (create an account first if needed).
2. Click **+ Create new secret key**.
3. Give it a name, then click **Create secret key**.
4. **Copy the key immediately** — it is only shown once.
5. Paste it into `.env` as `OPENAI_API_KEY`.
6. OpenAI API is pay-as-you-go — you may need to add a payment method under **Billing** (new accounts usually start with a small free trial credit).

### Pinecone

1. Go to **https://app.pinecone.io** and sign up (a free serverless tier is available).
2. Open the **API Keys** section in the left sidebar.
3. Click **Create API Key** and copy the key.
4. Paste it into `.env` as `PINECONE_API_KEY`.
5. The app creates a serverless index named `langchain-demo` on first run — the free tier is enough for this project.

> 🔒 **Never commit `.env`** — it is already covered by `.gitignore`. The `.env` file only exists on your machine; everyone else uses `.env.example`.

## ⚙️ Configuration

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | ✅ | — | Your OpenAI API key |
| `PINECONE_API_KEY` | ✅ | — | Your Pinecone API key |
| `OPENAI_MODEL` | — | `gpt-4o-mini` | OpenAI chat model to use |
| `PINECONE_CLOUD` | — | `aws` | Pinecone serverless cloud provider |
| `PINECONE_REGION` | — | `us-east-1` | Pinecone serverless region |

## 🧠 How It Works

1. **Ingest** — the knowledge base (`src/materials/torontoTravelAssistant.txt`) is loaded and split into overlapping chunks (~500 characters).
2. **Embed** — each chunk is converted to a 768-dimensional vector by a local sentence-transformers model.
3. **Store** — the vectors are upserted into a serverless Pinecone index (created automatically on first run).
4. **Retrieve** — when you ask a question, it is embedded and the 4 most similar chunks are fetched from Pinecone.
5. **Generate** — the chunks are injected into a prompt as context, and the OpenAI LLM answers grounded in that context.

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| "Failed to start the chatbot" | Both API keys in `.env` must be valid — check you copied `.env.example` to `.env` and filled in real keys |
| Index creation fails | Your Pinecone account may not support `aws/us-east-1` — set `PINECONE_CLOUD` / `PINECONE_REGION` to a cloud/region your account supports (e.g. `gcp` / `us-central1`) |
| Answers look wrong | The knowledge base only covers Toronto travel — rephrase your question, or extend the documents in `src/materials/` |
| First run is slow | The embedding model downloads once (~400 MB) and Pinecone provisions the index |

## 📄 License

[MIT](LICENSE)
