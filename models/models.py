# Pydantic is used for data validation and serialization.
from pydantic import BaseModel, Field, RootModel

# Typing module for advanced type hints.
from typing import List, Union

# Enum class used for defining constant prompt types.
from enum import Enum


class Metadata(BaseModel):
    """
    Represents extracted metadata from a document.

    Attributes:
        Summary (List[str]): A list of key summary points extracted from the document.
        Title (str): Title of the document.
        Author (str): Author of the document.
        DateCreated (str): Document creation date (string format for simplicity).
        LastModifiedDate (str): Last modified date of the document.
        Publisher (str): Publisher of the document, if available.
        Language (str): Language in which the document is written.
        PageCount (Union[int, str]): Total number of pages (may be unknown or string).
        SentimentTone (str): Overall sentiment or tone of the document.
    """

    Summary: List[str] = Field(
        default_factory=list, description="Summary of the document"
    )
    Title: str
    Author: str
    DateCreated: str
    LastModifiedDate: str
    Publisher: str
    Language: str
    PageCount: Union[
        int, str
    ]  # Can be int or str, to handle cases where page count is unknown
    SentimentTone: str


class FormatForChanges(BaseModel):
    """
    Represents changes found on a particular page during document comparison.

    Attributes:
        Page (str): Page number or identifier.
        Changes (str): Description of what has changed on the page.
    """

    Page: str
    Changes: str


class ComparatorSummary(RootModel[list[FormatForChanges]]):
    """
    Root model that encapsulates a list of page-wise comparison results.

    Used as the output schema for document comparison tasks.
    """

    pass


class PromptType(str, Enum):
    """
    Enum defining standardized keys for prompt templates used across the application.

    These values are used to retrieve the correct prompt from the PROMPT_REGISTRY.
    """

    DOCUMENT_ANALYSIS = "document_analysis"
    DOCUMENT_COMPARISON = "document_comparison"
    CONTEXTUALIZE_QUESTION = "contextualize_question"
    CONTEXT_QA = "context_qa"
