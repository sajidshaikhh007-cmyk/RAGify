from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
ROOT_DIR = PROJECT_DIR.parent

# Load the .env file inside project/
load_dotenv(PROJECT_DIR / ".env")


# --------------------------------------------------
# FastAPI
# --------------------------------------------------

app = FastAPI(title="RAGify API")


# Allow our React frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Request model
# --------------------------------------------------

class QuestionRequest(BaseModel):
    question: str


# --------------------------------------------------
# RAG setup
# --------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory=str(ROOT_DIR / "chroma-db"),
    embedding_function=embeddings,
)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 4,
        "fetch_k": 10,
        "lambda_mult": 0.5,
    },
)


llm = ChatMistralAI(
    model="mistral-small-2506"
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful AI assistant.

Use ONLY the provided context to answer the question.

If the answer is not present in the context,
say: "I could not find the answer in the document."
""",
        ),
        (
            "human",
            """Context:
{context}

Question:
{question}
""",
        ),
    ]
)


# --------------------------------------------------
# API endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "RAGify API is running"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        return {
            "answer": "Please enter a question.",
            "sources": [],
        }

    # Retrieve relevant documents
    docs = retriever.invoke(question)

    # Create context
    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    # Create final prompt
    final_prompt = prompt.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    # Ask Mistral
    response = llm.invoke(final_prompt)

    # Extract sources
    sources = []

    for doc in docs:
        metadata = doc.metadata or {}

        source = {
            "page": (
                metadata.get("page", 0) + 1
                if isinstance(metadata.get("page"), int)
                else None
            ),
            "content": doc.page_content[:300],
        }

        sources.append(source)

    return {
        "answer": response.content,
        "sources": sources,
    }