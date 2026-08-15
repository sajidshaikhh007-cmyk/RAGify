# from langchain_community.document_loaders import PyPDFLoader

# from langchain_text_splitters import RecursiveCharacterTextSplitter
    
# loader=PyPDFLoader("Text Book Machine LEarning.pdf")

# docs=loader.load()

# # print(len(docs))

# splitter=RecursiveCharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=200
# )
# chunks=splitter.split_documents(docs)

# print(chunks[0].page_content)

from langchain_community.document_loaders import WebBaseLoader
url="https://www.apnacollege.in/"

loader=WebBaseLoader(url)
docs=loader.load()
print(docs[0].page_content)
