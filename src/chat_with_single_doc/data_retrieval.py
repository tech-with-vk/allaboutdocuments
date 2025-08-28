import os
import sys
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import AllAboutDocumentsException
from prompt.prompt_library import PROMPT_REGISTRY
from models.models import PromptType

class ConversationalRAG:
    def __init__(self,session_id:str, retriever):
        try:
            self.logger = CustomLogger().get_logger(__name__)
        except Exception as e:
            self.logger.error("error initializing ConversationalRAG",error=str(e))
            raise AllAboutDocumentsException("error initializing ConversationalRAG",sys)
            
    def _load_llm(self):
        try:
            pass
        except Exception as e:
            self.logger.error("error when loading LLM via ModelLoader",error=str(e))
            raise AllAboutDocumentsException("error when loading LLM via ModelLoader",sys)
        
    def get_session_history(self,session_id:str):
        try:
            pass
        except Exception as e:
            self.logger.error("failed to fetch session history",error=str(e),session_id=session_id)
            raise AllAboutDocumentsException("failed to fetch session history",sys)
    
    def load_retriever_from_faiss(self):
        try:
            pass
        except Exception as e:
            self.logger.error("failed to load retriever from faiss",error=str(e))
            raise AllAboutDocumentsException("failed to load retriever from faiss",sys)
    
    def invoke(self,session_id:str):
        try:
            pass
        except Exception as e:
            self.logger.error("failed to invoke Conversation RAG",session_id=session_id,error=str(e))
            raise AllAboutDocumentsException("failed to invoke Conversation RAG",sys)   