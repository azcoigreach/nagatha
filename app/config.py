# config settings with pydantic and .env file
from pydantic import BaseSettings

class Settings(BaseSettings):
    API_KEY: str
    GAME_ID: str
    SERVER_ID: int
    DISCORD_TOKEN: str
    GUILD_ID: int

    SYSTEM_ADMIN_IDS: list[int] = []
    
    class Config:
        env_file = ".env"

settings = Settings()
