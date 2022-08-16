#!/usr/bin/env  python

from calibre.web.feeds.news import BasicNewsRecipe, classes

_name = 'Daily Current Affairs'

class dailycurrentaffairs(BasicNewsRecipe):
    title = _name
    description = ''
    language = 'en_IN'
    __author__ = 'Arpan'
    oldest_article = 1.5  # days
    max_articles_per_feed = 50
    encoding = 'utf-8'
    use_embedded_content = False
    #masthead_url = 'https://upload.wikimedia.org/wikipedia/en/0/06/Sandesh%28IndianNewspaper%29Logo.jpg'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)

    keep_only_tags = [
        classes('card-body entry-content')
    ]

    remove_tags = [
        classes('printfriendly p-0 awac-wrapper mb-0 readmore blog'),
        dict(name = 'a', attrs = {'rel' : 'noopener'})
        # dict(name = 'div', attrs = {'id' : lambda x: x and x.startswith('inside_post_content_ad')}),    
        # dict(name = 'div', attrs = {'id' : lambda x: x and x.startswith('filler_ad')})
    ]

    feeds = [
        ('Insights', 'https://www.insightsonindia.com/category/current-affairs-2/feed/'),
        ('IASbaba', 'https://iasbaba.com/iasbabas-daily-current-affairs/feed/'),
        ]

    def preprocess_html(self, soup):
        for img in soup.findAll('img', attrs={'data-src': True}):
            img['src'] = img['data-src'].split('?')[0]
        return soup