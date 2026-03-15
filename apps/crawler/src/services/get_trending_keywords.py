import feedparser
import requests


def get_automated_keywords(limit: int = 5):
    # RSS Headline Utama Google News Indonesia
    url = "https://news.google.com/rss?hl=id&gl=ID&ceid=ID:id"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        feed = feedparser.parse(response.text)

        keywords = []
        for entry in feed.entries[:limit]:
            # Kita ambil judul berita utama, lalu bersihkan
            # Contoh: "Harga Emas Antam Hari Ini Naik" -> diambil "Harga Emas Antam"
            full_title = entry.title.split(" - ")[0]  # type: ignore # Buang nama media di belakang
            clean_keyword = " ".join(full_title.split()[:3])  # Ambil 3 kata pertama
            keywords.append(clean_keyword)

        return list(set(keywords))
    except Exception as e:
        print(f"Gagal ambil trending: {e}")
        return ["Berita Terkini", "Ekonomi Indonesia"]
