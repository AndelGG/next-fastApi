from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "app_"

    MONGO_URI: str
    MONGO_DB: str


settings = AppSettings()  # type: ignore[call-arg]
