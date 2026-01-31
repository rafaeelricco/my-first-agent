from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_key: str = Field(default=..., description="API key for the LLM provider")

    model_id: str = Field(default="gemini-3-flash-preview", description="Model identifier")

    telegram_token: str = Field(
        default=..., description="Telegram Bot API token from BotFather"
    )
    telegram_chat_id: str = Field(
        default=..., description="Telegram chat ID to send messages to"
    )


settings = Settings()
