"""
init-db - A crude script to generate some sample cocktail data.

(This must be run from the project root,
otherwise it won't be able to load seed cocktail file, "hunters_moon.json")
"""

from argparse import ArgumentParser
import asyncio
from pathlib import Path
from random import randint
import sys

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from tqdm import tqdm

from beaniecocktails import Settings
from beaniecocktails.models import Cocktail

COCKTAIL_NAMES = [
    "Basil Gimlet",
    "Black Russian",
    "Blackberry Bourbon Smash",
    "Blood and Sand",
    "Blue Hawaiian",
    "Blue Lagoon",
    "Bourbon Street",
    "Caipirinha",
    "Champagne Cocktail",
    "Classic Daiquiri",
    "Classic Gin and Tonic",
    "Classic Mojito",
    "Cognac Old Fashioned",
    "Corpse Reviver #2",
    "Cucumber Collins",
    "Cucumber Gimlet",
    "Dark 'N' Stormy",
    "El Diablo",
    "Espresso Con Panna",
    "French 75",
    "French Connection",
    "Gin Fizz",
    "Golden Bee",
    "Grapefruit Basil Martini",
    "Green Fairy",
    "Hemingway Daiquiri",
    "Hemingway Special",
    "Irish Coffee",
    "Irish Mule",
    "Julep",
    "Lemon Drop",
    "Lillet Spritz",
    "Midnight Express",
    "Old Fashioned",
    "Peach Bellini",
    "Pear-fect Punch",
    "Penicillin",
    "Pimm's Cup",
    "Pomegranate Martini",
    "Sakura Spritz",
    "Scorpion's Tail",
    "Shirley Temple",
    "Sloe Gin Fizz",
    "Smoky Sour",
    "Sour Cherry",
    "Southern Belle",
    "Spicy Mango Mule",
    "Spiked Apple Cider",
    "Tequila Sunrise (Frozen)",
    "Tequila Sunrise (Regular)",
    "Tom Collins",
    "Vieux Carré",
    "Whiskey Smash",
    "Whiskey Sour",
]


def main(argv=sys.argv[1:]):
    arg_parser = ArgumentParser(description=__doc__)
    arg_parser.add_argument(
        "-C", "--clear-collection", action="store_true", default=False
    )
    arg_parser.add_argument("-d", "--dummy-data", action="store_true")

    args = arg_parser.parse_args(argv)
    asyncio.run(
        amain(clear_collection=args.clear_collection, create_dummy_data=args.dummy_data)
    )


async def amain(clear_collection=False, create_dummy_data=True):
    client: AsyncIOMotorClient = AsyncIOMotorClient(
        Settings().mongodb_url,
        connectTimeoutMS=1000,
        socketTimeoutMS=1000,
        serverSelectionTimeoutMS=1000,
    )
    db = client.get_default_database()
    await init_beanie(db, document_models=[Cocktail])

    if clear_collection:
        print("Delete existing cocktails.")
        await Cocktail.delete_all()

    # Create the autocomplete index if necessary:
    recipes = Cocktail.get_motor_collection()
    if not await recipes.list_search_indexes("autocomplete_name").to_list(length=1):
        print("Create autocomplete index on 'name' field ...")
        await db.create_collection(recipes.name)
        await recipes.create_search_index(
            {
                "definition": {
                    "mappings": {
                        "dynamic": False,
                        "fields": {"name": {"type": "autocomplete"}},
                    }
                },
                "name": "autocomplete_name",
            }
        )
    else:
        print("Autocomplete index already exists on 'name' field.")

    if create_dummy_data:
        print("Create dummy cocktail data.")
        json = Path("sample_data/hunters_moon.json").read_text()

        progress = tqdm(COCKTAIL_NAMES, desc="Loading Cocktails")
        for name in progress:
            # Load the seed cocktail:
            template_cocktail = Cocktail.model_validate_json(json)
            # Rename it to the current cocktail name:
            template_cocktail.name = name
            # Now remove between 0-3 ingredients, so the cocktails aren't all identical:
            for _ in range(randint(0, 3)):
                del template_cocktail.ingredients[
                    randint(0, len(template_cocktail.ingredients) - 1)
                ]
            # Finally, save the cocktail:
            await template_cocktail.save()
            progress.write(name)
