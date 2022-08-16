#!/usr/bin/env  python

from calibre.web.feeds.news import BasicNewsRecipe, classes

_name = 'Finshots'

class Finshots(BasicNewsRecipe):
    title = u'Finshots'
    description = 'Finshots and get your daily dose of the latest, most important Financial developments delivered in plain English. In less than 3 minutes.'
    language = 'en_IN'
    __author__ = 'Arpan'
    oldest_article = 1  # days
    max_articles_per_feed = 50
    encoding = 'utf-8'
    use_embedded_content = False
    masthead_url = 'https://d3jlwjv6gmyigl.cloudfront.net/assets/two/images/logo-2d6831bc63e1ecb76091541e2f20069a.png'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)
    # keep_only_tags = [
    #     classes('page-hdng stry-shrt-head img-hgt-blk athr-info tm-stmp stry-bdy'),
    # ]

    remove_tags = [
        classes('social-links site-nav-logo container c-search__form subscribe-main site-foot read-next-feed floating-header-share floating-header'),
        dict(name='div', attrs={'id':'subs-popup-banner'}),
    #     dict(name='section', attrs={'class':'glry-cnt mostvdtm main-wdgt glry-bg'}),
    ]
    # remove_tags_after = [ classes('stry-bdy')]

    feeds = [
        ('Daily' ,'https://finshots.in/archive/rss/'),   
        ('Markets', 'https://finshots.in/markets/rss/'),
        ('Money', 'https://finshots.in/tag/money/rss/'),
        ]

    # def get_cover_url(self):
    #     soup = self.index_to_soup('https://www.magzter.com/IN/HT-Digital-Streams-Ltd./Hindustan-Times-Hindi-New-Delhi/Newspaper/')
    #     for citem in soup.findAll('meta', content=lambda s: s and s.endswith('view/3.jpg')):
    #         return citem['content']

calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'