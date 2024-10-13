# pyright: reportMissingImports=false, reportUnknownVariableType=false, reportUntypedBaseClass=false

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    db_name: str = "main.db"
    password: str = ""


settings = Settings()
