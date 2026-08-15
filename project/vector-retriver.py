from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings




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