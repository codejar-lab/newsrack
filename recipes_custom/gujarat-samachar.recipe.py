#!/usr/bin/env  python

from calibre.web.feeds.news import BasicNewsRecipe, classes

_name = 'Gujarat Samachar'
class GujaratSamachar(BasicNewsRecipe):
    title = u'Gujarat Samachar'
    description = 'Gujarat Samachar is a Gujarati language daily newspaper in India.'
    language = 'gu'
    __author__ = 'Arpan'
    oldest_article = 1  # days
    max_articles_per_feed = 50
    encoding = 'utf-8'
    use_embedded_content = False
    masthead_url = 'https://www.gujaratsamachar.com/assets/logo.png'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)
    keep_only_tags = [
        classes('detail-news article-detail-news'),
    ]

    remove_tags = [
        classes('logo main-menu logo_date_time footer news-tags single-box social multiple citydrop react-share__ShareButton mx-1'),
    #     dict(name='div', attrs={'id':'subs-popup-banner'}),
    #     dict(name='section', attrs={'class':'glry-cnt mostvdtm main-wdgt glry-bg'}),
     ]
    # remove_tags_after = [ classes('stry-bdy')]

    feeds = [
        ('Top Stories' ,'https://www.gujaratsamachar.com/rss/top-stories'),        
        ('National', 'https://www.gujaratsamachar.com/rss/category/national'),
        ('International', 'https://www.gujaratsamachar.com/rss/category/international'),
        ('Editorial', 'https://www.gujaratsamachar.com/rss/category/editorial'),
        ('Science & Technology', 'https://www.gujaratsamachar.com/rss/category/science-technology'),
        ('Business', 'https://www.gujaratsamachar.com/rss/category/business'),
        ('Sports', 'https://www.gujaratsamachar.com/rss/category/sports'),
        ('Health', 'https://www.gujaratsamachar.com/rss/category/health'),
        ('Lifestyle & Fashion', 'https://www.gujaratsamachar.com/rss/category/lifestyle-fashion'),
        ('Entertainment', 'https://www.gujaratsamachar.com/rss/category/entertainment'),
        ]

    # def get_cover_url(self):
    #     soup = self.index_to_soup('https://www.magzter.com/IN/HT-Digital-Streams-Ltd./Hindustan-Times-Hindi-New-Delhi/Newspaper/')
    #     for citem in soup.findAll('meta', content=lambda s: s and s.endswith('view/3.jpg')):
    #         return citem['content']

calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'