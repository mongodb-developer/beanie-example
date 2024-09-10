"""
beaniecocktails - A cocktail API built with MongoDB and Beanie
"""


from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi import FastAPI
from pydantic_settings import BaseSettings

from .models import Cocktail
from .routes import cocktail_router


async def app_lifespan(app: FastAPI):
    # startup code goes here:
    client: AsyncIOMotorClient = AsyncIOMotorClient(
        Settings().mongodb_url,
        connectTimeoutMS=1000,
        socketTimeoutMS=1000,
        serverSelectionTimeoutMS=1000,
    )
    await init_beanie(client.get_default_database(), document_models=[Cocktail])
    app.include_router(cocktail_router, prefix="/v1")

    yield

    # shutdown code goes here:
    client.close()


app = FastAPI(lifespan=app_lifespan)


class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017/cocktails"
