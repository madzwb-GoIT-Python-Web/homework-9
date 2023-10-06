import scrapy

from multiprocessing import Pool
from multiprocessing import Process
from scrapy.crawler import CrawlerProcess


def scrap_with_spider(spider: scrapy.Spider):
    process = CrawlerProcess()
    process.crawl(spider)
    process.start()

def scrap(spiders):
    with Pool() as pool:
        pool.map(scrap_with_spider, spiders)
        pool.join()
    # pr1 = Process(target=scrap_with_spider, args=(QuotesSpider,))
    # pr2 = Process(target=scrap_with_spider, args=(AuthorsSpider,))
    # pr1.start()
    # pr2.start()
    # pr1.join()
    # pr2.join()