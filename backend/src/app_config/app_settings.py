from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        env_prefix="BACKEND_SERVER__",
    )
    PORT: int
    HOST: str
    WORKERS: int
    DEBUG: bool
    SECRET_KEY: str
    SAVE_PATH: str
    METHODS: List[str]
    HEADERS: List[str]
    ALGORITHM: str
    origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:3300",
        "http://127.0.0.1:3000",
        "https://localhost:3000",
        "https://localhost:3300",
        "https://127.0.0.1:3000",
        "http://localhost:10888",
        "http://127.0.0.1:10888",
    ]

    @property
    def app_settings(self):
        return self

    @computed_field(return_type=str)
    @property
    def server_url(self) -> str:
        return f"http://{self.PORT}:{self.PORT}"


app_settings = AppSettings()
