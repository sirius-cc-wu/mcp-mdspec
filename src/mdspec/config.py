from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    specs_dir: str = Field(
        default="specs",
        description="The directory where the specs are stored. This can be set using the SPECS_DIR environment variable.",
    )

settings = Settings()
