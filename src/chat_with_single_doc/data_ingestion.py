import sys
import uuid
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from logger.custom_logger import CustomLogger
from exception.custom_exception import AllAboutDocumentsException
from utils.model_loader import ModelLoader


class ChatWithSingleDocument:
    def __init__(self):
        try:
            self.logger = CustomLogger().get_logger(__name__)
        except Exception as e:
            self.logger.error(
                "failed to initialize ChatWithSingleDocument class", error=str(e)
            )
            raise AllAboutDocumentsException(
                "failed to initialize ChatWithSingleDocument class", sys
            )

    def ingest_files(self):
        try:
            pass
        except Exception as e:
            self.logger.error("document ingestion failed", error=str(e))
            raise AllAboutDocumentsException("document ingestion failed", sys)

    def _create_retriever(self):
        try:
            pass
        except Exception as e:
            self.logger.error("failed to create retriever", error=str(e))
            raise AllAboutDocumentsException("failed to create retriever", sys)
