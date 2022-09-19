# config settings with pydantic and .env file
from pydantic import BaseSettings

class Settings(BaseSettings):
    API_KEY: str
    GAME_ID: str
    SERVER_ID: int
    DISCORD_TOKEN: str
    GUILD_ID: int

    REGISTERED_GUILD_IDS: list[int] = []

    SYSTEM_ADMIN_IDS: list[int] = []
    SYSTEM_ADMIN_GUILD_IDS: list[int] = []

    BATTLEMETRICS_GUILD_IDS: list[int] = []

    CRYPTO_GUILD_IDS: list[int] = []

    YOUTUBE_GUILD_IDS: list[int] = []

    BETHESDA_GUILD_IDS: list[int] = []

    STEAM_GUILD_IDS: list[int] = []

    class Config:
        env_file = ".env"

settings = Settings()