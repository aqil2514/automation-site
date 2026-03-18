import datetime
import uuid

from pydantic import BaseModel, Field


class ProcessedArticles(BaseModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        description="ID unik untuk setiap konten mentah (otomatis dibuat)",
    )

    raw_content_id: uuid.UUID = Field(
        ...,
        description="ID unik dari table raw_contents",
    )

    title: str = Field(..., description="Judul Artikel")

    slug: str = Field(..., description="Slug dari artikel")

    content_full: str = Field(..., description="Isi artikel")

    excerpt: str = Field(..., description="Deskripsi singkat dari isi artikel")

    tags: list[str] = Field([], description="Tag tentang artikel")

    created_at: datetime.datetime = Field(
        ..., description="Tanggal digenerate-nya artikel oleh AI"
    )

    image_url: str = Field(..., description="Gambar dan URL Artikel")

    status: str = Field(
        ..., description="Status artikel (Untuk audit manual sebelum publish)"
    )
