from typing import List

from _recipe_utils import Recipe

# Define your custom recipes list here
recipes: List[Recipe] = [
    Recipe(
        recipe="frontline",
        slug="frontline",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
    ),
    Recipe(
        recipe="outlook_india",
        slug="outlook_india",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
    ),
    Recipe(
        recipe="india_today",
        slug="india_today",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
    ),
]
