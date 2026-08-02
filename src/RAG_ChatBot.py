from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
import time
from pathlib import Path
from pinecone import Pinecone, ServerlessSpec
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


class ChatBot:
    load_dotenv()
    def __init__(self):

        # Load and split the knowledge base into retrievable chunks
        materials_path = Path(__file__).resolve().parent / "materials" / "torontoTravelAssistant.txt"
        loader = TextLoader(str(materials_path))
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_documents(documents)

        # Local embeddings (all-mpnet-base-v2, 768-dim) — no API cost
        embeddings = HuggingFaceEmbeddings()

        # Connect to Pinecone (serverless)
        pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

        index_name = "langchain-demo"
        cloud = os.getenv('PINECONE_CLOUD', 'aws')
        region = os.getenv('PINECONE_REGION', 'us-east-1')

        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=768,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=cloud,
                    region=region
                )
            )
            # Wait for a freshly created index to become ready (bounded to ~60s)
            for _ in range(60):
                if pc.describe_index(index_name).status.ready:
                    break
                time.sleep(1)

        index = pc.Index(index_name)

        # Embed chunks and store them in Pinecone
        texts = [doc.page_content for doc in docs]
        embedded = embeddings.embed_documents(texts)
        vectors = [
            {"id": f"chunk-{i}", "values": embedded[i], "metadata": {"text": texts[i]}}
            for i in range(len(texts))
        ]
        index.upsert(vectors=vectors)

        # LLM (configurable via OPENAI_MODEL)
        model_name = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        llm = ChatOpenAI(model=model_name)

        # Define prompt template
        template = """
        You are a Toronto travel assistant. Users will ask you questions about their trip to Toronto. Use the following piece of context to answer the question.
        If you don't know the answer, just say you don't know.
        Your answer should be short and concise, no longer than 2 sentences.

        Context: {context}
        Question: {question}
        Answer:
        """

        prompt = ChatPromptTemplate.from_template(template)

        def retrieve(query):
            query_vector = embeddings.embed_query(query)
            result = index.query(vector=query_vector, top_k=4, include_metadata=True)
            return [
                Document(page_content=match.metadata["text"])
                for match in result.matches
            ]

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self.rag_chain = (
            {
                "context": lambda query: format_docs(retrieve(query)),
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
            | StrOutputParser()
        )


# Usage example:
if __name__ == "__main__":
    chatbot = ChatBot()
