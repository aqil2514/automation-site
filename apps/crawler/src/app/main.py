import asyncio
import time

import schedule

from .tasks import run_generate_raw_article, write_processed_article


def generate_article():
    print("====== Memulai Tugas Generate Artikel")
    asyncio.run(run_generate_raw_article())
    print("======Tugas telah selesai")


def write_article():
    print("====== Memulai Tugas Generate Artikel")
    asyncio.run(write_processed_article())
    print("======Tugas telah selesai")


schedule.every(30).minutes.do(generate_article)
schedule.every(5).seconds.do(write_article)


if __name__ == "__main__":
    print("Schedule App is Running")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Schedule dimatikan manual")
