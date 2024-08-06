from pydantic import BaseModel
from typing import Optional


class PublishData(BaseModel):
    platform: Optional[str] = "toutiao"
    title: str
    content: str
    mp3Url: str
