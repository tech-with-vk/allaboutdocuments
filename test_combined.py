# ############# Test code for document ingestion and analysis using a PDFHandler and DocumentMetadataAnalyzer #############

import io
from pathlib import Path
from datetime import datetime
import uuid

from src.document_analyzer.data_ingestion import DocumentHandler
from src.document_analyzer.document_metadata_analysis import DocumentMetadataAnalyzer
from src.document_comparator.data_ingestion import DocumentIngestion
from src.document_comparator.document_comparison import DocumentComparatorUsingLLM

# # Path to the PDF you want to test
# PDF_PATH = r"D:\\00.LLMOPS\\allaboutdocuments\\data\\document_analyzer\\350 NLP Projects with Code.pdf"


# # Dummy file wrapper to simulate uploaded file (Streamlit style)
# class DummyFile:
#     def __init__(self, file_path):
#         self.name = Path(file_path).name
#         self._file_path = file_path

#     def getbuffer(self):
#         return open(self._file_path, "rb").read()


# def test_document_analyzer():
#     try:
#         # ---------- STEP 1: DATA INGESTION ----------
#         print("Starting PDF ingestion...")
#         dummy_pdf = DummyFile(PDF_PATH)

#         handler = DocumentHandler(
#             # session_id=f"session_{os.getenv('USER', 'anonymous')}_{datetime.utcnow().strftime('%Y%m%dT%H%M%S%fZ')}_{uuid.uuid4().hex[:6]}"
#             session_id=f"{datetime.utcnow().strftime('%Y%m%dT%H%M%S%fZ')}_{uuid.uuid4().hex[:6]}"
#         )

#         saved_path = handler.save_pdf(dummy_pdf)
#         print(f"PDF saved at: {saved_path}")

#         text_content = handler.read_pdf(saved_path)
#         print(f"Extracted text length: {len(text_content)} chars\n")

#         # ---------- STEP 2: DATA ANALYSIS ----------
#         print("Starting metadata analysis...")
#         analyzer = DocumentMetadataAnalyzer()  # Loads LLM + parser

#         analysis_result = analyzer.analyze_document(text_content)

#         # ---------- STEP 3: DISPLAY RESULTS ----------
#         print("\n=== METADATA ANALYSIS RESULT ===")
#         for key, value in analysis_result.items():
#             print(f"{key}: {value}")

#     except Exception as e:
#         print(f"Test failed: {e}")


# if __name__ == "__main__":
#     test_document_analyzer()


# Test code for document ingestion and analysis using a PDFHandler and DocumentMetadataAnalyzer
# from pathlib import Path
# from src.document_analyzer.data_ingestion import DocumentHandler
# from src.document_analyzer.document_metadata_analysis import DocumentMetadataAnalyzer


# 📁 Define the directory containing PDFs
PDF_DIR = Path("data/document_analyzer")  # relative to project root or adjust as needed


# 🔍 Pick the first PDF file found in the directory
def get_first_pdf_file(directory: Path):
    if not directory.exists() or not directory.is_dir():
        raise FileNotFoundError(f"Directory not found: {directory}")

    pdf_files = list(directory.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError("No PDF files found in the directory.")

    return pdf_files[0]  # You can modify this to select randomly or by name


# Dummy file wrapper to simulate uploaded file (Streamlit style)
class DummyFile:
    def __init__(self, file_path):
        self.name = file_path.name
        self._file_path = file_path

    def getbuffer(self):
        return open(self._file_path, "rb").read()


def test_document_analyzer():
    try:
        # ---------- STEP 1: DATA INGESTION ----------
        print("Starting PDF ingestion...")

        pdf_path = get_first_pdf_file(PDF_DIR)
        print(f"Selected PDF: {pdf_path}")

        dummy_pdf = DummyFile(pdf_path)

        handler = DocumentHandler(
            session_id=f"{datetime.utcnow().strftime('%Y%m%dT%H%M%S%fZ')}_{uuid.uuid4().hex[:6]}"
        )

        saved_path = handler.save_pdf(dummy_pdf)
        print(f"PDF saved at: {saved_path}")

        text_content = handler.read_pdf(saved_path)
        print(f"Extracted text length: {len(text_content)} chars\n")

        # ---------- STEP 2: DATA ANALYSIS ----------
        print("Starting metadata analysis...")
        analyzer = DocumentMetadataAnalyzer()  # Loads LLM + parser

        analysis_result = analyzer.analyze_document(text_content)

        # ---------- STEP 3: DISPLAY RESULTS ----------
        print("\n=== METADATA ANALYSIS RESULT ===")
        for key, value in analysis_result.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Test failed: {e}")


if __name__ == "__main__":
    test_document_analyzer()


# ############# Testing code for document comparison using LLMs #############


def load_fake_uploaded_file(file_path: Path):
    return io.BytesIO(file_path.read_bytes())


def test_compare_documents():
    first_document_path = Path(
        "D:\\00.LLMOPS\\allaboutdocuments\\data\document_comparator\\The Benefits of LLMs V1.pdf"
    )
    second_document_path = Path(
        "D:\\00.LLMOPS\\allaboutdocuments\\data\document_comparator\\The Benefits of LLMs V2.pdf"
    )

    class FakeUpload:
        def __init__(self, file_path: Path) -> None:
            self.name = file_path.name
            self.buffer = file_path.read_bytes()

        def getbuffer(self):
            return self.buffer

    comparator = DocumentIngestion()
    first_document_upload = FakeUpload(first_document_path)
    second_document_upload = FakeUpload(second_document_path)

    first_document, second_document = comparator.save_uploaded_files(
        first_document_upload, second_document_upload
    )
    combined_text = comparator.combine_documents()
    comparator.delete_old_sessions(max_retained_logs=3)

    print("\n combined text preview (first 500) characters: \n")
    print(combined_text[:500])
    # print(combined_text)

    llm_comparator = DocumentComparatorUsingLLM()
    comparison_df = llm_comparator.compare_documents(combined_text)

    print("\n Comparison DataFrame:\n")
    print(comparison_df.head())


if __name__ == "__main__":
    test_compare_documents()
