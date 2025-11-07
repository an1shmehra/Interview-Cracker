# scraper/settings.py
BOT_NAME = "interview_cracker"
SPIDER_MODULES = ["scraper"]
NEWSPIDER_MODULE = "scraper"

ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1.5
TELNETCONSOLE_ENABLED = False
ITEM_PIPELINES = {
    "scraper.pipelines.SQLitePipeline": 300,
}
LOG_LEVEL = "INFO"
