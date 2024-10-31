from functools import cached_property
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="DB__",
        env_file="../.env",
        extra="ignore",
    )
    HOST: str
    PORT: str
    NAME: str
    USER: str
    PASS: str
    DB_POOL_SIZE: int
    DB_MAX_OVERFLOW: int
    DB_URL: str

    @cached_property
    def db_settings(self):
        return self

    @cached_property
    def dsn_async(self):
        return (
            f"postgresql+asyncpg://{self.USER}:{self.PASS}"
            f"@{self.HOST}:{self.PORT}/{self.NAME}"
        )

    @cached_property
    def dsn_sync(self):
        return (
            f"postgresql+psycopg2://{self.USER}:{self.PASS}"
            f"@{self.HOST}:{self.PORT}/{self.NAME}"
        )

    @cached_property
    def db_to_script(self):
        return (
            f"postgresql://{self.USER}:{self.PASS}"
            f"@{self.HOST}:{self.PORT}/{self.NAME}"
        )


class TestDBSettings(BaseSettings):
    NAME: str = "test_db.db"
    USER: str = ""
    PASS: str = ""

    @computed_field(return_type=str)
    def dsn_async(self):
        return f"sqlite+aiosqlite:///{self.NAME}"

    @computed_field(return_type=str)
    def dsn_sync(self):
        return f"sqlite:///{self.NAME}"


db_settings = DBSettings()
test_db_settings = TestDBSettings()
