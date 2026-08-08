from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = Field(default="development", description="Environment")
    openai_api_key: str = Field(description="OpenAI API Key")
    open_ai_base_url: str = Field(description="OpenAI Base URL")
    name_min_length: int = Field(description="Minimum length for user name")
    name_max_length: int = Field(description="Maximum length for user name")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


my_settings = Settings(env=".env", openai_api_key="",
                       open_ai_base_url="", name_min_length=2, name_max_length=100)
