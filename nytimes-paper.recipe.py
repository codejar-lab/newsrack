#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2018, Kovid Goyal <kovid at kovidgoyal.net>

# Original at https://github.com/kovidgoyal/calibre/blob/8597c509ed04f7435246f84ddf3e10a0227ccc7e/recipes/nytimes_sub.recipe

from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import re
import json
from pprint import pprint  # noqa

from calibre import strftime
from calibre.utils.date import strptime
from calibre.web.feeds.news import BasicNewsRecipe
from calibre.ebooks.BeautifulSoup import BeautifulSoup


class NewYorkTimesPrint(BasicNewsRecipe):

    title = "The New York Times - Print"
    description = "Today's New York Times"
    encoding = "utf-8"
    __author__ = "Kovid Goyal"
    language = "en"
    publication_type = "newspaper"
    masthead_url = "https://mwcm.nyt.com/.resources/mkt-wcm/dist/libs/assets/img/logo-nyt-header.svg"
    ignore_duplicate_articles = {"title", "url"}
    no_stylesheets = True
    compress_news_images = True
    compress_news_images_auto_size = 5
    scale_news_images = (800, 800)
    scale_news_images_to_device = False  # force img to be resized to scale_news_images
    timefmt = ""
    pub_date = None  # custom publication date

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
        dict(name=["script", "noscript", "style", "button"]),
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
    .sub-headline { font-size: 1rem; margin-bottom: 1rem; }
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

    def publication_date(self):
        return self.pub_date

    def preprocess_raw_html(self, raw_html, url):
        info = None
        soup = BeautifulSoup(raw_html)

        for script in soup.find_all("script"):
            if not script.text.strip().startswith("window.__preloadedData"):
                continue
            article_js = re.sub(
                r"window.__preloadedData\s*=\s*", "", script.text.strip()
            )
            if article_js.endswith(";"):
                article_js = article_js[:-1]
            article_js = article_js.replace(":undefined", ":null")
            info = json.loads(article_js)
            break

        if not (info and info.get("initialState")):
            # Sometimes the page does not have article content in the <script>
            # particularly in the Sports section, so we fallback to
            # raw_html and rely on remove_tags to clean it up
            self.log(f"Unable to find article from script in {url}")
            return raw_html

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
            self.log(f"Unable to find content in article object")
            return raw_html

        html_output = f"""<html><head><title></title></head>
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
        new_soup = BeautifulSoup(html_output, "html.parser")

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

    def read_todays_paper(self):
        INDEX = "https://www.nytimes.com/section/todayspaper"
        try:
            soup = self.index_to_soup(INDEX)
        except Exception as err:
            if getattr(err, "code", None) == 404:
                try:
                    soup = self.index_to_soup(
                        strftime(
                            "https://www.nytimes.com/issue/todayspaper/%Y/%m/%d/todays-new-york-times"
                        )
                    )
                except Exception as err:
                    if getattr(err, "code", None) == 404:
                        dt = datetime.datetime.today() - datetime.timedelta(days=1)
                        soup = self.index_to_soup(
                            dt.strftime(
                                "https://www.nytimes.com/issue/todayspaper/%Y/%m/%d/todays-new-york-times"
                            )
                        )
                    else:
                        raise
            else:
                raise
        return soup

    def read_nyt_metadata(self):
        soup = self.read_todays_paper()
        pdate = soup.find("meta", attrs={"name": "pdate", "content": True})["content"]
        date = strptime(pdate, "%Y%m%d", assume_utc=False, as_utc=False)
        self.cover_url = (
            "https://static01.nyt.com/images/{}/nytfrontpage/scan.jpg".format(
                date.strftime("%Y/%m/%d")
            )
        )
        # self.timefmt = strftime(" [%d %b, %Y]", date)
        self.pub_date = date
        self.title = f"NY Times (Print): {date:%-d %b, %Y}"
        return soup

    def parse_todays_page(self):
        soup = self.read_nyt_metadata()
        script = soup.findAll(
            "script", text=lambda x: x and "window.__preloadedData" in x
        )[0]
        script = type("")(script)
        json_data = script[script.find("{") : script.rfind(";")].strip().rstrip(";")
        data = json.loads(json_data.replace(":undefined", ":null"))["initialState"]
        containers, sections = {}, {}
        article_map = {}
        gc_pat = re.compile(r"groupings.(\d+).containers.(\d+)")
        pat = re.compile(r"groupings.(\d+).containers.(\d+).relations.(\d+)")
        for key in data:
            if "Article" in key:
                adata = data[key]
                if adata.get("__typename") == "Article":
                    url = adata.get("url")
                    summary = adata.get("summary")
                    headline = adata.get("headline")
                    if url and headline:
                        title = data[headline["id"]]["default"]
                        article_map[adata["id"]] = {
                            "title": title,
                            "url": url,
                            "description": summary or "",
                        }
            elif "Legacy" in key:
                sdata = data[key]
                tname = sdata.get("__typename")
                if tname == "LegacyCollectionContainer":
                    m = gc_pat.search(key)
                    containers[int(m.group(2))] = sdata["label"] or sdata["name"]
                elif tname == "LegacyCollectionRelation":
                    m = pat.search(key)
                    grouping, container, relation = map(int, m.groups())
                    asset = sdata["asset"]
                    if asset and asset["typename"] == "Article" and grouping == 0:
                        if container not in sections:
                            sections[container] = []
                        sections[container].append(asset["id"].split(":", 1)[1])

        feeds = []
        for container_num in sorted(containers):
            section_title = containers[container_num]
            if container_num in sections:
                articles = sections[container_num]
                if articles:
                    feeds.append((section_title, []))
                    for artid in articles:
                        if artid in article_map:
                            art = article_map[artid]
                            feeds[-1][1].append(art)

        def skey(x):
            name = x[0].strip()
            if name == "The Front Page":
                return 0, ""
            return 1, name.lower()

        feeds.sort(key=skey)
        for section, articles in feeds:
            self.log("\n" + section)
            for article in articles:
                self.log(article["title"] + " - " + article["url"])
        return feeds

    def parse_index(self):
        return self.parse_todays_page()

    # The NYT occassionally returns bogus articles for some reason just in case
    # it is because of cookies, dont store cookies
    def get_browser(self, *args, **kwargs):
        return self

    def clone_browser(self, *args, **kwargs):
        return self.get_browser()

    def open_novisit(self, *args, **kwargs):
        from calibre import browser, random_user_agent

        if not hasattr(self, "rua_stored"):
            self.rua_stored = random_user_agent(allow_ie=False)
        br = browser(user_agent=self.rua_stored)
        response = br.open_novisit(*args, **kwargs)
        return response

    open = open_novisit
