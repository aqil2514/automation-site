from typing import List, Optional
import uuid

from pydantic import BaseModel, ConfigDict, Field


class ProcessedArticle(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    raw_content_id: Optional[uuid.UUID] = None
    title: str = Field(..., max_length=500)
    slug: str = Field(..., description="Slug untuk URL SEO")
    content_full: str
    excerpt: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    image_url: str = Field(..., description="Gambar artikel")
    status: str = Field(..., description="Status Artikel")

    model_config = ConfigDict(from_attributes=True)
