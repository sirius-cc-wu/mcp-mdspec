from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    notes_dir: str = Field(
        default="notes",
        description="The directory where the notes are stored. This can be set using the NOTES_DIR environment variable.",
    )

settings = Settings()
