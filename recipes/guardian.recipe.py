# Copyright (c) 2022 https://github.com/ping/
#
# This software is released under the GNU General Public License v3.0
# https://opensource.org/licenses/GPL-3.0

"""
guardian.com
"""
from datetime import timezone, timedelta
import json

from calibre.web.feeds.news import BasicNewsRecipe
from calibre.web.feeds import Feed

_name = "Guardian"


class Guardian(BasicNewsRecipe):
    title = _name
    description = "Latest international news, sport and comment from the Guardian"
    language = "en_GB"
    __author__ = "ping"
    publication_type = "newspaper"
    oldest_article = 1  # days
    max_articles_per_feed = 60
    use_embedded_content = False
    no_stylesheets = True
    remove_javascript = True
    encoding = "UTF-8"
    compress_news_images = True
    masthead_url = "https://assets.guim.co.uk/images/guardian-logo-rss.c45beb1bafa34b347ac333af2e6fe23f.png"
    scale_news_images = (800, 800)
    scale_news_images_to_device = False  # force img to be resized to scale_news_images
    auto_cleanup = False
    timeout = 20
    timefmt = ""
    pub_date = None  # custom publication date

    remove_attributes = ["style", "width", "height"]
    remove_tags_before = [dict(name="main")]
    remove_tags_after = [dict(name="main")]
    remove_tags = [
        dict(name=["svg", "input", "button", "label"]),
        dict(id=["bannerandheader", "the-caption", "liveblog-navigation"]),
        dict(
            class_=[
                "skip",
                "meta__social",
                "live-blog__filter-switch",
                "ad-slot",
                "l-footer",
                "is-hidden",
                "js-most-popular-footer",
                "submeta",
                "block-share",
                "content-footer",
            ]
        ),
        dict(name="div", attrs={"data-print-layout": "hide"}),
        dict(attrs={"name": "FilterKeyEventsToggle"}),
        dict(attrs={"aria-hidden": "true"}),
        dict(
            name="time", attrs={"data-relativeformat": "med"}
        ),  # remove the relative timestamp, e.g. 8h ago
        dict(attrs={"data-component": "podcast-help"}),
    ]

    extra_css = """
    [data-gu-name="headline"] h1 { font-size: 1.8rem; margin-bottom: 0.4rem; }
    [data-gu-name="standfirst"] p { font-size: 1.2rem; font-style: italic; margin-top: 0; margin-bottom: 1rem; }
    
    [data-component="series"], [data-component="section"] { margin-right: 0.5rem; }
    [data-gu-name="meta"] { margin-bottom: 1.5rem; }
    [data-component="meta-byline"] {
        margin-top: 1rem; margin-bottom: 1rem;
        font-weight: bold; color: #444; font-style: normal;
    }
    [data-component="meta-byline"] div { display: inline-block; margin-right: 0.5rem; }
    [data-component="meta-byline"] a { color: #444; }
    *[data-gu-name="media"] span, *[item-prop="description"],
    div[data-spacefinder-type$=".ImageBlockElement"] > div,
    div.caption { font-size: 0.8rem; margin-bottom: 0.5rem; }
    img { width: 100%; height: auto; margin-bottom: 0.2rem; }
    [data-name="placeholder"] { color: #444; font-style: italic; }
    [data-name="placeholder"] a { color: #444; }
    blockquote { font-size: 0.85rem; color: #222; }
    
    time { margin-right: 0.5rem; }
    .embed { color: #444; font-size: 0.8rem; }
    """

    feeds = [
        (_name, "https://www.theguardian.com/international/rss"),
    ]

    def preprocess_html(self, soup):
        meta = soup.find(attrs={"data-gu-name": "meta"})
        if meta:
            # remove author image
            for img in meta.find_all("img"):
                img.decompose()

            # reformat the displayed date
            details = meta.find_all("details")
            for detail in details:
                summary = detail.find("summary")
                update_date = None
                if len(detail.contents) > 1:
                    update_date = detail.contents[1]
                published = soup.new_tag("div", attrs={"class": "published-date"})
                published.append(summary.string)
                detail.clear()
                detail.append(published)
                if update_date:
                    update = soup.new_tag("div", attrs={"class": "last-updated-date"})
                    update.append(update_date)
                    detail.append(update)
                detail.name = "div"
                detail["class"] = "meta-date"

        # search for highest resolution image
        for picture in soup.find_all("picture"):
            max_img_width = 0
            max_img_url = None
            for source in picture.find_all("source"):
                for img in source["srcset"].split(","):
                    if len(img.strip().split(" ")) > 1:
                        img_url, img_width = img.strip().split(" ")
                        # Example: 1400w
                        img_width = int(img_width[:-1])
                        if img_width > max_img_width:
                            max_img_url = img_url
                    else:
                        max_img_url = img.strip()
                        break
            img = picture.find("img")
            img["src"] = max_img_url

        # remove share on social media links for live articles
        for unordered_list in soup.find_all("ul"):
            is_social_media = False
            for list_item in unordered_list.find_all("li"):
                a_link = list_item.find("a", attrs={"aria-label": True})
                if a_link and a_link["aria-label"] in [
                    "Share on Facebook",
                    "Share on Twitter",
                ]:
                    is_social_media = True
                    break
            if is_social_media:
                unordered_list.decompose()

        # Patch Key Events ul in live articles
        # The div forces a linebreak in the li > a looks bad in the Kindle
        for unordered_list in soup.find_all("ul"):
            for link_item in unordered_list.find_all("a"):
                if link_item["href"].startswith("?filterKeyEvents"):
                    link_text = self.tag_to_string(link_item)
                    link_item.parent.string = link_text

        # embed YT blocks
        for yt in soup.find_all(
            attrs={
                "data-spacefinder-type": "model.dotcomrendering.pageElements.YoutubeBlockElement"
            }
        ):
            info_ele = yt.find(name="gu-island")
            if not info_ele:
                continue
            info = json.loads(info_ele["props"])
            link = f'https://www.youtube.com/watch?v={info["assetId"]}'
            yt.clear()
            yt["class"] = "embed"
            yt.append(f'{info["mediaTitle"]} ')
            a_link = soup.new_tag("a", href=link)
            a_link.append(link)
            yt.append(a_link)
            self.log("*" * 5, yt)

        return soup

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = f"{_name}: {article.utctime:%-d %b, %Y}"

    def publication_date(self):
        return self.pub_date

    def parse_feeds(self):
        # convert single parsed feed into date-sectioned feed
        # use this only if there is just 1 feed
        parsed_feeds = super().parse_feeds()
        if len(parsed_feeds or []) != 1:
            return parsed_feeds

        articles = []
        for feed in parsed_feeds:
            articles.extend(feed.articles)
        articles = sorted(articles, key=lambda a: a.utctime, reverse=True)
        new_feeds = []
        curr_feed = None
        parsed_feed = parsed_feeds[0]
        for i, a in enumerate(articles, start=1):
            date_published = a.utctime.replace(tzinfo=timezone.utc)
            date_published_loc = date_published.astimezone(
                timezone(offset=timedelta(hours=1))  # UK time
            )
            article_index = f"{date_published_loc:%-d %B, %Y}"
            if i == 1:
                curr_feed = Feed(log=parsed_feed.logger)
                curr_feed.title = article_index
                curr_feed.description = parsed_feed.description
                curr_feed.image_url = parsed_feed.image_url
                curr_feed.image_height = parsed_feed.image_height
                curr_feed.image_alt = parsed_feed.image_alt
                curr_feed.oldest_article = parsed_feed.oldest_article
                curr_feed.articles = []
                curr_feed.articles.append(a)
                continue
            if curr_feed.title == article_index:
                curr_feed.articles.append(a)
            else:
                new_feeds.append(curr_feed)
                curr_feed = Feed(log=parsed_feed.logger)
                curr_feed.title = article_index
                curr_feed.description = parsed_feed.description
                curr_feed.image_url = parsed_feed.image_url
                curr_feed.image_height = parsed_feed.image_height
                curr_feed.image_alt = parsed_feed.image_alt
                curr_feed.oldest_article = parsed_feed.oldest_article
                curr_feed.articles = []
                curr_feed.articles.append(a)
            if i == len(articles):
                # last article
                new_feeds.append(curr_feed)

        return new_feeds
