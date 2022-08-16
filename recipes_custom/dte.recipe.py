from calibre.web.feeds.news import BasicNewsRecipe, classes

_name = "Down To Earth"

class dte(BasicNewsRecipe):
    title = 'Down To Earth'
    language = 'en_IN'
    oldest_article = 15
    __author__ = 'Amit'
    max_articles_per_feed = 100
    no_stylesheets = True
    remove_javascript = True
    center_navbar = True
    use_embedded_content = False
    remove_empty_feeds = True
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)
    keep_only_tags = [
        classes('detail-heading content-main news-basic-info news-banner news-detail-content')
    ]
    remove_tags = [
        classes('add-comment btn hindi_detail_link single-news-letter author-categories-tags donate-text'),
        dict(id=['comments', 'breadcrumb', 'node_related_stories']),
        dict(attrs={'class': ['commentCount', 'box']})
    ]

    feeds = [
        ('India', 'https://www.downtoearth.org.in/rss/india'),
        ('World', 'https://www.downtoearth.org.in/rss/world'),
        ('Agriculture', 'https://www.downtoearth.org.in/rss/agriculture'),
        ('Climate Change', 'https://www.downtoearth.org.in/rss/climate-change'),
        ('Renewable Energy','https://www.downtoearth.org.in/rss/renewable-energy'),
        ('Economy', 'https://www.downtoearth.org.in/rss/economy'),
        ('Energy', 'https://www.downtoearth.org.in/rss/energy'),
        ('Environment', 'https://www.downtoearth.org.in/rss/environment'),
        ('Forests', 'https://www.downtoearth.org.in/rss/forests'),
        ('Disaster', 'https://www.downtoearth.org.in/rss/natural-disasters'),
        ('Pollution', 'https://www.downtoearth.org.in/rss/pollution'),
        ('Water', 'https://www.downtoearth.org.in/rss/water'),
        ('Waste', 'https://www.downtoearth.org.in/rss/waste'),
    ]

# Air Pollution
# India
# World
# Environment 
# Agriculture
# Water
# Food
# Natural Disasters
# Waste
# Energy
# Wildlife & Biodiversity
# Economy
# Science & Technology
# Forests
# Health
# Cartoons
# Book Reviews
# Interviews