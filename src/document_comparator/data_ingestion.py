import sys
import os
from datetime import datetime
from pathlib import Path
import uuid

# custom library/package imports
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import AllAboutDocumentsException


class DocumentIngestion:
    def __init__(
        self, base_dir: str = "data\\document_comparator", session_id=None
    ) -> None:
        self.logger = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.session_id = (
            session_id
            or f"{datetime.utcnow().strftime('%Y%m%dT%H%M%S%fZ')}_{uuid.uuid4().hex[:6]}"
            # f"session_{os.getenv('USER', 'anonymous')}_{datetime.utcnow().strftime('%Y%m%dT%H%M%S%fZ')}_{uuid.uuid4().hex[:6]}"
        )
        self.session_path = self.base_dir / self.session_id
        self.session_path.mkdir(parents=True, exist_ok=True)

    # def delete_existing_files(self):
    #     try:
    #         deleted_files = []
    #         if self.base_dir.exists() or self.base_dir.is_dir():
    #             for file in self.base_dir.iterdir():
    #                 if file.is_file():
    #                     file.unlink()
    #                     deleted_files.append(str(file))
    #                     self.logger.info("File deleted", path=str(file))
    #             self.logger.info(
    #                 "Folder cleaned up",
    #                 deleted_files=deleted_files,
    #                 folder=str(self.base_dir),
    #             )
    #     except Exception as e:
    #         self.logger.error(
    #             f"Error while deleting existing documents from data for comparison: {e}"
    #         )
    #         raise AllAboutDocumentsException(
    #             "Exception during deletion of documents from data for comparison folder.",
    #             sys,
    #         )

    def save_uploaded_files(self, first_document, second_document):
        try:
            # self.delete_existing_files()
            # self.logger.info("Existing files deleted successfully.")

            first_document_path = self.session_path / first_document.name
            second_document_path = self.session_path / second_document.name

            if not first_document.name.endswith(
                ".pdf"
            ) or not second_document.name.endswith(".pdf"):
                raise ValueError(
                    "Please try uploading PDF files. We currently support PDF files only."
                )

            with open(first_document_path, "wb") as f:
                f.write(first_document.getbuffer())

            with open(second_document_path, "wb") as f:
                f.write(second_document.getbuffer())

            self.logger.info(
                "Documents saved.",
                first_document=str(first_document_path),
                second_document=str(second_document_path),
            )
            return first_document_path, second_document_path

        except Exception as e:
            self.logger.error(
                f"Error while saving existing documents in data for comparison folder:: {e}"
            )
            raise AllAboutDocumentsException(
                "Exception when saving documents in data for comparison folder.", sys
            )

    def read_document(self, pdf_path: Path) -> str:
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError("The document is encrypted and cannot be read.")
                text_extract = []
                for page_number in range(doc.page_count):
                    page = doc.load_page(page_number)
                    page_text = page.get_text()

                    if page_text.strip():
                        text_extract.append(
                            f"\n ---- Page{page_number + 1} ---- \n{page_text}"
                        )
            self.logger.info(
                "The document was read successfully.",
                file=str(pdf_path),
                pages=len(text_extract),
            )
            # print("\n".join(text_extract))
            return "\n".join(text_extract)

        except Exception as e:
            self.logger.error(f"Error while reading the document: {e}")
            raise AllAboutDocumentsException(
                "Exception when reading document for comparison.", sys
            )

    def combine_documents(self):
        try:
            content_dict = {}
            doc_parts = []

            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix == ".pdf":
                    content_dict[filename.name] = self.read_document(filename)

            for filename, content in content_dict.items():
                doc_parts.append(f"Document: {filename}\n{content}")

            combined_text = "\n\n".join(doc_parts)

            self.logger.info("Documents combined.", count=len(doc_parts))
            return combined_text

        except Exception as e:
            self.logger.error(f"Error while combining the documents: {e}")
            raise AllAboutDocumentsException(
                "Exception when combining document for comparison.", sys
            )

    def delete_old_sessions(self, max_retained_logs: int = 3):
        try:
            session_folders = sorted(
                [f for f in self.base_dir.iterdir() if f.is_dir()], reverse=True
            )
            for folder in session_folders[max_retained_logs:]:
                for file in folder.iterdir():
                    file.unlink()
                folder.rmdir()
                self.logger.info("Old session folders deleted.", path=str(folder))

        except Exception as e:
            self.logger.error("Error while purging old sessions", error=str(e))
            raise AllAboutDocumentsException("Error while purging old sessions", sys)
