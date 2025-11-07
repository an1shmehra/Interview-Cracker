# scraper/gfg_spider.py
import scrapy
import yaml
import json
import hashlib
import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse
from items import QuestionItem

def fingerprint(title, body_text):
    h = hashlib.sha256()
    h.update((title or "").strip().lower().encode("utf-8"))
    h.update((body_text or "").strip().lower().encode("utf-8"))
    return h.hexdigest()

def try_select_first(response, selector_string):
    """Try comma-separated CSS selectors, return first matched SelectorList."""
    for sel in [s.strip() for s in selector_string.split(",") if s.strip()]:
        res = response.css(sel)
        if res:
            return res
    return None

def recursive_find_key(obj, keyname):
    """Recursively search dict/list for first occurrence of keyname (case-insensitive)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() == keyname.lower():
                return v
            found = recursive_find_key(v, keyname)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for elt in obj:
            found = recursive_find_key(elt, keyname)
            if found is not None:
                return found
    return None

class GFGSpider(scrapy.Spider):
    name = "gfg_spider"

    def start_requests(self):
        cfg_path = Path(__file__).parent / "sources.yaml"
        cfg = yaml.safe_load(cfg_path.read_text())
        self.meta_cfg = cfg.get("meta", {})
        self.sources = cfg.get("sources", {})
        self.gfg = self.sources.get("geeksforgeeks", {})
        self.base_url = self.gfg.get("base_url", "https://www.geeksforgeeks.org")
        self.allowed_domains = self.gfg.get("allowed_domains", ["geeksforgeeks.org"])
        self.list_link_selector = self.gfg.get("selectors", {}).get("list_page_article_links", "")
        self.body_block_selector = self.gfg.get("selectors", {}).get("body_block", "")
        self.title_selector = self.gfg.get("selectors", {}).get("title", "h1")
        self.editorial_selector = self.gfg.get("selectors", {}).get("editorial_block", "")
        self.code_selector = self.gfg.get("selectors", {}).get("code_snippet", "pre, code")
        self.examples_selector = self.gfg.get("selectors", {}).get("examples", "pre, .example")
        self.next_data_selector = self.gfg.get("selectors", {}).get("next_data_script", "script#__NEXT_DATA__")

        start_pages = self.gfg.get("start_pages", [])
        for url in start_pages:
            yield scrapy.Request(url, callback=self.parse_start_page)

    def parse_start_page(self, response):
        # split comma-separated selectors and follow links
        for sel in [s.strip() for s in self.list_link_selector.split(",") if s.strip()]:
            for href in response.css(sel + "::attr(href)").getall():
                if not href:
                    continue
                if href.startswith("/"):
                    href = urljoin(self.base_url, href)
                # ensure same domain
                if urlparse(href).netloc.endswith("geeksforgeeks.org"):
                    yield scrapy.Request(href, callback=self.parse_problem_page)

    def parse_problem_page(self, response):
        item = QuestionItem()
        item["source"] = "GeeksforGeeks"
        item["source_url"] = response.url
        item["date_scraped"] = datetime.datetime.utcnow().strftime(self.meta_cfg.get("date_format", "%Y-%m-%dT%H:%M:%SZ"))

        # Title
        title_sel = try_select_first(response, self.title_selector)
        if title_sel:
            item["title"] = title_sel.get().strip()
            # if selector returned full tag, extract inner text
            item["title"] = " ".join(title_sel.xpath("string(.)").get().split()).strip()
        else:
            # attempt to extract from og:title or meta
            og = response.css("meta[property='og:title']::attr(content)").get()
            item["title"] = og or ""

        # Body block (html + text snippet)
        body_sel = try_select_first(response, self.body_block_selector)
        if body_sel:
            item["body_html"] = body_sel.get()
            item["body_text"] = " ".join(body_sel.xpath("string(.)").get().split())
        else:
            item["body_html"] = ""
            item["body_text"] = ""

        # Editorial block
        editorial_sel = try_select_first(response, self.editorial_selector)
        if editorial_sel:
            item["editorial_html"] = editorial_sel.get()
        else:
            item["editorial_html"] = ""

        # Code snippets
        codes = []
        for c in response.css(self.code_selector):
            text = c.xpath("string(.)").get()
            if text:
                codes.append(text.strip())
        item["code_snippets"] = codes

        # Examples: heuristics - pre blocks containing Input/Output or Example
        examples = []
        for pre in response.css(self.examples_selector):
            txt = pre.xpath("string(.)").get()
            if not txt:
                continue
            if any(k in txt for k in ["Input", "Output", "Example", "Example:", "Sample"]):
                examples.append(" ".join(txt.split()))
        item["examples"] = examples

        # Tags
        tags = response.css(".tags a::text, .problem-tags a::text, .taglist a::text").getall()
        item["tags"] = [t.strip() for t in tags if t.strip()]

        # Difficulty
        diff = response.css(".difficulty::text, .difficulty-level::text, .level::text").get()
        item["difficulty"] = diff.strip() if diff else ""

        # If title/body are missing (React page), try to parse __NEXT_DATA__
        if (not item["title"] or not item["body_text"]) :
            script_text = response.css(self.next_data_selector + '::text').get()
            if script_text:
                try:
                    js = json.loads(script_text)
                    # try common keys
                    t = recursive_find_key(js, "title") or recursive_find_key(js, "problemTitle") or recursive_find_key(js, "heading")
                    content = recursive_find_key(js, "content") or recursive_find_key(js, "articleHtml") or recursive_find_key(js, "problemStatement") or recursive_find_key(js, "body")
                    if t and not item["title"]:
                        item["title"] = t if isinstance(t, str) else str(t)
                    if content and not item["body_text"]:
                        if isinstance(content, str):
                            item["body_html"] = content
                            item["body_text"] = " ".join(content.split())
                        else:
                            item["body_text"] = str(content)
                except Exception:
                    pass

        # Fingerprint for dedupe
        item["fingerprint"] = fingerprint(item.get("title", ""), item.get("body_text", "")[:500])

        yield item
