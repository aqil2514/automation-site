from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRE_CONNECT_URL: str = ""
    KOMPASIANA_EMAIL: str = ""
    KOMPASIANA_PASSWORD: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


config_env = Settings()
