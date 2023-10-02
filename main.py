import scrapy

from multiprocessing import Process
from scrapy.crawler import CrawlerProcess



class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls      = ['http://quotes.toscrape.com/']
    custom_settings = {
        "FEED_FORMAT"           : "json",
        "FEED_EXPORT_ENCODING"  : "utf-8",
        "FEED_URI"              : "data/authors.json"
    }

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            link = quote.xpath('span/a/@href').get()
            yield   response.follow(
                        url=self.start_urls[0] + link,
                        callback=self.parse_author
                    )
        link = response.xpath("/html//nav/ul[@class='pager']/li[@class='next']/a/@href").get()
        if link:
            yield scrapy.Request(url=self.start_urls[0] + link)

    def parse_author(self, response):
        content = response.xpath("/html//div[@class='author-details']")
        yield {
            "fullname"      : content.xpath("h3[@class='author-title']/text()")             .get().strip(),
            "born_date"     : content.xpath("p/span[@class='author-born-date']/text()")     .get().strip(),
            "born_location" : content.xpath("p/span[@class='author-born-location']/text()") .get().strip(),
            "description"   : content.xpath("div[@class='author-description']/text()")      .get().strip(),
        }


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls      = ['http://quotes.toscrape.com/']
    custom_settings = {
        "FEED_FORMAT"           : "json",
        "FEED_EXPORT_ENCODING"  : "utf-8",
        "FEED_URI"              : "data/quotes.json"
    }

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "quote" : quote.xpath("span[@class='text']/text()")                 .get(),
                "tags"  : quote.xpath("div[@class='tags']/a[@class='tag']/text()")  .extract(),
                "author": quote.xpath("span/small[@class='author']/text()")         .get()
            }
        link = response.xpath("/html//nav/ul[@class='pager']/li[@class='next']/a/@href").get()
        if link:
            yield scrapy.Request(url=self.start_urls[0] + link)


def scrap(spider: scrapy.Spider):
    process = CrawlerProcess()
    process.crawl(spider)
    process.start()


if __name__ == '__main__':

    pr1 = Process(target=scrap, args=(QuotesSpider,))
    pr2 = Process(target=scrap, args=(AuthorsSpider,))
    pr1.start()
    pr2.start()
    pr1.join()
    pr2.join()