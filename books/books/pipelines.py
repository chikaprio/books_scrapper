
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class BooksPipeline:
    def open_spider(self, spider):
        self.file = open('books.csv', 'w+b')
        self.export = CsvItemExporter(self.file, include_headers_line=True)
        self.export.start_exporting()

    def close_spider(self, spider):
        self.export.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.export.export_item(item)
        return item
