import streamlit as st
from dotenv import load_dotenv
# from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader



load_dotenv("environment/.env")

loader=PyPDFLoader("Text Book Machine LEarning.pdf")

docs=loader.load()

# print(len(docs))

# splitter=RecursiveCharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=200
# )
# chunks=splitter.split_documents(docs)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2")


vectorstore = Chroma(
    persist_directory= "chroma-db",
    embedding_function=embeddings
)
retriver=vectorstore.as_retriever(
        search_type = "mmr",
          search_kwargs ={
        "k" : 4,
        "fetch_k":10,
         "lambda_mult" :0.5}
)

llm = ChatMistralAI(model ="mistral-small-2506")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful AI assistant.

Use ONLY the provided context to answer the question.

If the answer is not present in the context,
say: "I could not find the answer in the document."
"""
        ),
        (
            "human",
            """Context:
{context}

Question:
{question}
"""
        )
    ]
)

st.set_page_config(page_title="RAG Chat")
st.title("RAG Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

query = st.chat_input("You :")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)

    docs = retriver.invoke(query)
    context = "\n\n".join(
        [doc.page_content for doc in docs]
     )

    final_prompt = prompt.invoke({
        "context" :context,
        "question": query
     })

    response=llm.invoke(final_prompt)

    with st.chat_message("assistant"):
        st.write(response.content)
    st.session_state.messages.append({"role": "assistant", "content": response.content})