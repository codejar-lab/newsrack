from typing import List

from _recipe_utils import Recipe, onlyon_days, onlyat_hours, onlyon_weekdays

# Define your custom recipes list here
recipes: List[Recipe] = [
    Recipe(
        recipe="frontline",
        slug="frontline",
        src_ext="mobi",
        target_ext=["epub"],
        category="Indian magazines",
    ),
    Recipe(
        recipe="outlook_india",
        slug="outlook_india",
        src_ext="mobi",
        target_ext=["epub"],
        category="Indian magazines",
    ),
    Recipe(
        recipe="india_today",
        slug="india_today",
        src_ext="mobi",
        target_ext=["epub"],
        category="Indian magazines",
    ),
    Recipe(
        recipe="the-hindu",
        slug="the-hindu",
        src_ext="mobi",
        target_ext=["epub"],
        category="news",
    ),
    Recipe(
        recipe="indian-express",
        slug="indian-express",
        src_ext="mobi",
        target_ext=["epub"],
        category="news",
    ),
    Recipe(
        recipe="live-mint",
        slug="live-mint",
        src_ext="mobi",
        target_ext=["epub"],
        category="news",
    ),
    Recipe(
        recipe="business-standard",
        slug="business-standard",
        src_ext="mobi",
        target_ext=["epub"],
        category="news",
    ),
    Recipe(
        recipe="gujarat-samachar",
        slug="gujarat-samachar",
        src_ext="mobi",
        target_ext=["epub"],
        category="Gujarati Newspaper",
    ),
    Recipe(
        recipe="sandesh",
        slug="sandesh",
        src_ext="mobi",
        target_ext=["epub"],
        category="Gujarati Newspaper",
    ),
    Recipe(
        recipe="dte",
        slug="dte",
        src_ext="mobi",
        target_ext=["epub"],
        category="Indian Magazines",
        enable_on=onlyon_days(list(range(15, 31)), -5),  # middle of the month?
    ),

        Recipe(
        recipe="open",
        slug="open",
        src_ext="mobi",
        target_ext=["epub"],
        timeout=180,
        overwrite_cover=True,
        category="Indian Magazines",
    ),
    Recipe(
        recipe="finshots",
        slug="finshots",
        src_ext="mobi",
        target_ext=["epub"],
        category="Newsletters",
    ),
    Recipe(
        recipe="seminar_magazine",
        slug="seminar_magazine",
        src_ext="mobi",
        target_ext=["epub"],
        category="Indian Magazines",
    ),
    Recipe(
        recipe="caravan_magazine",
        slug="caravan_magazine",
        src_ext="mobi",
        target_ext=["epub"],
        category="Indian Magazines",
    ),
    Recipe(
        recipe="live-law",
        slug="live-law",
        src_ext="mobi",
        target_ext=["epub"],
        category="news",
    ),
    Recipe(
        recipe="substack-nl",
        slug="substack-nl",
        src_ext="mobi",
        target_ext=["epub"],
        category="Newsletters",
    ),
    Recipe(
        recipe="daily-current",
        slug="daily-current",
        src_ext="mobi",
        target_ext=["epub"],
        category="UPSC",
    ),
    Recipe(
        recipe="swarajya",
        slug="swarajya",
        src_ext="mobi",
        target_ext=["epub"],
        category="Indian magazines",
    ),
    Recipe(
        recipe="atlantic-magazine",
        slug="atlantic-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="International magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -4)
        and onlyon_days(list(range(32 - 14, 32)), -4),
    ),
    Recipe(
        recipe="thediplomat",
        name="The Diplomat",
        slug="the-diplomat",
        src_ext="mobi",
        target_ext=["epub"],
        category="International magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4, 5], 5.5),
    ),
    Recipe(
        recipe="economist",
        slug="economist",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="International magazines",
        timeout=240,
    ),
    Recipe(
        recipe="hbr",
        slug="hbr",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="International magazines",
        enable_on=onlyon_days(list(range(1, 1 + 7)) + list(range(32 - 7, 32)), -5),
    ),
    Recipe(
        recipe="mit-tech-review",
        slug="mit-tech-review-feed",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4, 5], -4),
    ),
    Recipe(
        recipe="nature",
        slug="nature",
        src_ext="mobi",
        target_ext=["epub"],
        category="International magazines",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([2, 3, 4], 0),
    ),
    Recipe(
        recipe="scientific-american",
        slug="scientific-american",
        src_ext="mobi",
        target_ext=["epub"],
        category="International magazines",
        overwrite_cover=False,
        enable_on=onlyon_days(list(range(15, 31)), -5),  # middle of the month?
    ),
    Recipe(
        recipe="wired",
        slug="wired",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=True,
        category="International magazines",
    ),
    Recipe(
        recipe="time-magazine",
        slug="time-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="International magazines",
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4),
    ),
    Recipe(
        recipe="nautilus",
        slug="nautilus",
        src_ext="mobi",
        target_ext=["epub"],
        category="International magazines",
    ),
]
