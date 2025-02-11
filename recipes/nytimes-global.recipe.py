# Copyright (c) 2022 https://github.com/ping/
#
# This software is released under the GNU General Public License v3.0
# https://opensource.org/licenses/GPL-3.0

"""
nytimes.com
"""
import datetime
import re
import json

from calibre.web.feeds.news import BasicNewsRecipe
from calibre.ebooks.BeautifulSoup import BeautifulSoup

_name = "NY Times"


class NYTimesGlobal(BasicNewsRecipe):
    title = _name
    language = "en"
    __author__ = "ping"
    publication_type = "newspaper"
    description = "News from the New York Times"
    masthead_url = "https://mwcm.nyt.com/.resources/mkt-wcm/dist/libs/assets/img/logo-nyt-header.svg"

    oldest_article = 1  # days
    max_articles_per_feed = 25
    use_embedded_content = False
    timeout = 20
    timefmt = ""
    pub_date = None  # custom publication date

    simultaneous_downloads = 1

    remove_javascript = True
    no_stylesheets = True
    auto_cleanup = False
    compress_news_images = True
    scale_news_images = (800, 800)
    scale_news_images_to_device = False  # force img to be resized to scale_news_images

    ignore_duplicate_articles = {"title", "url"}

    remove_attributes = ["style", "font"]
    remove_tags_before = [dict(id="story")]
    remove_tags_after = [dict(id="story")]

    remove_tags = [
        dict(
            id=["in-story-masthead", "sponsor-wrapper", "top-wrapper", "bottom-wrapper"]
        ),
        dict(
            class_=[
                "NYTAppHideMasthead",
                "live-blog-meta",
                "css-13xl2ke",  # nyt logo in live-blog-byline
                "css-8r08w0",  # after storyline-context-container
            ]
        ),
        dict(role=["toolbar", "navigation", "contentinfo"]),
        dict(name=["script", "noscript", "style", "button", "svg"]),
    ]

    extra_css = """
    .live-blog-reporter-update {
        font-size: 0.8rem;
        padding: 0.2rem;
        margin-bottom: 0.5rem;
    }
    [data-testid="live-blog-byline"] {
        color: #444;
        font-style: italic;
    }
    [datetime] > span {
        margin-right: 0.6rem;
    }
    picture img {
        display: block; margin-bottom: 0.3rem; max-width: 100%; height: auto;
        box-sizing: border-box;
    }
    [aria-label="media"] {
        font-size: 0.8rem;
        display: block;
        margin-bottom: 1rem;
    }
    [role="complementary"] {
        font-size: 0.8rem;
        padding: 0.2rem;
    }
    [role="complementary"] h2 {
        font-size: 0.85rem;
        margin-bottom: 0.2rem;
     }

    .headline { font-size: 1.8rem; margin-bottom: 0.4rem; }
    .sub-headline { font-size: 1.2rem; font-style: italic; margin-bottom: 1rem; }
    .article-meta { margin-bottom: 1rem; }
    .article-meta .author { font-weight: bold; color: #444; }
    .article-meta .published-dt { margin-left: 0.5rem; }
    .article-img { margin-bottom: 0.8rem; max-width: 100%; }
    .article-img img {
        display: block; margin-bottom: 0.3rem; max-width: 100%; height: auto;
        box-sizing: border-box; }
    .article-img .caption { font-size: 0.8rem; }
    div.summary { font-size: 1.2rem; margin: 1rem 0; }
    """

    feeds = [
        ("Home", "https://www.nytimes.com/services/xml/rss/nyt/HomePage.xml"),
        # (
        #     "Global Home",
        #     "https://www.nytimes.com/services/xml/rss/nyt/GlobalHome.xml",
        # ),
        ("World", "https://www.nytimes.com/services/xml/rss/nyt/World.xml"),
        ("US", "https://www.nytimes.com/services/xml/rss/nyt/US.xml"),
        ("Business", "https://feeds.nytimes.com/nyt/rss/Business"),
        # ("Sports", "https://www.nytimes.com/services/xml/rss/nyt/Sports.xml"),
        ("Technology", "https://feeds.nytimes.com/nyt/rss/Technology"),
    ]

    def get_browser(self, *a, **kw):
        kw[
            "user_agent"
        ] = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        br = BasicNewsRecipe.get_browser(self, *a, **kw)
        return br

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = f"{_name}: {article.utctime:%-d %b, %Y}"

    def publication_date(self):
        return self.pub_date

    def preprocess_initial_data(self, template_html, info, raw_html, url):
        article = (info.get("initialData", {}) or {}).get("data", {}).get("article")
        body = article.get("sprinkledBody") or article.get("body")
        if not body:
            return raw_html

        new_soup = BeautifulSoup(template_html, "html.parser")
        for c in body.get("content", []):
            content_type = c["__typename"]
            if content_type in [
                "Dropzone",
                "RelatedLinksBlock",
                "EmailSignupBlock",
                "CapsuleBlock",  # ???
                "InteractiveBlock",
                "RelatedLinksBlock",
                "UnstructuredBlock",
            ]:
                continue
            if content_type in [
                "HeaderBasicBlock",
                "HeaderFullBleedVerticalBlock",
                "HeaderFullBleedHorizontalBlock",
                "HeaderMultimediaBlock",
                "HeaderLegacyBlock",
            ]:
                # Article Header / Meta
                if c.get("headline"):
                    headline = c["headline"]
                    heading_text = ""
                    if headline.get("default@stripHtml"):
                        heading_text += headline["default@stripHtml"]
                    else:
                        for x in headline.get("content", []):
                            heading_text += x.get("text@stripHtml", "") or x.get(
                                "text", ""
                            )
                    new_soup.head.title.string = heading_text
                    new_soup.body.article.h1.string = heading_text
                if c.get("summary"):
                    summary_text = ""
                    for x in c["summary"].get("content", []):
                        summary_text += x.get("text", "") or x.get("text@stripHtml", "")
                    subheadline = new_soup.find("div", class_="sub-headline")
                    subheadline.string = summary_text
                if c.get("timestampBlock"):
                    # Example 2022-04-12T09:00:05.000Z
                    post_date = datetime.datetime.strptime(
                        c["timestampBlock"]["timestamp"],
                        "%Y-%m-%dT%H:%M:%S.%fZ",
                    )
                    pub_dt_ele = new_soup.find("span", class_="published-dt")
                    pub_dt_ele.string = f"{post_date:%-d %B, %Y}"
                if c.get("ledeMedia"):
                    image_block = c["ledeMedia"]["media"]
                    container_ele = new_soup.new_tag(
                        "div", attrs={"class": "article-img"}
                    )
                    if "crops" not in image_block:
                        # not an image leded
                        continue
                    img_url = image_block["crops"][0]["renditions"][0]["url"]
                    img_ele = new_soup.new_tag("img")
                    img_ele["src"] = img_url
                    container_ele.append(img_ele)
                    if image_block.get("legacyHtmlCaption"):
                        span_ele = new_soup.new_tag("span", attrs={"class": "caption"})
                        span_ele.append(BeautifulSoup(image_block["legacyHtmlCaption"]))
                        container_ele.append(span_ele)
                    new_soup.body.article.append(container_ele)
                if c.get("byline"):
                    authors = []
                    for b in c["byline"]["bylines"]:
                        for creator in b["creators"]:
                            authors.append(creator["displayName"])
                    pub_dt_ele = new_soup.find("span", class_="author")
                    pub_dt_ele.string = ", ".join(authors)
            elif content_type in ["ParagraphBlock", "DetailBlock"]:
                para_ele = new_soup.new_tag("p")
                para_ele.string = ""
                for cc in c.get("content", []):
                    para_ele.string += cc.get("text", "")
                new_soup.body.article.append(para_ele)
            elif content_type == "ImageBlock":
                image_block = c["media"]
                container_ele = new_soup.new_tag("div", attrs={"class": "article-img"})
                for v in image_block.get("crops", []):
                    img_url = v["renditions"][0]["url"]
                    img_ele = new_soup.new_tag("img")
                    img_ele["src"] = img_url
                    container_ele.append(img_ele)
                    break
                if image_block.get("legacyHtmlCaption"):
                    span_ele = new_soup.new_tag("span", attrs={"class": "caption"})
                    span_ele.append(BeautifulSoup(image_block["legacyHtmlCaption"]))
                    container_ele.append(span_ele)
                new_soup.body.article.append(container_ele)
            elif content_type == "DiptychBlock":
                # 2-image block
                image_blocks = [c["imageOne"], c["imageTwo"]]
                for image_block in image_blocks:
                    container_ele = new_soup.new_tag(
                        "div", attrs={"class": "article-img"}
                    )
                    for v in image_block.get("crops", []):
                        img_url = v["renditions"][0]["url"]
                        img_ele = new_soup.new_tag("img")
                        img_ele["src"] = img_url
                        container_ele.append(img_ele)
                        break
                    if image_block.get("legacyHtmlCaption"):
                        span_ele = new_soup.new_tag("span", attrs={"class": "caption"})
                        span_ele.append(BeautifulSoup(image_block["legacyHtmlCaption"]))
                        container_ele.append(span_ele)
                    new_soup.body.article.append(container_ele)
            elif content_type == "GridBlock":
                # n-image block
                container_ele = new_soup.new_tag("div", attrs={"class": "article-img"})
                for image_block in c.get("gridMedia", []):
                    for v in image_block.get("crops", []):
                        img_url = v["renditions"][0]["url"]
                        img_ele = new_soup.new_tag("img")
                        img_ele["src"] = img_url
                        container_ele.append(img_ele)
                        break
                caption = f'{c.get("caption", "")} {c.get("credit", "")}'.strip()
                if caption:
                    span_ele = new_soup.new_tag("span", attrs={"class": "caption"})
                    span_ele.append(BeautifulSoup(caption))
                    container_ele.append(span_ele)
                new_soup.body.article.append(container_ele)
            elif content_type == "DetailBlock":
                container_ele = new_soup.new_tag("div", attrs={"class": "detail"})
                for d in c["content"]:
                    if d["__typename"] == "LineBreakInline":
                        container_ele.append(new_soup.new_tag("br"))
                    elif d["__typename"] == "TextInline":
                        container_ele.append(d["text"])
                new_soup.body.article.append(container_ele)
            elif content_type == "BlockquoteBlock":
                container_ele = new_soup.new_tag("blockquote")
                for x in c["content"]:
                    if x["__typename"] == "ParagraphBlock":
                        para_ele = new_soup.new_tag("p")
                        para_ele.string = ""
                        for xx in x.get("content", []):
                            para_ele.string += xx.get("text", "")
                        container_ele.append(para_ele)
                new_soup.body.article.append(container_ele)
            elif content_type in ["Heading1Block", "Heading2Block", "Heading3Block"]:
                if content_type == "Heading1Block":
                    container_tag = "h1"
                elif content_type == "Heading2Block":
                    container_tag = "h2"
                else:
                    container_tag = "h3"
                container_ele = new_soup.new_tag(container_tag)
                for x in c["content"]:
                    if x["__typename"] == "TextInline":
                        container_ele.append(
                            x.get("text", "") or x.get("text@stripHtml", "")
                        )
                new_soup.body.article.append(container_ele)
            elif content_type == "ListBlock":
                if c["style"] == "UNORDERED":
                    container_ele = new_soup.new_tag("ul")
                else:
                    container_ele = new_soup.new_tag("ol")
                for x in c["content"]:
                    li_ele = new_soup.new_tag("li")
                    for y in x["content"]:
                        if y["__typename"] == "ParagraphBlock":
                            para_ele = new_soup.new_tag("p")
                            for z in y.get("content", []):
                                para_ele.append(z.get("text", ""))
                            li_ele.append(para_ele)
                    container_ele.append(li_ele)
                new_soup.body.article.append(container_ele)
            elif content_type == "PullquoteBlock":
                container_ele = new_soup.new_tag("blockquote")
                for x in c["quote"]:
                    if x["__typename"] == "TextInline":
                        container_ele.append(x["text"])
                    if x["__typename"] == "ParagraphBlock":
                        para_ele = new_soup.new_tag("p")
                        for z in x.get("content", []):
                            para_ele.append(z.get("text", ""))
                        container_ele.append(para_ele)
                new_soup.body.article.append(container_ele)
            elif content_type == "VideoBlock":
                container_ele = new_soup.new_tag("div", attrs={"class": "embed"})
                container_ele.string = "[Embedded video available]"
                new_soup.body.article.append(container_ele)
            elif content_type == "AudioBlock":
                container_ele = new_soup.new_tag("div", attrs={"class": "embed"})
                container_ele.string = "[Embedded audio available]"
                new_soup.body.article.append(container_ele)
            elif content_type == "BylineBlock":
                # For podcasts? - TBD
                pass
            elif content_type == "YouTubeEmbedBlock":
                container_ele = new_soup.new_tag("div", attrs={"class": "embed"})
                yt_link = f'https://www.youtube.com/watch?v={c["youTubeId"]}'
                a_ele = new_soup.new_tag("a", href=yt_link)
                a_ele.string = yt_link
                container_ele.append(a_ele)
                new_soup.body.article.append(container_ele)
            elif content_type == "TwitterEmbedBlock":
                container_ele = new_soup.new_tag("div", attrs={"class": "embed"})
                container_ele.append(BeautifulSoup(c["html"]))
                new_soup.body.article.append(container_ele)
            elif content_type == "InstagramEmbedBlock":
                container_ele = new_soup.new_tag("div", attrs={"class": "embed"})
                a_ele = new_soup.new_tag("a", href=c["instagramUrl"])
                a_ele.string = c["instagramUrl"]
                container_ele.append(a_ele)
                new_soup.body.article.append(container_ele)
            elif content_type == "LabelBlock":
                container_ele = new_soup.new_tag("h4", attrs={"class": "label"})
                for x in c["content"]:
                    if x["__typename"] == "TextInline":
                        container_ele.append(x["text"])
                new_soup.body.article.append(container_ele)
            elif content_type == "SummaryBlock":
                container_ele = new_soup.new_tag("div", attrs={"class": "summary"})
                for x in c["content"]:
                    if x["__typename"] == "TextInline":
                        container_ele.append(x["text"])
                new_soup.body.article.append(container_ele)
            elif content_type == "TimestampBlock":
                timestamp_val = c["timestamp"]
                container_ele = new_soup.new_tag(
                    "time", attrs={"data-timestamp": timestamp_val}
                )
                container_ele.append(timestamp_val)
                new_soup.body.article.append(container_ele)
            elif content_type == "RuleBlock":
                new_soup.body.article.append(new_soup.new_tag("hr"))
            else:
                self.log.warning(f"{url} has unexpected element: {content_type}")
                self.log.debug(json.dumps(c))

        return str(new_soup)

    def preprocess_initial_state(self, template_html, info, raw_html, url):
        content_service = info.get("initialState")
        content_node_id = None
        for k, v in content_service["ROOT_QUERY"].items():
            if not (
                k.startswith("workOrLocation") and v and v["typename"] == "Article"
            ):
                continue
            content_node_id = v["id"]
            break
        if not content_node_id:
            for k, v in content_service["ROOT_QUERY"].items():
                if not (
                    k.startswith("workOrLocation")
                    and v
                    and v["typename"] == "LegacyCollection"
                ):
                    continue
                content_node_id = v["id"]
                break

        if not content_node_id:
            self.log(f"Unable to find content in script in {url}")
            return raw_html

        article = content_service.get(content_node_id)
        try:
            body = article.get("sprinkledBody") or article.get("body")
            document_block = content_service[body["id"]]  # typename = "DocumentBlock"
        except:  # noqa
            # live blog probably
            self.log(f"Unable to find content in article object for {url}")
            return raw_html

        new_soup = BeautifulSoup(template_html, "html.parser")

        for c in document_block.get("content@filterEmpty", []):
            content_type = c["typename"]
            if content_type in [
                "Dropzone",
                "RelatedLinksBlock",
                "EmailSignupBlock",
                "CapsuleBlock",  # ???
                "InteractiveBlock",
            ]:
                continue
            if content_type in [
                "HeaderBasicBlock",
                "HeaderFullBleedVerticalBlock",
                "HeaderFullBleedHorizontalBlock",
                "HeaderMultimediaBlock",
                "HeaderLegacyBlock",
            ]:
                # Article Header / Meta
                header_block = content_service[c["id"]]
                if header_block.get("headline"):
                    heading_text = ""
                    headline = content_service[header_block["headline"]["id"]]
                    if headline.get("default@stripHtml"):
                        heading_text += headline["default@stripHtml"]
                    else:
                        for x in headline.get("content", []):
                            heading_text += content_service.get(x["id"], {}).get(
                                "text@stripHtml", ""
                            ) or content_service.get(x["id"], {}).get("text", "")
                    new_soup.head.title.string = heading_text
                    new_soup.body.article.h1.string = heading_text
                if header_block.get("summary"):
                    summary_text = ""
                    for x in content_service.get(header_block["summary"]["id"]).get(
                        "content", []
                    ):
                        summary_text += content_service.get(x["id"], {}).get(
                            "text@stripHtml", ""
                        ) or content_service.get(x["id"], {}).get("text", "")
                    subheadline = new_soup.find("div", class_="sub-headline")
                    subheadline.string = summary_text
                if header_block.get("timestampBlock"):
                    # Example 2022-04-12T09:00:05.000Z
                    post_date = datetime.datetime.strptime(
                        content_service[header_block["timestampBlock"]["id"]][
                            "timestamp"
                        ],
                        "%Y-%m-%dT%H:%M:%S.%fZ",
                    )
                    pub_dt_ele = new_soup.find("span", class_="published-dt")
                    pub_dt_ele.string = f"{post_date:%-d %B, %Y}"
                if header_block.get("ledeMedia"):
                    image_block = content_service.get(
                        content_service[header_block["ledeMedia"]["id"]]["media"]["id"]
                    )
                    container_ele = new_soup.new_tag(
                        "div", attrs={"class": "article-img"}
                    )
                    for k, v in image_block.items():
                        if not k.startswith("crops("):
                            continue
                        img_url = content_service[
                            content_service[v[0]["id"]]["renditions"][0]["id"]
                        ]["url"]
                        img_ele = new_soup.new_tag("img")
                        img_ele["src"] = img_url
                        container_ele.append(img_ele)
                        break
                    if image_block.get("legacyHtmlCaption"):
                        span_ele = new_soup.new_tag("span", attrs={"class": "caption"})
                        span_ele.append(BeautifulSoup(image_block["legacyHtmlCaption"]))
                        container_ele.append(span_ele)
                    new_soup.body.article.append(container_ele)
                if header_block.get("byline"):
                    authors = []
                    for b in content_service[header_block["byline"]["id"]]["bylines"]:
                        for creator in content_service[b["id"]]["creators"]:
                            authors.append(
                                content_service[creator["id"]]["displayName"]
                            )
                    pub_dt_ele = new_soup.find("span", class_="author")
                    pub_dt_ele.string = ", ".join(authors)
            elif content_type == "ParagraphBlock":
                para_ele = new_soup.new_tag("p")
                para_ele.string = ""
                for cc in content_service.get(c["id"], {}).get("content", []):
                    para_ele.string += content_service.get(cc["id"], {}).get("text", "")
                new_soup.body.article.append(para_ele)
            elif content_type == "ImageBlock":
                image_block = content_service.get(
                    content_service.get(c["id"], {}).get("media", {}).get("id", "")
                )
                container_ele = new_soup.new_tag("div", attrs={"class": "article-img"})
                for k, v in image_block.items():
                    if not k.startswith("crops("):
                        continue
                    img_url = content_service[
                        content_service[v[0]["id"]]["renditions"][0]["id"]
                    ]["url"]
                    img_ele = new_soup.new_tag("img")
                    img_ele["src"] = img_url
                    container_ele.append(img_ele)
                    break
                if image_block.get("legacyHtmlCaption"):
                    span_ele = new_soup.new_tag("span", attrs={"class": "caption"})
                    span_ele.append(BeautifulSoup(image_block["legacyHtmlCaption"]))
                    container_ele.append(span_ele)
                new_soup.body.article.append(container_ele)
            elif content_type == "DiptychBlock":
                # 2-image block
                diptych_block = content_service[c["id"]]
                image_block_ids = [
                    diptych_block["imageOne"]["id"],
                    diptych_block["imageTwo"]["id"],
                ]
                for image_block_id in image_block_ids:
                    image_block = content_service[image_block_id]
                    container_ele = new_soup.new_tag(
                        "div", attrs={"class": "article-img"}
                    )
                    for k, v in image_block.items():
                        if not k.startswith("crops("):
                            continue
                        img_url = content_service[
                            content_service[v[0]["id"]]["renditions"][0]["id"]
                        ]["url"]
                        img_ele = new_soup.new_tag("img")
                        img_ele["src"] = img_url
                        container_ele.append(img_ele)
                        break
                    if image_block.get("legacyHtmlCaption"):
                        span_ele = new_soup.new_tag("span", attrs={"class": "caption"})
                        span_ele.append(BeautifulSoup(image_block["legacyHtmlCaption"]))
                        container_ele.append(span_ele)
                    new_soup.body.article.append(container_ele)
            elif content_type == "GridBlock":
                # n-image block
                grid_block = content_service[c["id"]]
                image_block_ids = [
                    m["id"]
                    for m in grid_block.get("media", [])
                    if m["typename"] == "Image"
                ]
                container_ele = new_soup.new_tag("div", attrs={"class": "article-img"})
                for image_block_id in image_block_ids:
                    image_block = content_service[image_block_id]
                    for k, v in image_block.items():
                        if not k.startswith("crops("):
                            continue
                        img_url = content_service[
                            content_service[v[0]["id"]]["renditions"][0]["id"]
                        ]["url"]
                        img_ele = new_soup.new_tag("img")
                        img_ele["src"] = img_url
                        container_ele.append(img_ele)
                        break
                caption = (
                    f'{grid_block.get("caption", "")} {grid_block.get("credit", "")}'
                ).strip()
                if caption:
                    span_ele = new_soup.new_tag("span", attrs={"class": "caption"})
                    span_ele.append(BeautifulSoup(caption))
                    container_ele.append(span_ele)
                new_soup.body.article.append(container_ele)
            elif content_type == "DetailBlock":
                container_ele = new_soup.new_tag("div", attrs={"class": "detail"})
                for x in content_service[c["id"]]["content"]:
                    d = content_service[x["id"]]
                    if d["__typename"] == "LineBreakInline":
                        container_ele.append(new_soup.new_tag("br"))
                    elif d["__typename"] == "TextInline":
                        container_ele.append(d["text"])
                new_soup.body.article.append(container_ele)
            elif content_type == "BlockquoteBlock":
                container_ele = new_soup.new_tag("blockquote")
                for x in content_service[c["id"]]["content"]:
                    if x["typename"] == "ParagraphBlock":
                        para_ele = new_soup.new_tag("p")
                        para_ele.string = ""
                        for xx in content_service.get(x["id"], {}).get("content", []):
                            para_ele.string += content_service.get(xx["id"], {}).get(
                                "text", ""
                            )
                        container_ele.append(para_ele)
                new_soup.body.article.append(container_ele)
            elif content_type in ["Heading1Block", "Heading2Block", "Heading3Block"]:
                if content_type == "Heading1Block":
                    container_tag = "h1"
                elif content_type == "Heading2Block":
                    container_tag = "h2"
                else:
                    container_tag = "h3"
                container_ele = new_soup.new_tag(container_tag)
                for x in content_service[c["id"]]["content"]:
                    if x["typename"] == "TextInline":
                        container_ele.append(
                            content_service[x["id"]].get("text", "")
                            or content_service[x["id"]].get("text@stripHtml", "")
                        )
                new_soup.body.article.append(container_ele)
            elif content_type == "ListBlock":
                list_block = content_service[c["id"]]
                if list_block["style"] == "UNORDERED":
                    container_ele = new_soup.new_tag("ul")
                else:
                    container_ele = new_soup.new_tag("ol")
                for x in content_service[c["id"]]["content"]:
                    li_ele = new_soup.new_tag("li")
                    for y in content_service[x["id"]]["content"]:
                        if y["typename"] == "ParagraphBlock":
                            para_ele = new_soup.new_tag("p")
                            for z in content_service.get(y["id"], {}).get(
                                "content", []
                            ):
                                para_ele.append(
                                    content_service.get(z["id"], {}).get("text", "")
                                )
                            li_ele.append(para_ele)
                    container_ele.append(li_ele)
                new_soup.body.article.append(container_ele)
            elif content_type == "PullquoteBlock":
                container_ele = new_soup.new_tag("blockquote")
                for x in content_service[c["id"]]["quote"]:
                    if x["typename"] == "TextInline":
                        container_ele.append(content_service[x["id"]]["text"])
                    if x["typename"] == "ParagraphBlock":
                        para_ele = new_soup.new_tag("p")
                        for z in content_service.get(x["id"], {}).get("content", []):
                            para_ele.append(
                                content_service.get(z["id"], {}).get("text", "")
                            )
                        container_ele.append(para_ele)
                new_soup.body.article.append(container_ele)
            elif content_type == "VideoBlock":
                container_ele = new_soup.new_tag("div", attrs={"class": "embed"})
                container_ele.string = "[Embedded video available]"
                new_soup.body.article.append(container_ele)
            elif content_type == "AudioBlock":
                container_ele = new_soup.new_tag("div", attrs={"class": "embed"})
                container_ele.string = "[Embedded audio available]"
                new_soup.body.article.append(container_ele)
            elif content_type == "BylineBlock":
                # For podcasts? - TBD
                pass
            elif content_type == "YouTubeEmbedBlock":
                container_ele = new_soup.new_tag("div", attrs={"class": "embed"})
                yt_link = f'https://www.youtube.com/watch?v={content_service[c["id"]]["youTubeId"]}'
                a_ele = new_soup.new_tag("a", href=yt_link)
                a_ele.string = yt_link
                container_ele.append(a_ele)
                new_soup.body.article.append(container_ele)
            elif content_type == "TwitterEmbedBlock":
                container_ele = new_soup.new_tag("div", attrs={"class": "embed"})
                container_ele.append(BeautifulSoup(content_service[c["id"]]["html"]))
                new_soup.body.article.append(container_ele)
            elif content_type == "LabelBlock":
                container_ele = new_soup.new_tag("h4", attrs={"class": "label"})
                for x in content_service[c["id"]]["content"]:
                    if x["typename"] == "TextInline":
                        container_ele.append(content_service[x["id"]]["text"])
                new_soup.body.article.append(container_ele)
            elif content_type == "SummaryBlock":
                container_ele = new_soup.new_tag("div", attrs={"class": "summary"})
                for x in content_service[c["id"]]["content"]:
                    if x["typename"] == "TextInline":
                        container_ele.append(content_service[x["id"]]["text"])
                new_soup.body.article.append(container_ele)
            elif content_type == "TimestampBlock":
                timestamp_val = content_service[c["id"]]["timestamp"]
                container_ele = new_soup.new_tag(
                    "time", attrs={"data-timestamp": timestamp_val}
                )
                container_ele.append(timestamp_val)
                new_soup.body.article.append(container_ele)
            elif content_type == "RuleBlock":
                new_soup.body.article.append(new_soup.new_tag("hr"))
            else:
                self.log.warning(f"{url} has unexpected element: {content_type}")
                self.log.debug(json.dumps(c))
                self.log.debug(json.dumps(content_service[c["id"]]))

        return str(new_soup)

    def preprocess_raw_html(self, raw_html, url):
        info = None
        soup = BeautifulSoup(raw_html)

        for script in soup.find_all("script"):
            if not script.contents:
                continue
            if not script.contents[0].strip().startswith("window.__preloadedData"):
                continue
            article_js = re.sub(
                r"window.__preloadedData\s*=\s*", "", script.contents[0].strip()
            )
            if article_js.endswith(";"):
                article_js = article_js[:-1]
            article_js = article_js.replace(":undefined", ":null")
            try:
                info = json.loads(article_js)
                break
            except json.JSONDecodeError:
                self.log.exception("Unable to parse preloadedData")

        if not info:
            self.log(f"Unable to find article from script in {url}")
            return raw_html

        html_output = """<html><head><title></title></head>
        <body>
            <article>
            <h1 class="headline"></h1>
            <div class="sub-headline"></div>
            <div class="article-meta">
                <span class="author"></span>
                <span class="published-dt"></span>
            </div>
            </article>
        </body></html>
        """

        if info.get("initialState"):
            # Seems limited to "live" articles
            return self.preprocess_initial_state(html_output, info, raw_html, url)

        if (info.get("initialData", {}) or {}).get("data", {}).get("article"):
            return self.preprocess_initial_data(html_output, info, raw_html, url)

        # Sometimes the page does not have article content in the <script>
        # particularly in the Sports section, so we fallback to
        # raw_html and rely on remove_tags to clean it up
        self.log(f"Unable to find article from script in {url}")
        return raw_html
