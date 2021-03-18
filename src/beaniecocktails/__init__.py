"""
beaniecocktails - A cocktail API built with MongoDB and Beanie
"""


import motor
from beanie.general import init_beanie
from fastapi import FastAPI
from pydantic import BaseSettings

from .models import Cocktail
from .routes import cocktail_router

app = FastAPI()


class Settings(BaseSettings):
    mongodb_url = "mongodb://localhost:27017/cocktails"


@app.on_event("startup")
async def app_init():
    client = motor.motor_asyncio.AsyncIOMotorClient(Settings().mongodb_url)
    init_beanie(client.get_default_database(), document_models=[Cocktail])
    app.include_router(cocktail_router, prefix="/v1")