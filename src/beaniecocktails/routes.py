from typing import List

from fastapi import APIRouter, HTTPException, Depends
from beanie import PydanticObjectId

from .models import Cocktail, IngredientAggregation

cocktail_router = APIRouter()


async def get_cocktail(cocktail_id: PydanticObjectId) -> Cocktail:
    """ Helper function to look up a cocktail by id """

    cocktail = await Cocktail.get(cocktail_id)
    if cocktail is None:
        raise HTTPException(status_code=404, detail="Cocktail not found")
    return cocktail


@cocktail_router.get("/cocktails/{cocktail_id}", response_model=Cocktail)
async def get_cocktail_by_id(cocktail: Cocktail = Depends(get_cocktail)):
    return cocktail


@cocktail_router.get("/cocktails/", response_model=List[Cocktail])
async def list_cocktails():
    return await Cocktail.find_all().to_list()


@cocktail_router.post("/cocktails/", response_model=Cocktail)
async def create_cocktail(cocktail: Cocktail):
    return await cocktail.create()


@cocktail_router.get("/ingredients", response_model=List[IngredientAggregation])
async def list_ingredients():
    """ Group on each ingredient name and return a list of `IngredientAggregation`s. """

    return await Cocktail.aggregate(
        aggregation_pipeline=[
            {"$unwind": "$ingredients"},
            {"$group": {"_id": "$ingredients.name", "total": {"$sum": 1}}},
            {"$sort": {"_id": 1}},
        ],
        projection_model=IngredientAggregation,
    ).to_list()


@cocktail_router.get("/cocktail_autocomplete", response_model=List[str])
async def cocktail_autocomplete(fragment: str):
    """ Return an array of cocktail names matched from a string fragment. """

    return [
        c["name"]
        for c in await Cocktail.aggregate(
            aggregation_pipeline=[
                {
                    "$search": {
                        "autocomplete": {
                            "query": fragment,
                            "path": "name",
                        }
                    }
                }
            ]
        ).to_list()
    ]
