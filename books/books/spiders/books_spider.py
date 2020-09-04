import scrapy

from books.items import BooksItem


class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = [
        'http://books.toscrape.com/index.html'
    ]

    def parse(self, response, **kwargs):
        if not response.css(".h1").xpath('./a/text()').get():
            yield scrapy.Request(url=response.url, dont_filter=True)

        product_urls = response.css('article.product_pod a').xpath('@href').getall()
        for prod_href in product_urls:
            url = response.urljoin(prod_href)
            request = scrapy.Request(url, callback=self.parse_book_detail)
            yield request
        next_page = response.css('li.next a').xpath('@href').get()
        if next_page is None:
            yield None
        yield response.follow(next_page, self.parse)

    def parse_book_detail(self, response):
        if not response.css(".h1").xpath('./a/text()').get():
            yield scrapy.Request(url=response.url, dont_filter=True)
        item = BooksItem()
        item['title'] = response.xpath('//h1/text()').get()
        item['description'] = response.css('.product_page').xpath('./p/text()').get()
        item['price'] = response.css('.price_color::text').get()
        item['UPC'] = response.css('tr td::text').extract_first()
        item['rating'] = response.css('p.star-rating').xpath('./@class').get().split(' ')[1]
        yield item
