from sqlalchemy import Column, String, Integer, ForeignKey, Time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

    ingredients_in_recipe = relationship(
        "IngredientsInRecipes",
        back_populates="ingredient",
        cascade="all, delete-orphan",
        lazy="subquery",
    )

    recipes = association_proxy("ingredients_in_recipe", "recipe")


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cooking_time = Column(Integer, index=True)
    cooking_description = Column(String, index=True)
    views = Column(Integer, default=0)

    ingredients_in_recipe = relationship(
        "IngredientsInRecipes",
        back_populates="recipe",
        cascade="all, delete-orphan",
        lazy="subquery",
    )

    ingredients = association_proxy(
        "ingredients_in_recipe",
        "ingredient",
        creator=lambda ingr: IngredientsInRecipes(ingredient=ingr),
    )


class IngredientsInRecipes(Base):
    __tablename__ = "IngredientsInRecipes"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)

    recipe = relationship(
        "Recipe",
        back_populates="ingredients_in_recipe",
        cascade="save-update",
        lazy="joined",
        innerjoin=True,
    )

    ingredient = relationship(
        "Ingredient",
        back_populates="ingredients_in_recipe",
        cascade="save-update",
        lazy="joined",
        innerjoin=True,
    )
