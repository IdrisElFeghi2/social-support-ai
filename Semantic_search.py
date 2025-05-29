from langchain_community.vectorstores import FAISS  # ✅ Correct import
from langchain_huggingface import HuggingFaceEmbeddings  # ✅ Correct import

# Initialize embedding model (local and free)
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load the vector store (set allow_dangerous_deserialization=True because you created it)
vectorstore = FAISS.load_local(
    "data/vectorstores/english_laws",
    embeddings=embedding,
    allow_dangerous_deserialization=True
)

# Run a semantic search
query = "What are the laws of scial befits?"
results = vectorstore.similarity_search(query, k=3)

# Print results
for i, doc in enumerate(results, 1):
    print(f"\n🔹 Result {i}:\n{doc.page_content}\n")
