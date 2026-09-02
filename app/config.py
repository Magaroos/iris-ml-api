from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODEL_PATH: str
    API_TITLE: str
    MAX_BATCH_SIZE: int
    LOG_LEVEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()
print("Loaded MODEL_PATH:", Settings().MODEL_PATH)