from pydantic import BaseModel, Field
from typing import List


class BaseIngredient(BaseModel):
    name: str = Field(description="Ingredient name")
    description: str = Field(description="Ingredient description")


class IngredientIn(BaseIngredient): ...


class IngredientOut(BaseIngredient):
    id: int = Field(description="Ingredient id")

    class Config:
        orm_mode = True


class BaseRecipe(BaseModel):
    name: str = Field(description="Recipe name")
    cooking_description: str = Field(description="Detailed recipe cooking description")
    cooking_time: int = Field(description="Cooking time in minutes")


class RecipeIn(BaseRecipe):
    ingredients: List[int] = Field(description="Ingredients id list")


class RecipeOutDetailed(BaseRecipe):
    id: int = Field(description="Recipe id")
    ingredients: List[IngredientOut] = Field(description="Ingredients list")

    class Config:
        orm_mode = True


class RecipeOutShort(BaseRecipe):
    views: int = Field(description="Recipe views count")

    class Config:
        orm_mode = True
