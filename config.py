from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    notes_dir: str = "notes"

settings = Settings()
