#!/usr/bin/env  python
import json
import datetime
from calibre.web.feeds.news import BasicNewsRecipe, classes

_name = 'Sandesh'
class Sandesh(BasicNewsRecipe):
    title = u'Sandesh'
    description = 'Sandesh is a Gujarati language daily newspaper in India.'
    language = 'gu'
    __author__ = 'Arpan'
    oldest_article = 1  # days
    max_articles_per_feed = 50
    encoding = 'utf-8'
    use_embedded_content = True
    masthead_url = 'https://upload.wikimedia.org/wikipedia/en/0/06/Sandesh%28IndianNewspaper%29Logo.jpg'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)
    # keep_only_tags = [
    #     classes('detail-news article-detail-news'),
    # ]

    # remove_tags = [
    #     classes('logo main-menu logo_date_time footer news-tags single-box social multiple citydrop react-share__ShareButton mx-1'),
    #     dict(name='div', attrs={'id':'subs-popup-banner'}),
    #     dict(name='section', attrs={'class':'glry-cnt mostvdtm main-wdgt glry-bg'}),
    #  ]
    # remove_tags_after = [ classes('stry-bdy')]

    feeds = [
        ('Gujarat' ,'https://sandesh.com/rss/gujarat.xml'),        
        ('National', 'https://sandesh.com/rss/india.xml'),
        ('International', 'https://sandesh.com/rss/world.xml'),
        ('Editorial', 'https://sandesh.com/rss/opinion.xml'),
        ('Science & Technology', 'https://sandesh.com/rss/tech.xml'),
        ('Business', 'https://sandesh.com/rss/business.xml'),
        ('Sports', 'https://sandesh.com/rss/sports.xml'),
        ('Health', 'https://sandesh.com/rss/health.xml'),
        ('Lifestyle & Fashion', 'https://sandesh.com/rss/lifestyle.xml'),
        ('Entertainment', 'https://sandesh.com/rss/entertainment.xml'),
        ]

    def get_cover_url(self):
        date_td = datetime.date.today()
        url = 'https://wapi.sandesh.com/api/v1/e-paper?slug=ahmedabad&date=' + str(date_td)
        soup = self.index_to_soup(url)
        response = json.loads(soup.text)
        posturl = (response['data']['sub'][0]['photo'])
        cover_url = 'https://esandesh.gumlet.io/' + posturl
        return cover_url

calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'