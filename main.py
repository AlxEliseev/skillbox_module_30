from typing import List, Annotated

from fastapi import FastAPI, Path, HTTPException
# from sqlalchemy.future import select
from sqlalchemy import select, update
from contextlib import asynccontextmanager
from models import IngredientsInRecipes
import models
import schemas
from database import engine, session

@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app starts
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    # after app finishes
    await session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post('/recipes/', response_model=schemas.RecipeOutDetailed,
          summary='Add new recipe',
          description='Adds new recipe with ingredients got by id')
async def recipes(recipe: schemas.RecipeIn) -> models.Recipe:
    recipe = recipe.dict()

    ingredients = []
    for ingredient_id in recipe.pop('ingredients'):
        ingredient = await session.execute(select(models.Ingredient).where(models.Ingredient.id==ingredient_id))
        ingredient = ingredient.scalar()
        if ingredient:
            ingredients.append(ingredient)
        else:
            raise HTTPException(400, f'No ingredient with id # {ingredient_id}. Create ingredient first')

    new_recipe = models.Recipe(**recipe)
    session.add(new_recipe)

    for ingr in ingredients:
        # new_recipe.ingredients_in_recipe.append(IngredientsInRecipes(ingredient=ingr))
        new_recipe.ingredients.append(ingr)

    await session.commit()
    return new_recipe


@app.get('/recipes/', response_model=List[schemas.RecipeOutShort],
         summary='The list af all recipes',
         description='Shows the list af all recipes'
         )
async def get_recipes() -> List[models.Recipe]:
    res = await session.execute(select(models.Recipe).
                                order_by(models.Recipe.views.desc(),
                                models.Recipe.cooking_time.desc())
                                )
    return res.scalars().all()


@app.get('/recipes/{recipe_id}', response_model=schemas.RecipeOutDetailed,
         summary='Recipe information',
         description='Shows detailed recipe information by recipe_id'
         )
async def get_recipe(recipe_id: Annotated[int, Path(ge=0)]) -> List[models.Recipe]:
    res = await session.execute(select(models.Recipe).where(models.Recipe.id == recipe_id))
    result = res.scalar()
    if result:
        await session.execute(update(models.Recipe).
                              where(models.Recipe.id == recipe_id).
                              values(views = models.Recipe.views + 1))
        await session.commit()
        return result
    else:
        raise HTTPException(400, 'No result found')
