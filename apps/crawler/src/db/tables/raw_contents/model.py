import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class RawContent(BaseModel):
    # Kita berikan deskripsi dan contoh agar user tahu formatnya
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        description="ID unik untuk setiap konten mentah (otomatis dibuat)",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )

    source_url: str = Field(
        ...,
        description="URL sumber asli dari konten yang di-scrape",
        examples=["https://tekno.kompas.com/read/2026/03/15/berita-ai-terbaru"],
    )

    title: str = Field(
        ...,
        description="Judul artikel atau konten mentah",
        max_length=500,
        examples=["Masa Depan Kecerdasan Buatan di Tahun 2026"],
    )

    content_raw: str = Field(
        ...,
        description="Isi konten lengkap dalam bentuk teks mentah atau HTML",
        examples=["Laporan terbaru menunjukkan bahwa..."],
    )

    image_url: Optional[str] = Field(
        None,
        description="URL gambar utama jika tersedia",
        examples=["https://img.kompas.com/data/ai-future.jpg"],
    )

    status: str = Field(
        "pending",
        description="Status pemrosesan konten (misal: pending, processing, completed)",
        examples=["pending"],
    )

    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description="Waktu data dimasukkan ke database",
        examples=["2026-03-15T05:28:30"],
    )

    # Menggunakan model_config (Cara modern di Pydantic V2)
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "source_url": "https://example.com/news",
                "title": "Contoh Judul Berita",
                "content_raw": "Ini adalah isi teks mentah yang sangat panjang...",
                "image_url": "https://example.com/image.jpg",
                "status": "pending",
            }
        },
    )
