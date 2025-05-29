import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline
from langdetect import detect

# Embedding models

english_embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
arabic_embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Load vector stores
english_vectorstore = FAISS.load_local(
    "data/vectorstores/english_laws",
    embeddings=english_embedding,
    allow_dangerous_deserialization=True
)

arabic_vectorstore = FAISS.load_local(
    "data/vectorstores/arabic_laws",
    embeddings=arabic_embedding,
    allow_dangerous_deserialization=True
)

# Load LLM (CPU friendly)
llm_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    tokenizer="google/flan-t5-base",
    max_new_tokens=256,
    do_sample=True,
    temperature=0.1,
    device=-1  # CPU
)

llm = HuggingFacePipeline(pipeline=llm_pipeline)

# Prompt Template
prompt = PromptTemplate(
    template="""
You are a legal assistant. Use ONLY the following law excerpts to answer.

Question: {question}

Law Chunks:
{context}

Answer:
""",
    input_variables=["question", "context"]
)

# Function to route question to appropriate vectorstore
def answer_question(question: str) -> str:
    lang = detect(question)
    print(f"🧭 Detected Language: {lang}")
    
    if lang == "ar":
        retriever = arabic_vectorstore.as_retriever(search_type="similarity", k=4)
    else:
        retriever = english_vectorstore.as_retriever(search_type="similarity", k=4)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain.run(question)
