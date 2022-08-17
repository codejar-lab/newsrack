from typing import List

from _recipe_utils import Recipe, onlyon_days, onlyat_hours, onlyon_weekdays

# Define your custom recipes list here
recipes: List[Recipe] = [
    # Recipe(
    #     recipe="frontline",
    #     slug="frontline",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="magazines",
    # ),
    # Recipe(
    #     recipe="outlook_india",
    #     slug="outlook_india",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="magazines",
    # ),
    # Recipe(
    #     recipe="india_today",
    #     slug="india_today",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="magazines",
    # ),
    # Recipe(
    #     recipe="the-hindu",
    #     slug="the-hindu",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="news",
    # ),
    # Recipe(
    #     recipe="indian-express",
    #     slug="indian-express",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="news",
    # ),
    # Recipe(
    #     recipe="live-mint",
    #     slug="live-mint",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="news",
    # ),
    # Recipe(
    #     recipe="business-standard",
    #     slug="business-standard",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="news",
    # ),
    Recipe(
        recipe="gujarat-samachar",
        slug="gujarat-samachar",
        src_ext="azw3",
        category="Gujarati Newspaper",
    ),
    Recipe(
        recipe="sandesh",
        slug="sandesh",
        src_ext="azw3",
        category="Gujarati Newspaper",
    ),
    # Recipe(
    #     recipe="dte",
    #     slug="dte",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="Indian Magazines",
    #     enable_on=onlyon_days(list(range(15, 31)), -5),  # middle of the month?
    # ),

    #     Recipe(
    #     recipe="open",
    #     slug="open",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     timeout=180,
    #     overwrite_cover=True,
    #     category="Indian Magazines",
    # ),
    # Recipe(
    #     recipe="finshots",
    #     slug="finshots",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="Newsletters",
    # ),
    # Recipe(
    #     recipe="seminar_magazine",
    #     slug="seminar_magazine",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="Indian Magazines",
    # ),
    # Recipe(
    #     recipe="caravan_magazine",
    #     slug="caravan_magazine",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="Indian Magazines",
    # ),
    # Recipe(
    #     recipe="live-law",
    #     slug="live-law",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="news",
    # ),
    # Recipe(
    #     recipe="substack-nl",
    #     slug="substack-nl",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="Newsletters",
    # ),
    # Recipe(
    #     recipe="daily-current",
    #     slug="daily-current",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="UPSC",
    # ),
    # Recipe(
    #     recipe="swarajya",
    #     slug="swarajya",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="magazines",
    # ),
]
