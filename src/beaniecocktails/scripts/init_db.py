from asyncio import run
from pathlib import Path

from beaniecocktails import Settings
from beaniecocktails.models import Cocktail

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from random import randint

COCKTAIL_NAMES = [
    "Sour Cherry",
    "Spicy Mango Mule",
    "Blue Hawaiian",
    "Gin Fizz",
    "Classic Daiquiri",
    "Pomegranate Martini",
    "Southern Belle",
    "French 75",
    "Espresso Con Panna",
    "Smoky Sour",
    "Cucumber Gimlet",
    "Dark 'N' Stormy",
    "Basil Gimlet",
    "Spiked Apple Cider",
    "Pear-fect Punch",
    "Black Russian",
    "Sakura Spritz",
    "Classic Gin and Tonic",
    "Irish Mule",
    "Whiskey Smash",
    "Lemon Drop",
    "French Connection",
    "Tequila Sunrise",
    "Pimm's Cup",
    "Vieux Carré",
    "Grapefruit Basil Martini",
    "Hemingway Daiquiri",
    "Old Fashioned",
    "Julep",
    "Cognac Old Fashioned",
    "Tom Collins",
    "Sloe Gin Fizz",
    "Shirley Temple",
    "Bourbon Street",
    "Caipirinha",
    "Penicillin",
    "Corpse Reviver #2",
    "Blood and Sand",
    "El Diablo",
    "Scorpion's Tail",
    "Golden Bee",
    "Blue Lagoon",
    "Lillet Spritz",
    "Hemingway Special",
    "Cucumber Collins",
    "Classic Mojito",
    "Peach Bellini",
    "Blackberry Bourbon Smash",
    "Green Fairy",
    "Whiskey Sour",
    "Tequila Sunrise (Frozen)",
    "Midnight Express",
    "French 75 (French Connection)",
    "Champagne Cocktail",
    "Sloe Gin Fizz",
    "Cucumber Gimlet",
    "Smoky Sour",
    "Irish Coffee",
    "Blood and Sand",
    "Corpse Reviver #2",
    "Penicillin",
    "El Diablo",
    "Black Russian",
    "Tequila Sunrise (Regular)",
    "Spiked Apple Cider",
    "Whiskey Smash",
    "Sour Cherry",
    "Julep",
    "French Connection",
    "Shirley Temple",
    "Hemingway Daiquiri",
    "Basil Gimlet",
    "Dark 'N' Stormy",
    "Tequila Sunrise (Frozen)",
    "Pimm's Cup",
    "Southern Belle",
    "Lillet Spritz",
    "Midnight Express",
    "Whiskey Sour",
    "Green Fairy",
    "Old Fashioned",
    "Blackberry Bourbon Smash",
    "Penicillin",
    "Sloe Gin Fizz",
    "Bourbon Street",
    "Tequila Sunrise (Regular)",
    "Irish Coffee",
    "Corpse Reviver #2",
    "Blood and Sand",
    "Cognac Old Fashioned",
    "Scorpion's Tail",
    "Hemingway Special",
    "French 75",
]


def main():
    run(amain())


async def amain():
    client: AsyncIOMotorClient = AsyncIOMotorClient(
        Settings().mongodb_url,
        connectTimeoutMS=1000,
        socketTimeoutMS=1000,
        serverSelectionTimeoutMS=1000,
    )
    await init_beanie(client.get_default_database(), document_models=[Cocktail])
    json = Path("sample_data/hunters_moon.json").read_text()
    for name in COCKTAIL_NAMES:
        template_cocktail = Cocktail.model_validate_json(json)
        print("Input:", template_cocktail.id)
        template_cocktail.name = name
        for _ in range(randint(0, 3)):
            del template_cocktail.ingredients[
                randint(0, len(template_cocktail.ingredients) - 1)
            ]
        await template_cocktail.save()
        print(f"Saved {name}")
