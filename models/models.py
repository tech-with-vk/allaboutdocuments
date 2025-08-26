from ctypes import Union
from pydantic import BaseModel, Field
from typing import List, Union  # noqa: F811


class Metadata(BaseModel):
    Summary: List[str] = Field(
        default_factory=list, description="Summary of the doucment"
    )
    Title: str
    Author: str
    DateCreated: str
    LastModifiedDate: str
    Publisher: str
    Language: str
    PageCount: Union[int, str]
    SentimentTone: str
