from typing import Optional, List

from beanie import Document
from pydantic import BaseModel, Field


class Cocktail(Document):
    class DocumentMeta:
        collection_name = "recipes"

    name: str
    ingredients: List["Ingredient"]


class Ingredient(BaseModel):
    name: str
    quantity: Optional["IngredientQuantity"]


class IngredientQuantity(BaseModel):
    quantity: Optional[str]
    unit: Optional[str]


class IngredientAggregation(BaseModel):
    id: str = Field(None, alias="_id")
    total: int


Cocktail.update_forward_refs()
Ingredient.update_forward_refs()