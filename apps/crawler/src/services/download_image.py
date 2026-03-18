import asyncio
from datetime import datetime
import os

import httpx


# async def download_image(url: str, save_path: str):
async def download_image(url: str):
    now = datetime.now()

    file_name = f"img-{now.strftime('%Y%m')}.png"

    save_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name)

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return save_path
        return None


if __name__ == "__main__":
    asyncio.run(
        download_image(
            "https://res.cloudinary.com/dwcr3rpgi/image/upload/v1773801182/automation-site/articles/ribuan-motor-padati-jogja-sinyal-mudik-lebaran-2026-lebih-cepat.png"
        )
    )
