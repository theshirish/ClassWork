from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = Field(default="development", description="Environment")
    open_ai_api_key: str = Field(description="OpenAI API Key")
    open_ai_base_url: str = Field(description="OpenAI Base URL")
    open_ai_temperature: float = Field(description="OpenAI Temperature")
    open_ai_retries: int = Field(description="OpenAI Retries")
    open_ai_timeout: int = Field(description="OpenAI Timeout")
    # name_min_length: int = Field(description="Minimum length for user name")
    # name_max_length: int = Field(description="Maximum length for user name")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


my_settings = Settings()

# my_settings = Settings(env=".env", open_ai_api_key="",
#                        open_ai_base_url="", open_ai_temperature=0.2, open_ai_retries=3, open_ai_timeout=60)
