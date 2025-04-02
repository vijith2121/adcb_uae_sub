import scrapy
# from adcb_uae_sub.items import Product
from lxml import html

class Adcb_uae_subSpider(scrapy.Spider):
    name = "adcb_uae_sub"
    start_urls = ["https://example.com"]

    def parse(self, response):
        parser = html.fromstring(response.text)
        print("Visited:", response.url)
