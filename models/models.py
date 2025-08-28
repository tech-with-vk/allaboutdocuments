from pydantic import BaseModel, Field, RootModel
from typing import List, Union
from enum import Enum


class Metadata(BaseModel):
    Summary: List[str] = Field(
        default_factory=list, description="Summary of the document"
    )
    Title: str
    Author: str
    DateCreated: str
    LastModifiedDate: str
    Publisher: str
    Language: str
    PageCount: Union[int, str]  # This data may not be available always
    SentimentTone: str

class FormatForChanges(BaseModel):
    Page: str
    Changes: str


class ComparatorSummary(RootModel[list[FormatForChanges]]):
    pass


class PromptType(str, Enum):
    DOCUMENT_ANALYSIS = "document_analysis"
    DOCUMENT_COMPARISON = "document_comparison"
    CONTEXTUALIZE_QUESTION = "contextualize_question"
    CONTEXT_QA = "context_qa"