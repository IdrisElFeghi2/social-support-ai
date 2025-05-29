import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# 📁 Folder paths
PDF_DIR = "data/laws_pdf/English"
VECTOR_DIR = "data/vectorstores/english_laws"
os.makedirs(VECTOR_DIR, exist_ok=True)

# 🧠 Load and chunk all PDFs
def load_and_split_pdfs(pdf_dir, chunk_size=512, overlap=125):
    all_docs = []
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            path = os.path.join(pdf_dir, filename)
            print(f"📄 Loading: {filename}")
            loader = PyPDFLoader(path)
            docs = loader.load()
            all_docs.extend(docs)

    print(f"✅ Loaded {len(all_docs)} documents. Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    chunks = splitter.split_documents(all_docs)
    print(f"✂️ Created {len(chunks)} chunks.")
    return chunks

# 🔍 Create vector store with HuggingFace
def create_faiss_vector_store(chunks, vector_dir):
    print("🔧 Creating embeddings using HuggingFace...")
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embedding)
    vectorstore.save_local(vector_dir)
    print(f"✅ Vector store saved to: {vector_dir}")

# 🚀 Run the pipeline
if __name__ == "__main__":
    chunks = load_and_split_pdfs(PDF_DIR)
    create_faiss_vector_store(chunks, VECTOR_DIR)
