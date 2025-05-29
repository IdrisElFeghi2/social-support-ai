import streamlit as st
from langdetect import detect
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
import re

def clean_t5_output(text):
    return re.sub(r"<extra_id_\d+>", "", text).strip()
# Setup
st.set_page_config(page_title="Legal Assistant", layout="wide")
st.title("📚 UAE Legal Assistant - Multilingual (Arabic & English)")

# Load multilingual embedding model
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Load vector stores
english_store = FAISS.load_local("data/vectorstores/english_laws", embeddings=embedding, allow_dangerous_deserialization=True)
arabic_store = FAISS.load_local("data/vectorstores/arabic_laws", embeddings=embedding, allow_dangerous_deserialization=True)

# Load light-weight multilingual LLM
from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("google/mt5-small", use_fast=False)
model = T5ForConditionalGeneration.from_pretrained("google/mt5-small")

llm_pipeline = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=256,
    do_sample=True,
    temperature=0.1,
    device=-1  # or 0 if you're using GPU
)
llm = HuggingFacePipeline(pipeline=llm_pipeline)

# RAG prompt template
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

# Get language from langdetect
def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

# Main UI
question = st.text_input("Ask a legal question (Arabic or English):")

if question:
    lang = detect_language(question)
    st.write(f"🌐 Detected Language: {'Arabic' if lang == 'ar' else 'English'}")

    retriever = arabic_store.as_retriever(k=4) if lang == 'ar' else english_store.as_retriever(k=4)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

    with st.spinner("Searching legal documents..."):
        answer = qa_chain.run(question)
        answer = clean_t5_output(answer)

    st.markdown("### 📌 Answer")
    st.write(answer)
