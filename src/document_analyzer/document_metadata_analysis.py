from langchain_community.vectorstores.starrocks import Metadata
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import AllAboutDocumentsException
from models.models import Metadata
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from prompt.prompt_library import prompt_to_analyze_document_metadata


class DocumentMetadataAnalyzer:
    def __init__(self) -> None:
        # Set up the custom logger for this module
        self.logger = CustomLogger().get_logger(__name__)

        try:
            # Load the language model (e.g., ChatGPT, Gemini, Claude, etc.)
            self.loader = ModelLoader()
            self.llm = self.loader.load_llm()  # Initialize the model

            # Define a JSON parser to convert model output into a `Metadata` Pydantic model
            self.parser = JsonOutputParser(pydantic_object=Metadata)

            # Use OutputFixingParser to correct malformed JSON outputs using the LLM
            self.fixing_parser = OutputFixingParser.from_llm(
                parser=self.parser, llm=self.llm
            )

            # Load the prompt template for document metadata analysis
            self.prompt_to_analyze_document_metadata = (
                prompt_to_analyze_document_metadata
            )

            # Log success message once initialization is complete
            self.logger.info("Document analyzer initialized successfully")

        except Exception as e:
            # Log error if anything goes wrong during initialization
            self.logger.error(
                f"Error while initializing Document Metadata Analyzer: {e}"
            )
            # Raise a custom exception, including the original error
            raise AllAboutDocumentsException(
                "Error while initializing Document Metadata Analyzer.", e
            ) from e

    def analyze_document(self, document_text: str) -> dict:
        """
        Examine a document's content using a pre-trained model to extract structured metadata and generate a summary.
        Logs all activities to log file for troubleshooting purposes.

        Args:
            document_text (str): The raw text of the document to analyze.

        Returns:
            dict: A dictionary representing structured metadata extracted from the document.
        """
        try:
            # Compose the processing chain: prompt → LLM → output parser
            chain = (
                self.prompt_to_analyze_document_metadata | self.llm | self.fixing_parser
            )
            self.logger.info("Metadata analysis chain initiated.")

            # Invoke the chain with required inputs, including format instructions for valid JSON
            response = chain.invoke(
                {
                    "format_instructions": self.parser.get_format_instructions(),
                    "document_text": document_text,
                }
            )

            # Log successful analysis
            self.logger.info("Metadata analysis successful.")
            return response  # Return structured metadata

        except Exception as e:
            # Log error if the analysis fails
            self.logger.error(f"Document metadata analysis failed: {e}")

            # Raise a custom exception, preserving the original exception
            raise AllAboutDocumentsException(
                "Failed to initialize Document Handler", e
            ) from e
