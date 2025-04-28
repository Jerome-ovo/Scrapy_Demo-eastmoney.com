from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from stocks_info.stocks_info.spiders.stock_spider import StockSpider  # 修正为正确的类名

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(StockSpider)  # 使用修正后的StockSpider类
    process.start()