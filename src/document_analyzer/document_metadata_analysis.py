# Standard library imports
import sys

# Local application imports
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import AllAboutDocumentsException
from models.models import Metadata
from prompt.prompt_library import PROMPT_REGISTRY

# Langchain imports
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser


class DocumentMetadataAnalyzer:
    """
    Analyzes raw document text using an LLM to extract structured metadata in JSON format.
    Automatically applies output correction and logs all key operations.
    """

    def __init__(self) -> None:
        """
        Initialize the DocumentMetadataAnalyzer by:
        - Loading the language model
        - Preparing output parsers
        - Fetching the prompt template for metadata extraction
        """
        self.logger = CustomLogger().get_logger(__name__)

        try:
            # Load LLM and initialize parser
            self.loader = ModelLoader()
            self.llm = self.loader.load_llm()

            # Parser for converting LLM output to Metadata model
            self.parser = JsonOutputParser(pydantic_object=Metadata)

            # Use fixing parser to repair malformed outputs using LLM
            self.fixing_parser = OutputFixingParser.from_llm(
                parser=self.parser, llm=self.llm
            )

            # Load prompt for metadata analysis
            self.prompt_to_analyze_document_metadata = PROMPT_REGISTRY[
                "document_analyzer"
            ]

            self.logger.info("DocumentMetadataAnalyzer initialized successfully.")

        except Exception as e:
            self.logger.error(
                "Failed to initialize DocumentMetadataAnalyzer.", error=str(e)
            )
            raise AllAboutDocumentsException(
                "Initialization failed in DocumentMetadataAnalyzer.", e
            ) from e

    def analyze_document(self, document_text: str) -> dict:
        """
        Analyzes raw document content to extract metadata using the loaded LLM and prompt.

        Args:
            document_text (str): Full text content of the document to be analyzed.

        Returns:
            dict: Parsed metadata conforming to the Metadata schema.
        """
        try:
            # Construct the LLM chain: Prompt → LLM → Output Parser
            chain = (
                self.prompt_to_analyze_document_metadata | self.llm | self.fixing_parser
            )

            self.logger.info("Starting metadata analysis chain.")

            # Invoke the chain with format instructions and input document
            response = chain.invoke(
                {
                    "format_instructions": self.parser.get_format_instructions(),
                    "document_text": document_text,
                }
            )

            self.logger.info("Metadata analysis completed successfully.")
            return response

        except Exception as e:
            self.logger.error("Failed to analyze document metadata.", error=str(e))
            raise AllAboutDocumentsException(
                "Metadata analysis failed in DocumentMetadataAnalyzer.", e
            ) from e
