from typing import List
from aiohttp import payload_type

from fastapi import Depends, FastAPI, Response, status
from fastapi.responses import JSONResponse
from fastapi_discord import DiscordOAuthClient, RateLimited, Unauthorized, User
from fastapi_discord.models import GuildPreview

from .config import settings

app = FastAPI()

discord = DiscordOAuthClient(
    settings.client_id, settings.client_secret, settings.redirect_uri, ("bot")
)  # scopes

@app.get("/")
async def root():
    return {"message": "Nagatha Discord Bot"}

@app.get("/login")
async def login():
    return {"url": discord.oauth_login_url}


@app.get("/callback")
async def callback(code: str):
    token, refresh_token = await discord.get_access_token(code)
    return {"access_token": token, "refresh_token": refresh_token}


@app.get(
    "/authenticated",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=bool,
)
async def isAuthenticated(token: str = Depends(discord.get_token)):
    try:
        auth = await discord.isAuthenticated(token)
        return auth
    except Unauthorized:
        return False


@app.exception_handler(Unauthorized)
async def unauthorized_error_handler(_, __):
    return JSONResponse({"error": "Unauthorized"}, status_code=401)


@app.exception_handler(RateLimited)
async def rate_limit_error_handler(_, e: RateLimited):
    return JSONResponse(
        {"error": "RateLimited", "retry": e.retry_after, "message": e.message},
        status_code=429,
    )


@app.get("/user", dependencies=[Depends(discord.requires_authorization)], response_model=User)
async def get_user(user: User = Depends(discord.user)):
    return user


@app.get(
    "/guilds",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=List[GuildPreview],
)
async def get_guilds(guilds: List = Depends(discord.guilds)):
    return guilds


@app.post("/commands")
async def commands():
    payload = f"{"type": 1}"
    return Response(payload, status_code=status.HTTP_200_OK)