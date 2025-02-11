# Copyright (c) 2022 https://github.com/ping/
#
# This software is released under the GNU General Public License v3.0
# https://opensource.org/licenses/GPL-3.0

"""
ft.com
"""
from urllib.parse import urljoin, quote_plus
import json
import re
from datetime import datetime, timezone

from calibre.web.feeds.news import BasicNewsRecipe
from calibre.ebooks.BeautifulSoup import BeautifulSoup

_name = "Financial Times"


class FinancialTimes(BasicNewsRecipe):
    title = _name
    __author__ = "ping"
    description = "Financial Times"
    publisher = "The Financial Times Ltd."
    language = "en_GB"
    category = "news, finance, politics, UK, World"
    publication_type = "newspaper"
    oldest_article = 1  # days
    use_embedded_content = False
    encoding = "utf-8"
    remove_javascript = True
    no_stylesheets = True
    auto_cleanup = False
    masthead_url = "https://www.ft.com/partnercontent/content-hub/static/media/ft-horiz-new-black.215c1169.png"
    ignore_duplicate_articles = {"url"}

    timeout = 20
    timefmt = ""
    pub_date = None  # custom publication date

    extra_css = """
    .headline { font-size: 1.8rem; margin-bottom: 0.5rem; }
    .sub-headline { margin-bottom: 0.4rem;  color: #444; font-size: 1.2rem; }
    .article-meta { margin-top: 1rem; padding-bottom: 0.2rem; border-bottom: 1px solid #aaa; }
    .article-meta .author { font-weight: bold; color: #444; }
    .article-meta .published-dt { margin-left: 0.5rem; }
    .article-img { margin-bottom: 0.8rem; }
    .article-img img { display: block; margin-bottom: 0.3rem; }
    .article-img .caption { font-size: 0.8rem; }
    """

    feeds = [
        ("Home", "https://www.ft.com/rss/home"),
        ("Home (International)", "https://www.ft.com/rss/home/international"),
        ("World", "https://www.ft.com/world?format=rss"),
        ("US", "https://www.ft.com/world/us?format=rss"),
        ("Technology", "https://www.ft.com/technology?format=rss"),
        ("Markets", "https://www.ft.com/markets?format=rss"),
        ("Climate", "https://www.ft.com/climate-capital?format=rss"),
        ("Opinion", "https://www.ft.com/opinion?format=rss"),
        # ("Work & Careers", "https://www.ft.com/work-careers?format=rss"),
        # ("Life & Arts", "https://www.ft.com/life-arts?format=rss"),
        # ("How to Spend It", "https://www.ft.com/htsi?format=rss"),
    ]

    def get_cover_url(self):
        soup = self.index_to_soup(
            "https://www.todayspapers.co.uk/the-financial-times-front-page-today/"
        )
        tag = soup.find("div", attrs={"class": "elementor-image"})
        if tag:
            self.cover_url = tag.find("img")["src"]
        return getattr(self, "cover_url", self.cover_url)

    def print_version(self, url):
        return urljoin("https://ft.com", url)

    def preprocess_raw_html(self, raw_html, url):
        article = None
        soup = BeautifulSoup(raw_html)
        for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
            article = json.loads(script.contents[0])
            if not (article.get("@type") and article["@type"] == "NewsArticle"):
                continue
            break
        if not (article and article.get("articleBody")):
            self.abort_article(f"Unable to find article: {url}")
        try:
            author = article.get("author", {}).get("name", "")
        except AttributeError:
            author = ", ".join([a["name"] for a in article.get("author", [])])

        date_published = article.get("datePublished", None)
        if date_published:
            # Example: 2022-03-29T04:00:05.154Z
            date_published = datetime.strptime(
                date_published, "%Y-%m-%dT%H:%M:%S.%fZ"
            ).replace(tzinfo=timezone.utc)

        paragraphs = []
        for para in article["articleBody"].split("\n\n"):
            if para.startswith("RECOMMENDED"):  # skip recommended inserts
                continue
            if "ARE YOU PERSONALLY AFFECTED BY THE WAR IN UKRAINE" in para.upper():
                continue
            if "NEWSLETTER" in para:
                continue
            para = para.replace("\n", " ")
            mobj = re.findall(
                r"^(?P<caption>.*)\[(?P<img_url>https://.+\.(jpg|png))\]",
                para,
            )
            if mobj:
                for caption, img_url, _ in mobj:
                    # reduced image size
                    new_img_url = f"https://www.ft.com/__origami/service/image/v2/images/raw/{quote_plus(img_url)}?fit=scale-down&source=next&width=700"
                    # replace the image tag
                    para = para.replace(
                        f"{caption}[{img_url}]",
                        f"""<div class="article-img">
                            <img src="{new_img_url}" title="{caption}">
                            <span class="caption">{caption}</span>
                            </div>""",
                    )
            para = f"<p>{para}</p>"
            paragraphs.append(para)
        article_body = "\n".join(paragraphs)

        html_output = f"""<html><head><title>{article["headline"]}</title></head>
        <body>
            <article data-og-link="{url}">
            <h1 class="headline">{article["headline"]}</h1>
            {"" if not article.get("description") else '<div class="sub-headline">' + article.get("description", "") + '</div>'}
            <div class="article-meta">
                <span class="author">{author}</span>
                <span class="published-dt">{date_published:%-d %B, %Y}</span>
            </div>
            {article_body}
            </article>
        </body></html>
        """
        return html_output

    def populate_article_metadata(self, article, soup, _):
        # pick up the og link from preprocess_raw_html() and set it as url instead of the rss url
        og_link = soup.select("[data-og-link]")
        if og_link:
            article.url = og_link[0]["data-og-link"]
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = f"{_name}: {article.utctime:%-d %b, %Y}"

    def publication_date(self):
        return self.pub_date
