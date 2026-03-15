import uuid

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.services.vertext_ai.articles.generate import generate_article_from_raw
from src.db.tables.raw_contents.select import select_raw_contents
from src.db.tables.processed_articles.model import ProcessedArticle
from src.db.tables.processed_articles.insert import insert_processed_article
from src.db.tables.article_postings.model import ArticlePosting
from src.db.tables.article_postings.insert import insert_article_posting

router = APIRouter(prefix="/articles", tags=["Articles Generation"])


class GenerateArticleResponse(BaseModel):
    status: str
    message: str
    article_id: uuid.UUID


@router.post(
    "/generate",
    status_code=status.HTTP_201_CREATED,
    response_model=GenerateArticleResponse,
    summary="Simpan Hasil Artikel AI",
    description="Endpoint untuk menyimpan artikel yang sudah ditulis AI dan otomatis masuk antrean posting.",
)
async def generate_article_handler(payload: ProcessedArticle):
    """
    Proses yang dilakukan:
    1. Validasi data artikel hasil AI.
    2. Simpan ke tabel `processed_articles`.
    3. Buat entri antrean di `article_postings` untuk platform Kompasiana.
    """
    try:
        # 1. Simpan artikel utama
        article_id = await insert_processed_article(payload)

        # 2. Buat antrean posting secara otomatis (Default: Kompasiana)
        posting_payload = ArticlePosting(
            article_id=uuid.UUID(str(article_id)),
            platform_name="kompasiana",
            status="queued",
        )
        await insert_article_posting(posting_payload)

        return {
            "status": "success",
            "message": "Artikel berhasil disimpan dan masuk antrean posting.",
            "article_id": str(article_id),
        }

    except Exception as e:
        print(f"Error pada generate_article_handler: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gagal memproses pembuatan artikel.",
        )


@router.post("/generate-ai")
async def generate_article_ai():
    pending_article = await select_raw_contents("pending")
    oldest_article = pending_article[-1]

    processed_article = await generate_article_from_raw(oldest_article)

    await insert_processed_article(processed_article)

    return {
        "message": "Artikel berhasil disimpan",
        "response": processed_article,
    }
