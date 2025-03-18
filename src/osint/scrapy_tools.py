#Testing    
import scrapy # type: ignore
from scrapy.crawler import CrawlerProcess # type: ignore

# Define the spider
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

# Run the spider programmatically
if __name__ == "__main__":
    # Create a CrawlerProcess instance
    process = CrawlerProcess(settings={
        "FEEDS": {
            "quotes.json": {"format": "json"},  # Save output to quotes.json
        },
    })

    # Add the spider to the process
    process.crawl(QuotesSpider)

    # Start the crawling process
    process.start()