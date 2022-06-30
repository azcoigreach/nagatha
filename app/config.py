from pydantic import BaseSettings

class Settings(BaseSettings):
    client_id: str
    client_secret: str
    redirect_uri: str

    class Config:
        env_file = ".env"

settings = Settings()