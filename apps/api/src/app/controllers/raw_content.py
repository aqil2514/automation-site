from typing import Optional

from fastapi import APIRouter, HTTPException, status

from src.db.tables.raw_contents.select import select_raw_contents
from src.db.tables.raw_contents.insert import insert_new_raw_contents
from src.db.tables.raw_contents.model import RawContent


router = APIRouter(prefix="/contents", tags=["Raw Contents"])


@router.post(
    "/raw_contents",
    status_code=status.HTTP_201_CREATED,
    summary="Membuat Konten Mentah Baru",
    description="Endpoint ini digunakan untuk menyimpan konten mentah hasil scraping ke database PostgreSQL",
    response_description="Pesan sukses jika data berhasil disimpan",
)
async def create_new_raw_contents(payload: RawContent):
    """
    Simpan data konten mentah ke tabel `raw_contents`:

    - **source_url**: URL asal konten
    - **title**: Judul konten
    - **content_raw**: Isi konten dalam format teks mentah/HTML
    - **image_url**: (Opsional) URL gambar utama
    - **status**: Status awal (default: 'pending')
    """
    try:
        await insert_new_raw_contents(payload)
        return {"message": "Data Konten mentah berhasil dibuat"}
    except Exception as e:
        print(f"Detail Error : {e}")
        raise HTTPException(500, detail="Data gagal dibuat")


@router.get(
    "/raw_contents",
    response_model=list[RawContent],
    summary="Mengambil Daftar Konten Mentah",
    description="Mengambil data konten mentah. Bisa difilter berdasarkan status (pending/processing/completed).",
    response_description="Daftar konten mentah yang sesuai kriteria",
)
async def get_raw_contents(
    status_query: Optional[str] = None,
):
    """
    Ambil data dengan opsi filter:

    - **status_query**: (Optional) Filter berdasarkan status data. Contoh: `pending`
    """
    try:
        data = await select_raw_contents(status_filter=status_query)
        return data
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gagal mengambil data",
        )
