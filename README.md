# 🤖 Simple RAG Chatbot

A domain-specific chatbot built with **Retrieval-Augmented Generation (RAG)**. It answers questions about traveling to Toronto by first retrieving the most relevant passages from a local knowledge base, then grounding an OpenAI LLM's answer in that context.

Built with **Python, LangChain, Streamlit, and Pinecone**.

## ✨ Features

- **RAG Pipeline** — Retrieves relevant document chunks instead of guessing, reducing hallucinations.
- **Streamlit Chat UI** — Clean, interactive chat interface.
- **Local Embeddings** — Sentence-transformers run on your machine (no embedding API costs).
- **Serverless Pinecone Vector Store** — The index is created and populated automatically on first run.
- **Fully Configurable** — API keys, model, and Pinecone region can be configured through `.env`.
- **Context-Aware Responses** — Generates answers based on retrieved knowledge rather than relying entirely on pre-trained information.
- **Docker Support** — Run the application in a container without setting up a local Python environment.

## 🎯 Project Overview

This project demonstrates how Retrieval-Augmented Generation (RAG) can be used to build a domain-specific AI chatbot that provides accurate and context-aware responses.

Instead of relying entirely on an LLM's pre-trained knowledge, the chatbot searches a dedicated knowledge base for relevant information before generating a response. This helps minimize hallucinations and ensures that answers remain relevant to the selected domain.

The project also demonstrates the integration of modern AI development tools, including LangChain for orchestration, Pinecone for vector storage, and Streamlit for building an interactive user interface.

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend / RAG | LangChain (LCEL), Python 3.11+ |
| Vector Database | Pinecone (Serverless) |
| Embeddings | sentence-transformers (all-mpnet-base-v2, 768-dim) |
| LLM | OpenAI (gpt-4o-mini by default) |
| Containerization | Docker & Docker Compose |

## 📁 Project Structure

```text
ChatBot/
├── .env.example            # Template for API keys → copy to .env
├── requirements.txt        # Pinned, tested dependencies
├── Dockerfile              # Recipe for the Docker image
├── .dockerignore           # Files Docker should not send into the image
├── docker-compose.yml      # Makes running the container one command
├── src/
│   ├── RAG_ChatBot.py      # Chatbot: load, split, embed, store, retrieve, chain
│   ├── streamlitMain.py    # Streamlit user interface
│   └── materials/          # Knowledge base documents
└── video/                  # Demo video
```

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.11+ (tested on 3.14)
- An OpenAI account
- A Pinecone account
- Git installed on your machine

### 2. Clone the Repository

```bash
git clone https://github.com/MayankSharma26032006/ChatBot.git
cd ChatBot
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv

# Activate the environment
# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set Up Your API Keys

Create your environment file:

```bash
cp .env.example .env

# Windows
copy .env.example .env
```

Open `.env` and fill in your API keys. Refer to [Getting Your API Keys](#-getting-your-api-keys) below.

### 6. Run the Application

```bash
streamlit run src/streamlitMain.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser and start chatting about Toronto!

## 🐳 Running with Docker

You can also run the application inside a container without setting up a local Python environment. You only need Docker Desktop installed and running.

### 🔒 Environment Variables

Your `.env` file stays on your machine. It is listed in `.dockerignore`, so it is never copied into the image. Docker only passes its values to the running container at startup.

### 1. Make Sure `.env` Exists

```bash
cp .env.example .env

# Windows
copy .env.example .env
```

Fill in your `OPENAI_API_KEY` and `PINECONE_API_KEY` as described above.

### 2. Build and Run

```bash
docker compose up --build
```

The first build installs the Python packages and takes a few minutes; later runs are much faster.

Once the terminal shows the Streamlit URL, open [http://localhost:8501](http://localhost:8501).

### 3. Stop the Application

Press `Ctrl+C` in the terminal running the application, or run:

```bash
docker compose down
```

### What Each Docker File Does

| File | Description |
|---|---|
| `Dockerfile` | Recipe for the image: Python base image, CPU build of PyTorch, dependency installation, source copying, and Streamlit startup on port 8501. |
| `.dockerignore` | Keeps `.env`, `.git`, Python caches, and virtual environments out of the image. |
| `docker-compose.yml` | Builds the image, publishes port 8501, and loads `.env` at runtime. |

### Handy Docker Commands

| Command | Description |
|---|---|
| `docker compose up --build` | Build the image and start the application. |
| `docker compose up` | Start the application again without rebuilding. |
| `docker compose down` | Stop and remove the container. |
| `docker compose logs -f` | Follow the application's logs. |

## 🔑 Getting Your API Keys

### OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys) and sign in (create an account if needed).
2. Click **+ Create new secret key**.
3. Give your key a name and create it.
4. Copy the key immediately — it is only shown once.
5. Paste it into `.env` as `OPENAI_API_KEY`.

**Note:** OpenAI API usage is pay-as-you-go. You may need to add a payment method under Billing. ChatGPT subscriptions and API billing are separate.

### Pinecone API Key

1. Visit [Pinecone](https://app.pinecone.io) and sign up.
2. Open the **API Keys** section in the left sidebar.
3. Click **Create API Key** and copy your key.
4. Paste it into `.env` as `PINECONE_API_KEY`.

The application creates a serverless index named `langchain-demo` on the first run. The free tier is sufficient for this project, subject to account limits.

🔒 **Security Reminder:** Never commit your `.env` file to GitHub. It is already covered by `.gitignore`. The `.env` file only exists on your machine; everyone else should use `.env.example`.

## ⚙️ Configuration

The application uses environment variables for configuration.

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | ✅ | — | Your OpenAI API key |
| `PINECONE_API_KEY` | ✅ | — | Your Pinecone API key |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | OpenAI chat model to use |
| `PINECONE_CLOUD` | No | `aws` | Pinecone serverless cloud provider |
| `PINECONE_REGION` | No | `us-east-1` | Pinecone serverless region |

## 🧠 How It Works

The chatbot follows a five-step Retrieval-Augmented Generation pipeline:

### 1. Ingest

The knowledge base (`src/materials/torontoTravelAssistant.txt`) is loaded and split into overlapping chunks of approximately 500 characters.

### 2. Embed

Each document chunk is converted into a 768-dimensional vector using the local `sentence-transformers` model (`all-mpnet-base-v2`).

### 3. Store

The generated vectors are upserted into a serverless Pinecone index. The index is automatically created if it does not already exist.

### 4. Retrieve

When a user asks a question, the query is converted into an embedding and the four most similar document chunks are retrieved from Pinecone.

### 5. Generate

The retrieved chunks are injected into a prompt as context. The OpenAI LLM uses this information to generate a relevant, context-grounded response.

```text
        User Question
              |
              v
      Query Embedding
              |
              v
       Pinecone Search
              |
              v
   Retrieve Relevant Chunks
              |
              v
    Context + User Question
              |
              v
         OpenAI LLM
              |
              v
      Generated Answer
```

## 💡 Example Use Cases

Users can interact with the chatbot to get information about traveling to Toronto, including:

- Popular tourist attractions and must-visit destinations.
- Transportation options and getting around the city.
- Travel recommendations and sightseeing suggestions.
- General travel-related information available in the knowledge base.
- Contextual answers to follow-up questions.

### Sample Questions

Try asking the chatbot:

- What are the most popular tourist attractions in Toronto?
- What is the best way to travel around Toronto?
- Which places should I visit during a short trip to Toronto?
- Can you suggest some popular destinations for first-time visitors?
- What are some important things to know before traveling to Toronto?

## 🔍 Why RAG?

Traditional LLM-based chatbots generate responses using their existing training knowledge, which may sometimes result in inaccurate or outdated information.

This project uses Retrieval-Augmented Generation to improve response quality by introducing an external knowledge source.

**Key advantages:**

- **Improved Accuracy:** Responses are generated using relevant retrieved documents.
- **Reduced Hallucinations:** The model is instructed to rely on the provided context.
- **Domain-Specific Knowledge:** The chatbot focuses on information related to Toronto travel.
- **Flexible Knowledge Base:** New documents can be added without retraining the language model.
- **Efficient Retrieval:** Vector similarity search helps identify relevant information quickly.

## ⚡ Performance and Optimization

- Uses local sentence-transformers embeddings to avoid external embedding API costs.
- Stores document embeddings in Pinecone for efficient similarity-based retrieval.
- Uses overlapping text chunks to preserve context between document segments.
- Automatically initializes the vector database when running the application for the first time.
- Uses a lightweight OpenAI model (`gpt-4o-mini`) to balance response quality and API costs.
- Supports Docker-based deployment for easier setup and portability.

## 🔮 Future Improvements

Some potential improvements that could be added to the project include:

- Support for uploading custom PDF, DOCX, and TXT documents.
- Integration of additional travel-related knowledge sources.
- Displaying source documents and references alongside chatbot responses.
- Adding conversation memory for more personalized follow-up interactions.
- Implementing chat history and session management.
- Expanding the chatbot to support multiple cities and travel destinations.
- Adding response streaming for a smoother user experience.
- Deploying the application to a cloud hosting platform.

## 📌 Limitations

- The chatbot's knowledge is limited to the documents available in its knowledge base.
- Response accuracy depends on the relevance and quality of retrieved document chunks.
- An active internet connection is required for communication with OpenAI and Pinecone.
- OpenAI API usage may incur costs depending on the number of requests and selected model.
- The initial setup requires downloading the sentence-transformers embedding model.
- The quality of responses depends on the retrieval process and the information available in the source documents.

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| "Failed to start the chatbot" | Both API keys in `.env` must be valid. Check that you copied `.env.example` to `.env` and filled in real keys. |
| Index creation fails | Your Pinecone account may not support `aws/us-east-1`. Set `PINECONE_CLOUD` / `PINECONE_REGION` to a supported cloud and region (e.g. `gcp` / `us-central1`). |
| Answers look wrong | The knowledge base only covers Toronto travel. Rephrase your question or extend the documents in `src/materials/`. |
| First run is slow | The embedding model downloads once (~400 MB), and Pinecone provisions the index. |
| `docker compose up` says the env file is missing | Create `.env` from `.env.example` (see Running with Docker). |
| Docker build fails with "daemon is not running" | Start Docker Desktop and wait until it says "Engine running". |

## 👨‍💻 Author

**Mayank Sharma**
**Mayank Bisht**

## ⭐ Support

If you find this project useful, consider giving the repository a star!

Contributions, suggestions, and feedback are always welcome.
