# Standard library imports
import dotenv
import pandas as pd

# Third-party imports
from langchain_core.output_parsers import JsonOutputParser
# from langchain.output_parsers import OutputFixingParser  # Optional: for fixing bad JSON

# Local application/library specific imports
from logger.custom_logger import CustomLogger
from exception.custom_exception import AllAboutDocumentsException
from models.models import ComparatorSummary
from prompt.prompt_library import PROMPT_REGISTRY
from utils.model_loader import ModelLoader


class DocumentComparatorUsingLLM:
    """
    Compares two PDF documents using an LLM pipeline.

    This class performs the following:
    - Loads an LLM model
    - Loads a predefined prompt for document comparison
    - Invokes the model with structured parsing
    - Returns the parsed comparison result as a pandas DataFrame
    """

    def __init__(self):
        """
        Initializes the DocumentComparatorUsingLLM with:
        - Environment variables
        - Logger
        - Language model
        - Prompt and output parser
        """
        dotenv.load_dotenv()

        self.logger = CustomLogger().get_logger(__name__)
        self.loader = ModelLoader()
        self.llm = self.loader.load_llm()

        self.parser = JsonOutputParser(pydantic_object=ComparatorSummary)

        # Optional: If LLM output is inconsistent, use OutputFixingParser
        # self.fixing_parser = OutputFixingParser.from_llm(
        #     parser=self.parser, llm=self.llm
        # )

        self.prompt = PROMPT_REGISTRY["document_comparator"]

        # Compose chain: prompt → model → parser
        self.chain = self.prompt | self.llm | self.parser
        # Alternative if using fixing parser:
        # self.chain = self.prompt | self.llm | self.parser | self.fixing_parser

        self.logger.info("DocumentComparatorUsingLLM initialized successfully.")

    def compare_documents(self, combined_docs: str) -> pd.DataFrame:
        """
        Compares the content of two documents using the LLM chain.

        Args:
            combined_docs (str): Combined content of two PDF documents.

        Returns:
            pd.DataFrame: Structured comparison result.
        """
        try:
            inputs = {
                "combined_docs": combined_docs,
                "format_instruction": self.parser.get_format_instructions(),
            }

            self.logger.info("Starting document comparison.")
            response = self.chain.invoke(inputs)
            self.logger.info("Document comparison completed successfully.")

            return self._format_response(response)

        except Exception as e:
            self.logger.error("LLM comparison failed.", error=str(e))
            raise AllAboutDocumentsException(
                "Failed to compare documents using LLM.", e
            ) from e

    def _format_response(self, response_parsed: list[dict]) -> pd.DataFrame:
        """
        Formats the LLM's parsed response into a pandas DataFrame.

        Args:
            response_parsed (list[dict]): The structured output from the LLM parser.

        Returns:
            pd.DataFrame: Tabular format of comparison results.
        """
        try:
            df = pd.DataFrame(response_parsed)
            self.logger.info("LLM response formatted as DataFrame.", DataFrame=df)
            return df

        except Exception as e:
            self.logger.error(
                "Failed to convert LLM response to DataFrame.", error=str(e)
            )
            raise AllAboutDocumentsException(
                "Failed to format LLM response into a DataFrame.", e
            ) from e
