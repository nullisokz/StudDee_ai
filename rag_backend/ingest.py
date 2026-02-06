from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import shutil
import os

pdf_path = "./ai_ml_bok_kap1_kap2.pdf"
embed_model = "sentence-transformers/all-MiniLM-L6-v2"
dbpath = os.path.expanduser("./chroma_db")



def main():

    if not os.path.exists(pdf_path):
        print("Ingen matchande pdf fil")
        raise FileNotFoundError(f'Hittar ej pdf fil')

    if os.path.exists(dbpath):
        print("Rensar extisterande db")
        shutil.rmtree(dbpath)

    print(f"Laddar pdf...")
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    pages = pages[13:]
    print(f'{len(pages)} sidor laddade')

    print("Chunking..")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = splitter.split_documents(pages)
    print(f'{len(chunks)} antal chunks laddade')

    embeddings = HuggingFaceEmbeddings(
        model_name = embed_model
    )

    print(f'Sparar till chroma db...')
    Chroma.from_documents(
        documents=chunks,
        embedding = embeddings,
        persist_directory = dbpath 
    )

    print(f'Klart, ChromaDB är byggd')

if __name__ == "__main__":
    main()