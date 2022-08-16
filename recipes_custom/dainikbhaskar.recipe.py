#!/usr/bin/env  python

from calibre.web.feeds.news import BasicNewsRecipe, classes

_name = "Dainik Bhaskar"

class dainikbhaskar(BasicNewsRecipe):
    title = u'दैनिक भास्कर'
    description = 'Dainik Bhaskar is an Indian Hindi-language daily newspaper owned by the Dainik Bhaskar Group. It is ranked 4th in the world by circulation and is the largest newspaper in India by circulation.'
    language = 'hi'
    __author__ = 'unkn0wn'
    oldest_article = 1  # days
    max_articles_per_feed = 50
    encoding = 'utf-8'
    use_embedded_content = False
    masthead_url = 'https://tse4.mm.bing.net/th?id=OIP.t6kK1-rSpzNbSerwzD5qbQHaDY'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)
    
    def get_cover_url(self):
        soup = self.index_to_soup('https://epaper.bhaskar.com/')
        tag = soup.find(attrs={'class': 'scaleDiv'})
        if tag:
            self.cover_url = tag.find('img')['src'].replace("_ss.jpg", "_l.jpg")
        return super().get_cover_url()

    keep_only_tags = [
        classes('f5afa1d3'),
    ]

    remove_tags = [
        classes('_3c197847 _66d97d7f e0d43c76 bhaskar-widget-container-class _28e65306 _8adadf19 _07c65a39'),
        dict(name='svg'),
    ]

    feeds = [
        ('देश ', 'https://www.bhaskar.com/rss-v1--category-1061.xml'),
        ('ओपिनियन', 'https://www.bhaskar.com/rss-v1--category-1944.xml'),
        ('विदेश ', 'https://www.bhaskar.com/rss-v1--category-1125.xml'),
        ('ओरिजिनल', 'https://www.bhaskar.com/rss-v1--category-4587.xml'),
        ('बिजनेस', 'https://www.bhaskar.com/rss-v1--category-1051.xml'),
        ('स्पोर्ट्स ', 'https://www.bhaskar.com/rss-v1--category-1053.xml'),
        ('मैगजीन ', 'https://www.bhaskar.com/rss-v1--category-1057.xml'),
        ('करिअर ', 'https://www.bhaskar.com/rss-v1--category-11945.xml'),
        #https://www.bhaskar.com/rss
        ]

calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'