"""
Test script for Conversational Retrieval-Augmented Generation (RAG) on a single document.

This script:
1. Loads an existing FAISS index if available, otherwise creates one.
2. Initializes a retriever from the FAISS index.
3. Uses ConversationalRAG to answer a user question based on the document context.
"""

#  Standard Library Imports
import sys
from pathlib import Path

#  Third-Party Library Imports
from langchain_community.vectorstores import FAISS

#  Local Application Imports
from src.chat_with_a_document.data_ingestion import SingleDocumentIngestor
from src.chat_with_a_document.data_retrieval import ConversationalRAG
from utils.model_loader import ModelLoader

# Path to the FAISS index directory
FAISS_INDEX_PATH = Path("faiss_index")


def test_conversational_rag(pdf_path: str, question: str) -> None:
    """
    Executes a test of Conversational RAG on a given document and question.

    Args:
        pdf_path (str): Path to the PDF document.
        question (str): Natural language question for RAG to answer.
    """
    try:
        # Initialize the model loader (for embeddings)
        model_loader = ModelLoader()

        # ---------- STEP 1: Load FAISS Index or Ingest Document ----------
        if FAISS_INDEX_PATH.exists():
            print("📦 FAISS index found. Loading index...")

            embeddings = model_loader.load_embeddings()

            # Load the FAISS vector store from local path
            vectorstore = FAISS.load_local(
                folder_path=str(FAISS_INDEX_PATH),
                embeddings=embeddings,
                allow_dangerous_deserialization=True,
            )

            # Create a retriever for semantic search
            retriever = vectorstore.as_retriever(
                search_type="similarity", search_kwargs={"k": 5}
            )
        else:
            print("⚠️ FAISS index not found. Ingesting document to build index...")

            with open(pdf_path, "rb") as f:
                uploaded_files = [f]

                # Ingest the file and build the FAISS index
                ingestor = SingleDocumentIngestor()
                retriever = ingestor.ingest_files(uploaded_files)

        # ---------- STEP 2: Run Conversational RAG ----------
        print("💬 Running Conversational RAG...")
        session_id = "test_conversational_rag_session"

        rag = ConversationalRAG(retriever=retriever, session_id=session_id)
        response = rag.invoke(question)

        print("\n++++++++++ RAG RESPONSE ++++++++++")
        print(f"Question: {question}")
        print(f"Answer: {response}")

    except Exception as e:
        print(f"❌ Test failed. Reason: {str(e)}.")
        sys.exit(1)


if __name__ == "__main__":
    # ---------- Configuration ----------
    pdf_path = "data/chat_with_a_document/ML Projects in python.pdf"
    question = "What is the theme of the document?"

    # ---------- Pre-check ----------
    if not Path(pdf_path).exists():
        print(f"❌ File not found at: {pdf_path}")
        sys.exit(1)

    # ---------- Run Test ----------
    test_conversational_rag(pdf_path, question)
