import scrapy
from scrapy_intro.items import ScrapyIntroItem

class QuotesSpider(scrapy.Spider):
    name = "about_author"
    start_urls = [
        "https://quotes.toscrape.com/",
    ]

    def parse(self, response):

        for about in response.css('div.quote'):
            about_author = about.css('div.quote a::attr(href)').get()
            full_author_link = f"https://quotes.toscrape.com/{about_author}"
            yield response.follow(full_author_link, callback=self.parse_data)

        next_page = response.css("nav li.next a::attr(href)").get()
        if next_page:
            next_full_link = f"https://quotes.toscrape.com/{next_page}"
            yield response.follow(next_full_link, callback=self.parse)

    def parse_data(self, response):
        author_bio = ScrapyIntroItem()
        author_bio['author_name'] = response.css('h3.author-title::text').get()
        author_bio['author_birth_date'] = response.css('span.author-born-date::text').get()
        author_bio['author_birth_loc'] = response.css('span.author-born-location::text').get()
        author_bio['author_description'] = response.css('div.author-description::text').get()
        yield author_bio

