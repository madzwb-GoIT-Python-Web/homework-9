
from scrapper import scrapper

from quotes_toscrape_com.spiders    import AuthorsSpider
from quotes_toscrape_com.spiders    import QuotesSpider

# from quotes_toscrape_com.spiders import AuthorsSpider, QuotesSpider


if __name__ == '__main__':
    spiders = [AuthorsSpider, QuotesSpider]
    scrapper.scrap(spiders)
