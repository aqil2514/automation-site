import asyncio
import json  # Tambahkan ini jika ingin simpan ke file
from src.services.get_article import get_article
from src.services.search_article import search_article


async def main():
    keywords = ["Iran", "Spanyol"]

    # 1. Cari link (limit 10 per keyword seperti yang kita buat tadi)
    found_links = await search_article(keywords, 3)

    all_articles_data = []

    print(f"\nMemulai proses scraping untuk {len(found_links)} artikel...")

    # 2. Loop semua link yang ditemukan
    for index, link in enumerate(found_links, 1):
        try:
            print(f"[{index}/{len(found_links)}] Mengambil konten: {link[:60]}...")

            # Panggil fungsi get_article Anda
            article_obj = await get_article(link)

            # 3. Mapping hasil ke dictionary agar rapi
            article_data = {
                "title": article_obj.title,
                "content": article_obj.content,
                "authors": article_obj.authors,
                "top_image": article_obj.top_image,
                "url": link,
            }

            all_articles_data.append(article_data)

        except Exception as e:
            print(f"Gagal mengambil {link}: {e}")

    # 4. Hasil akhir (siap dikirim ke frontend atau database)
    print(f"\nSelesai! Berhasil mengumpulkan {len(all_articles_data)} artikel.")

    # Contoh cetak satu judul artikel pertama
    if all_articles_data:
        print(f"Judul artikel pertama: {all_articles_data[0]['title']}")

    # OPSIONAL: Simpan ke JSON agar bisa dibaca Next.js
    with open("articles_result.json", "w", encoding="utf-8") as f:
        json.dump(all_articles_data, f, indent=4)


if __name__ == "__main__":
    asyncio.run(main())
