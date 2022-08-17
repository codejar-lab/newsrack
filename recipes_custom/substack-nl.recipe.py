#!/usr/bin/env  python

from calibre.web.feeds.news import BasicNewsRecipe, classes

_name = 'Substack Newsletters'

class Newsletters(BasicNewsRecipe):
    title = _name
    description = 'My Favourite Newsletters from Substack.'
    language = 'en_IN'
    __author__ = 'Arpan'
    oldest_article = 7  # days
    max_articles_per_feed = 2
    encoding = 'utf-8'
    use_embedded_content = True
    #masthead_url = 'https://upload.wikimedia.org/wikipedia/en/0/06/Sandesh%28IndianNewspaper%29Logo.jpg'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)
    feeds = [
        ('The Signal', 'https://daily.thesignal.co/feed'),
        ('Public Policy' ,'https://publicpolicy.substack.com/feed'),
        ('Multitudes' ,'https://shantanukishwar.substack.com/feed'),
        ('India Wants to Know', 'https://iwtkquiz.substack.com/feed'),
        ('Wisdom Project', 'https://wisdomproject.substack.com/feed'),
        ('Bank on Basak', 'https://www.bankonbasak.com/feed'),
        ('Curated Commons', 'https://subbu.substack.com/feed'),
        ('Environment of India', 'https://www.environmentofindia.com/feed'),
        ]

#        ('Network Capital', 'https://www.thenetworkcapital.com/feed'),       
#        https://pradologue.substack.com/feed
