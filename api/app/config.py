from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    UPLOAD_DIR: str = "/data/uploads"
    OUTPUT_DIR: str = "/data/output"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
