import asyncio
from functools import partial
from io import BytesIO
import json

import cloudinary
import cloudinary.uploader

from src.db.tables.processed_articles.model import ProcessedArticle
from src.db.tables.raw_contents.model import RawContent

from src.services.vertext_ai.connection import vertex_client
from google.genai import types

_TEMPLATE_PROMPT = """
    Anda adalah seorang jurnalis profesional. 
    Tulis ulang berita berikut menjadi artikel blog yang menarik untuk Kompasiana.
    
    Judul Asli: {title_raw}
    Konten Asli: {content_raw}
    Sumber Konten: {source_url}
    
    Ketentuan:
    1. Gaya bahasa santai tapi informatif.
    2. Buat judul yang lebih clickbait tapi tetap akurat.
    3. Buat slug (URL friendly) dari judul tersebut.
    4. Berikan ringkasan singkat (excerpt) maksimal 160 karakter.
    5. Berikan 3-5 tags yang relevan.
    6. Buatlah prompt deskriptif (dalam bahasa Inggris) untuk menghasilkan gambar utama artikel ini menggunakan AI. Prompt harus detail, mendeskripsikan subjek, suasana, dan gaya (misal: gaya ilustrasi cat air atau foto jurnalisme dramatis).
    
    Format Output (JSON):
    {{
        "title": "...",
        "slug": "...",
        "content_full": "...",
        "excerpt": "...",
        "tags": ["...", "...", "..."]
        "ai_image_prompt" :"..."
    }}
    """


async def generate_article_from_raw(content_raw: RawContent) -> ProcessedArticle:
    prompt = _TEMPLATE_PROMPT.format(
        title_raw=content_raw.title,
        content_raw=content_raw.content_raw,
        source_url=content_raw.source_url,
    )

    response = vertex_client.models.generate_content(
        model="gemini-2.5-flash",
        contents={"text": prompt},
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )

    article_text = response.candidates[0].content.parts[0].text  # type: ignore
    article_data = json.loads(str(article_text))
    image_prompt = article_data.get("ai_image_prompt")

    slug = article_data.get("slug", "default-slug")
    image_url = await generate_article_image(image_prompt, slug)

    return ProcessedArticle(
        raw_content_id=content_raw.id,
        title=article_data.get("title", ""),
        slug=article_data.get("slug", ""),
        content_full=article_data.get("content_full", ""),
        excerpt=article_data.get("excerpt", ""),
        tags=article_data.get("tags", []),
        image_url=image_url,
        status="pending",
    )


async def generate_article_image(image_prompt: str, slug: str) -> str:
    """
    Fungsi ini melakukan generate gambar via Gemini dan langsung upload ke Cloudinary.
    Mengembalikan URL Cloudinary jika sukses, atau string kosong jika gagal.
    """
    try:
        # 1. Generate Gambar dari Gemini
        image_response = vertex_client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=image_prompt,
            config=types.GenerateContentConfig(
                image_config=types.ImageConfig(aspect_ratio="16:9")
            ),
        )

        # 2. Ekstrak Bytes Gambar
        image_bytes = None
        if image_response.candidates:
            for part in image_response.candidates[0].content.parts:  # type: ignore
                if part.inline_data:
                    image_bytes = part.inline_data.data
                    break

        if not image_bytes:
            print(
                "Warning: AI tidak mengembalikan gambar (mungkin terblokir safety filter)."
            )
            return ""

        # 3. Langsung Upload Bytes ke Cloudinary
        # Tidak perlu simpan ke lokal (static/images) lagi
        cloud_url = await upload_image_to_cloud(image_bytes, slug)

        return cloud_url

    except Exception as e:
        print(f"Error pada generate_article_image: {e}")
        return ""


async def upload_image_to_cloud(image_bytes: bytes, slug: str):
    try:
        file_to_upload = BytesIO(image_bytes)
        loop = asyncio.get_event_loop()

        # Gunakan file_to_upload (BytesIO) langsung
        upload_func = partial(
            cloudinary.uploader.upload,
            file_to_upload,  # Posisi pertama biasanya untuk file
            folder="automation-site/articles",
            public_id=slug,
            overwrite=True,
            resource_type="image",
        )

        upload_result = await loop.run_in_executor(None, upload_func)
        return upload_result.get("secure_url")
    except Exception as e:
        print(f"Cloudinary Error : {e}")
        return ""
