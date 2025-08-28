import sys
import dotenv
import pandas as pd
from logger.custom_logger import CustomLogger
from exception.custom_exception import AllAboutDocumentsException
from models.models import ComparatorSummary  # noqa
from prompt.prompt_library import PROMPT_REGISTRY
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
from src import document_comparator  # noqa
from langchain.output_parsers import OutputFixingParser  # noqa


class DocumentComparatorUsingLLM:
    def __init__(self):
        dotenv.load_dotenv()
        self.logger = CustomLogger().get_logger(__name__)
        self.loader = ModelLoader()
        self.llm = self.loader.load_llm()
        self.parser = JsonOutputParser(pydantic_object=ComparatorSummary)
        # self.fixing_parser = OutputFixingParser.from_llm(
        #     parser=self.parser, llm=self.llm
        # )
        self.prompt = PROMPT_REGISTRY["document_comparator"]
        self.chain = self.prompt | self.llm | self.parser
        # self.chain = self.prompt | self.llm | self.parser | self.fixing_parser
        self.logger.info(
            "DocumentComparatorUsingLLM initialized with model and parser."
        )

    def compare_documents(self, combined_docs: str) -> pd.DataFrame:
        try:
            inputs = {
                "combined_docs": combined_docs,
                "format_instruction": self.parser.get_format_instructions(),
            }

            self.logger.info("Starting data comparison")
            response = self.chain.invoke(inputs)

            self.logger.info("Document comparison completed", response=response)
            return self._format_response(response)

        except Exception as e:
            self.logger.error(f"Error while comparing documents: {e}")
            raise AllAboutDocumentsException(
                "An error occurred while comparing documents", sys
            )

    def _format_response(self, response_parsed: list[dict]) -> pd.DataFrame:
        try:
            df = pd.DataFrame(response_parsed)
            self.logger.info("Response formatted as dataframe.", dataframe=df)
            return df
        except Exception as e:
            self.logger.error(
                "Error in formatting response into a DataFrame", error=str(e)
            )
            raise AllAboutDocumentsException(
                "Exception while formatting response into a dataframe:", sys
            )
