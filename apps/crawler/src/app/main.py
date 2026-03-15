import asyncio
import json  # Tambahkan ini jika ingin simpan ke file
from src.services.get_trending_keywords import get_automated_keywords
from src.services.get_article import get_article
from src.services.search_article import search_article


async def main():
    trending_topics = get_automated_keywords(limit=5)
    print(f"Topik tren hari ini di Indonesia: {trending_topics}")

    # 1. Cari link (limit 10 per keyword seperti yang kita buat tadi)
    found_links = await search_article(trending_topics, 3)

    all_articles_data = []

    print(f"\nMemulai proses scraping untuk {len(found_links)} artikel...")

    # 2. Loop semua link yang ditemukan
    for index, link in enumerate(found_links, 1):
        try:
            print(f"[{index}/{len(found_links)}] Mengambil konten: {link[:60]}...")

            # Panggil fungsi get_article Anda
            article_data = await get_article(link)

            # VALIDASI: Simpan hanya jika ada isinya
            if article_data.status == "success" and len(article_data.content) > 150:
                all_articles_data.append(article_data)
                print(f"✅ Sukses: {article_data.title[:50]}...")
            else:
                # Jika kosong, mungkin ini halaman video/galeri, kita skip saja
                print(f"⚠️ Skip: Konten terlalu pendek/kosong ({link[:40]}...)")

        except Exception as e:
            print(f"Gagal mengambil {link}: {e}")

    # 4. Hasil akhir
    print(f"\nSelesai! Berhasil mengumpulkan {len(all_articles_data)} artikel.")

    # Konversi list of ArticleSchema menjadi list of dict
    json_ready_data = [article.model_dump() for article in all_articles_data]

    # Simpan ke JSON
    with open("articles_result.json", "w", encoding="utf-8") as f:
        json.dump(json_ready_data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    asyncio.run(main())
