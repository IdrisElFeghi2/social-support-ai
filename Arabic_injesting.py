import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Paths
TEXT_DIR = "data/laws_pdf/Arabic/text"
VECTOR_DIR = "data/vectorstores/arabic_laws"


# Load and split .txt documents
def load_and_split_txts(text_dir, chunk_size=512, overlap=125):
    all_docs = []
    for filename in os.listdir(text_dir):
        if filename.endswith(".txt"):
            path = os.path.join(text_dir, filename)
            print(f"📄 Loading: {filename}")
            loader = TextLoader(path, encoding="utf-8")
            docs = loader.load()
            all_docs.extend(docs)

    print(f"✅ Loaded {len(all_docs)} documents. Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    chunks = splitter.split_documents(all_docs)
    print(f"✂️ Created {len(chunks)} chunks.")
    return chunks

# Create FAISS vector store
def create_faiss_vector_store(chunks, vector_dir):
    print("🔧 Creating embeddings using multilingual model...")
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    vectorstore = FAISS.from_documents(chunks, embedding)
    vectorstore.save_local(vector_dir)
    print(f"✅ Vector store saved to: {vector_dir}")

# Run the pipeline
if __name__ == "__main__":
    chunks = load_and_split_txts(TEXT_DIR)
    create_faiss_vector_store(chunks, VECTOR_DIR)
