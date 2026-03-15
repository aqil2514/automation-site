import os
from google import genai
from src.core.config import config_env

# 1. Pastikan OS mengenali path kredensial
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config_env.GOOGLE_APPLICATION_CREDENTIALS

vertex_client = genai.Client(
    vertexai=True,
    # PASTIKAN INI ID PROJECT (Contoh: 'automation-489502'), BUKAN PATH JSON
    project=config_env.GOOGLE_CLOUD_PROJECT_ID,
    location=config_env.GOOGLE_CLOUD_LOCATION,
)
