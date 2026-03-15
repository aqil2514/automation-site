import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict, Field


class ArticlePosting(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    article_id: uuid.UUID
    platform_name: str  # Contoh: 'kompasiana'
    external_url: Optional[str] = None
    status: str = "queued"
    notes: Optional[str] = None
    published_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)
