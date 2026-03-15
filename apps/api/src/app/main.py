from fastapi import FastAPI
from src.services.cloudinary.connection import init_cloudinary
from src.app.controllers.raw_content import router as raw_content_router
from src.app.controllers.article import router as article_router

app = FastAPI(
    title="Automation Site API",
    description="API untuk mengelola konten mentah hasil scraping",
    version="1.0.0",
)

init_cloudinary()


@app.get("/")
def read_root():
    return {"status": "success"}


app.include_router(raw_content_router)
app.include_router(article_router)
