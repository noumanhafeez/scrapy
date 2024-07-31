import scrapy
from scrapy_intro.items import ScrapyIntroItem

class QuotesSpider(scrapy.Spider):
    name = "quotes_start_urls"
    start_urls = [
        "https://quotes.toscrape.com/",
    ]

    def parse(self, response):
        quote_item = ScrapyIntroItem()

        for quote in response.css('div.quote'):
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item

        next_page = response.css("nav li.next a::attr(href)").get()
        if next_page:
            full_link = f"https://quotes.toscrape.com/{next_page}"
            yield response.follow(full_link, callback=self.parse)
