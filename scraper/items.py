# scraper/items.py
import scrapy

class QuestionItem(scrapy.Item):
    title = scrapy.Field()
    body_html = scrapy.Field()
    body_text = scrapy.Field()
    editorial_html = scrapy.Field()
    code_snippets = scrapy.Field()
    examples = scrapy.Field()
    tags = scrapy.Field()
    difficulty = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    date_scraped = scrapy.Field()
    fingerprint = scrapy.Field()
