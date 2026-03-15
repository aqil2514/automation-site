from pydantic import BaseModel
from typing import List, Optional


class ArticleSchema(BaseModel):
    title: str
    content: str
    url: str
    authors: List[str] = []
    top_image: Optional[str] = None
    status: str
