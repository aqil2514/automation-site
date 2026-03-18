from src.services.get_article import get_article
from src.services.search_article import search_article
from src.db.tables.raw_contents.insert import insert_new_raw_contents
from src.services.get_trending_keywords import get_automated_keywords


async def run_generate_raw_article():
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
            if article_data.status == "pending" and len(article_data.content_raw) > 150:
                all_articles_data.append(article_data)
                print(f"✅ Sukses: {article_data.title[:50]}...")
            else:
                # Jika kosong, mungkin ini halaman video/galeri, kita skip saja
                print(f"⚠️ Skip: Konten terlalu pendek/kosong ({link[:40]}...)")

        except Exception as e:
            print(f"Gagal mengambil {link}: {e}")

    # 3. Hasil akhir
    print(f"\nSelesai! Berhasil mengumpulkan {len(all_articles_data)} artikel.")

    if all_articles_data:
        await insert_new_raw_contents(all_articles_data)
    else:
        print("Tidak ada artikel yang layak untuk dimasukkan ke database.")
