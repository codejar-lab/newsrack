# --------------------------------------------------------------------
# This file defines default recipes distributed with newsrack.
# To customise your own instance, do not modify this file.
# Add your recipes to _recipes_custom.py instead and new recipe source
# files to recipes_custom/.
# --------------------------------------------------------------------

from _recipe_utils import Recipe, onlyon_days, onlyat_hours, onlyon_weekdays

# Only mobi work as periodicals on the Kindle
# Notes:
#   - When epub is converted to mobi periodicals:
#       - masthead is lost
#       - mobi retains periodical support but has the non-funtional
#         calibre generated nav, e.g. Next Section, Main, etc
#       - article summary/description is lost
#   - When mobi periodical is converted to epub:
#       - epub loses the calibre generated nav, e.g. Next Section, Main, etc
#         but full toc is retained
#   - Recipe can be defined twice with different src_ext, will work except
#     for potential throttling and time/bandwidth taken

# Keep this list in alphabetical order

recipes = [
"""
    Recipe(
        recipe="asahi-shimbun",
        slug="asahi-shimbun",
        src_ext="mobi",
        target_ext=["epub"],
        category="news",
    ),
    Recipe(
        recipe="asian-review",
        slug="arb",
        src_ext="mobi",
        target_ext=["epub"],
        category="books",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], 8),
    ),
    Recipe(
        recipe="atlantic",
        slug="the-atlantic",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
    ),
    Recipe(
        recipe="atlantic-magazine",
        slug="atlantic-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -4)
        and onlyon_days(list(range(32 - 14, 32)), -4),
    ),
    Recipe(
        recipe="channelnewsasia",
        slug="channelnewsasia",
        src_ext="mobi",
        target_ext=["epub"],
        category="news",
    ),
    Recipe(
        recipe="thediplomat",
        name="The Diplomat",
        slug="the-diplomat",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4, 5], 5.5),
    ),
    Recipe(
        recipe="economist",
        slug="economist",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="magazines",
        timeout=240,
    ),
    Recipe(
        recipe="ft",
        slug="ft",
        src_ext="mobi",
        target_ext=["epub"],
        category="news",
    ),
    Recipe(
        recipe="fivebooks",
        slug="fivebooks",
        src_ext="mobi",
        target_ext=["epub"],
        category="books",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4]),
    ),
    Recipe(
        recipe="guardian",
        slug="guardian",
        src_ext="mobi",
        target_ext=["epub"],
        category="news",
    ),
    Recipe(
        recipe="hbr",
        slug="hbr",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="magazines",
        enable_on=onlyon_days(list(range(1, 1 + 3)) + list(range(32 - 14, 32)), -5),
    ),
    Recipe(
        recipe="joongangdaily",
        slug="joongang-daily",
        src_ext="mobi",
        target_ext=["epub"],
        category="news",
    ),
    Recipe(
        recipe="korea-herald",
        slug="korea-herald",
        src_ext="mobi",
        target_ext=["epub"],
        category="news",
    ),
    Recipe(
        recipe="london-review",
        slug="lrb",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="books",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4]),
    ),
    Recipe(
        recipe="mit-press-reader",
        slug="mit-press-reader",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -4),
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
        recipe="mit-tech-review-magazine",
        slug="mit-tech-review-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
        overwrite_cover=False,
        enable_on=onlyon_days(list(range(1, 1 + 7)) + list(range(32 - 7, 32)), -5),
    ),
    Recipe(
        recipe="nature",
        slug="nature",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([2, 3, 4], 0),
    ),
    Recipe(
        recipe="nautilus",
        slug="nautilus",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
    ),
    Recipe(
        recipe="newyorker",
        slug="newyorker",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -5),
    ),
    Recipe(
        recipe="nytimes-global",
        slug="nytimes-global",
        src_ext="mobi",
        target_ext=["epub"],
        category="news",
    ),
    Recipe(
        recipe="nytimes-paper",
        slug="nytimes-print",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="news",
        enable_on=onlyat_hours(list(range(20, 24)) + list(range(0, 4))),
    ),
    Recipe(
        recipe="nytimes-books",
        slug="nytimes-books",
        src_ext="mobi",
        target_ext=["epub"],
        category="books",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -5),
    ),
    Recipe(
        recipe="poetry",
        slug="poetry-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="magazines",
        enable_on=onlyon_days(list(range(1, 1 + 7)) + list(range(32 - 7, 32)), -5),
    ),
    Recipe(
        recipe="propublica",
        slug="propublica",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
    ),
    Recipe(
        recipe="politico-magazine",
        slug="politico-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4, 5], -5),
    ),
    Recipe(
        recipe="restofworld",
        slug="restofworld",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4, 5])
        and onlyat_hours(list(range(9, 19))),
    ),
    Recipe(
        recipe="scientific-american",
        slug="scientific-american",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
        overwrite_cover=False,
        enable_on=onlyon_days(list(range(15, 31)), -5),  # middle of the month?
    ),
    Recipe(
        recipe="scmp",
        slug="scmp",
        src_ext="mobi",
        target_ext=["epub"],
        category="news",
    ),
    Recipe(
        recipe="sydney-morning-herald",
        slug="sydney-morning-herald",
        src_ext="mobi",
        target_ext=["epub"],
        category="news",
    ),
    Recipe(
        recipe="taipei-times",
        slug="taipei-times",
        src_ext="mobi",
        target_ext=["epub"],
        timeout=600,
        category="news",
        enable_on=onlyat_hours(list(range(6, 14)), 8),
    ),
    Recipe(
        recipe="thirdpole",
        slug="thirdpole",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
        enable_on=onlyat_hours(list(range(5, 20)), 5.5),
    ),
    Recipe(
        recipe="time-magazine",
        slug="time-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="magazines",
        enable_on=onlyon_weekdays([3, 4, 5, 6], -4),
    ),
    Recipe(
        recipe="vox",
        slug="vox",
        src_ext="mobi",
        target_ext=["epub"],
        category="magazines",
    ),
    Recipe(
        recipe="wapo",
        slug="wapo",
        src_ext="mobi",
        target_ext=["epub"],
        timeout=600,
        category="news",
    ),
    Recipe(
        recipe="wired",
        slug="wired",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=True,
        category="magazines",
    ),
"""
]
