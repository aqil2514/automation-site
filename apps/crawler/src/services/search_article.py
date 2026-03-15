import urllib.parse

import feedparser
import urllib
from googlenewsdecoder import gnewsdecoder

GOOGLE_SEARCH_NEWS_URL = """
https://news.google.com/rss/search?q={keyword}
"""


async def search_article(keywords: list[str], limit: int = 10) -> list[str]:
    all_urls = []
    for keyword in keywords:
        encoded_keyword = urllib.parse.quote(keyword)
        print(f"Mencari berita tentang '{encoded_keyword}'")
        rss_url = GOOGLE_SEARCH_NEWS_URL.format(keyword=encoded_keyword).strip()

        feed = feedparser.parse(rss_url)
        total_news = len(feed.entries[:limit])
        print(f"Ditemukan {total_news} berita")

        for index, entry in enumerate(feed.entries[:limit], 1):
            print(
                f"Memproses artikel tentang {encoded_keyword} ke-{index} dari {total_news} artikel"
            )

            link = entry.link
            decoded_url = gnewsdecoder(link)
            try:
                decoded_url = gnewsdecoder(entry.link)
                if decoded_url.get("status"):
                    all_urls.append(decoded_url.get("decoded_url"))
                else:
                    all_urls.append(entry.link)
            except Exception:
                all_urls.append(entry.link)

    return list(set(all_urls))
