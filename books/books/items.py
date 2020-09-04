import scrapy


class BooksItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    UPC = scrapy.Field()
    rating = scrapy.Field()

