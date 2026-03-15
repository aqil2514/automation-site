import cloudinary
from src.core.config import config_env


def init_cloudinary():
    cloudinary.config(
        cloud_name=config_env.CLOUDINARY_CLOUD_NAME,
        api_key=config_env.CLOUDINARY_API_KEY,
        api_secret=config_env.CLOUDINARY_API_SECRET,
        secure=True,
    )
