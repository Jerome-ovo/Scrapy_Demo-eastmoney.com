import scrapy
import csv
import pymysql
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class StockSpider(scrapy.Spider):
    name = 'stock_spider'
    allowed_domains = ['eastmoney.com']
    start_urls = ['https://quote.eastmoney.com/center/gridlist.html#hs_a_board']  # 目标网页链接

    def __init__(self):
        self.ad_closed = False  # 初始化广告关闭标志
        self.driver = webdriver.Chrome()  # 这里使用 ChromeDriver，也可以使用其他浏览器驱动

    def start_requests(self):
        start_urls = 'https://quote.eastmoney.com/center/gridlist.html#hs_a_board'
        self.driver.get(start_urls)

        # 获取渲染后的 HTML
        body = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')
        self.parse(response)

    def close_ad(self):
        if not self.ad_closed:  # 只在第一次进入页面时关闭广告
            try:
                # 查找广告关闭按钮
                ad_close_button = self.driver.find_element(By.CSS_SELECTOR,
                         'img[src="https://emcharts.dfcfw.com/fullscreengg/ic_close.png"]')
                # 点击关闭按钮
                ad_close_button.click()
                self.logger.info("广告关闭成功")
                self.ad_closed = True  # 设置广告已关闭标志
            except Exception as e:
                self.logger.warning("没有找到广告关闭按钮或点击失败: " + str(e))
        else:
            self.logger.info("广告已经关闭，不再重复操作。")

    def parse(self, response):
        # 关闭广告
        self.close_ad()

        # 获取当前页面的股票数据
        self.extract_stock_data(response)

        # 查找并点击“下一页”按钮
        try:
            # 使用显式等待，直到按钮可点击
            next_page_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@title="下一页"]'))
            )
            # 滚动页面到按钮的位置
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
            # 点击“下一页”
            next_page_button.click()
            time.sleep(2)  # 等待页面加载
            body = self.driver.page_source
            response = HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')
            self.parse(response)  # 递归调用，爬取下一页
        except Exception as e:
            self.logger.info("没有更多分页，爬取结束。")
            return

    # 将百分比字符串转为浮动类型（例如 '9.25%' 转为 9.25）
    @staticmethod
    def convert_percent_to_float(percent_str):
        if isinstance(percent_str, str) and '%' in percent_str:
            return float(percent_str.replace('%', ''))  # 移除百分号并转换为浮动类型
        return float(percent_str)  # 如果已经是数字，直接返回

    @staticmethod
    def convert_to_numeric(value):
        """
        将带有'万'和'亿'单位的字符串转换为相应的数值。
        """
        if isinstance(value, str):
            if '万' in value:
                return float(value.replace('万', '')) * 10000  # 将'万'转为数字
            elif '亿' in value:
                return float(value.replace('亿', '')) * 100000000  # 将'亿'转为数字
        # 如果是纯数字字符串，直接转为float
        return float(value)

    def extract_stock_data(self, response):
        # 打印 HTML 响应内容（部分）
        # print(response.body.decode('utf-8')[:1000])  # 手动解码为字符串并显示前1000个字符

        # 获取所有股票的数据行
        rows = response.css('div.main div#mainpage.mainlc.scf div#mainc div '
                            'div.pagehsj div.quotetable table tbody tr')  # 通过 class 选择器定位表格和 tbody

        for row in rows[:]:
            # 提取各个字段
            rank = row.css('td:nth-child(1)::text').get()  # 排名
            stock_code = row.css('td:nth-child(2) a::text').get()  # 股票代码
            stock_name = row.css('td:nth-child(3) a::text').get()  # 股票名称
            price = row.css('td:nth-child(5) span::text').get()  # 价格
            percent = row.css('td:nth-child(6) span::text').get()  # 涨幅
            range = row.css('td:nth-child(7) span::text').get()  # 涨跌额度
            volume = row.css('td:nth-child(8) span::text').get()  # 成交量（手）
            amount = row.css('td:nth-child(9) span::text').get()  # 成交额
            amplitude = row.css('td:nth-child(10) span::text').get()  # 振幅
            # url
            stock_url = row.css('td:nth-child(2) a::attr(href)').get()  # 股票链接
            guba_url = row.css('td:nth-child(4) a:nth-child(1)::attr(href)').get()  # 股吧链接
            zjlx_url = row.css('td:nth-child(4) a:nth-child(2)::attr(href)').get()  # 资金流链接
            stock_data_url = row.css('td:nth-child(4) a:nth-child(3)::attr(href)').get()  # 数据链接

            # 处理数据为空的情况
            if None in [rank, stock_code, stock_name, stock_url, guba_url, zjlx_url, stock_data_url, price, percent,
                        volume, range, amount, amplitude]:
                continue

            # 打印爬取的股票数据
            # self.logger.info(
            #     f"爬取的股票：索引：{rank}：{stock_name}, 代码：{stock_code}, 当前价：{price}, 涨跌幅：{percent}, "
            #     f"涨跌额度：{range}, 成交量（手）：{volume}, 成交额：{amount}, 振幅：{amplitude}")
            # print(
            #     f"爬取的股票：索引：{rank}：{stock_name}, 代码：{stock_code}, 当前价：{price}, 涨跌幅：{percent}, "
            #     f"涨跌额度：{range}, 成交量（手）：{volume}, 成交额：{amount}, 振幅：{amplitude}")

            # 保存到 CSV 文件
            self.save_to_csv(rank, stock_name, stock_code, price, percent, range, volume, amount, amplitude)

            # 百分数 -> 去掉百分号
            percent = self.convert_percent_to_float(percent)
            amplitude = self.convert_percent_to_float(amplitude)
            # 转换为数字
            volume = self.convert_to_numeric(volume)
            amount = self.convert_to_numeric(amount)
            # 保存到 MySQL 数据库
            self.save_to_mysql(rank, stock_name, stock_code, price, percent, range, volume, amount, amplitude)

    def save_to_csv(self, rank, name, code, price, percent, range, volume, amount, amplitude):
        with open('stocks.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['index', 'stock_name', 'stock_code', 'price', 'percent', 'range', 'volume', 'amount', 'amplitude']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(
                {'index': rank, 'stock_name': name, 'stock_code': code, 'price': price, 'percent': percent,
                 'range': range, 'volume': volume, 'amount': amount, 'amplitude': amplitude})

    def save_to_mysql(self, rank, name, code, price, percent, my_range, volume, amount, amplitude):
        connection = None
        cursor = None
        try:
            # 建立数据库连接
            connection = pymysql.connect(
                host='localhost',
                database='stocks_db',  # 确保 MySQL 数据库已创建
                user='root',
                password='123456'
            )
            # 创建一个游标对象
            cursor = connection.cursor()
            print(f"Executing SQL: INSERT INTO stock_prices (rank_position, stock_name, "
                  f"stock_code, price, percent, myRange, volume, amount, amplitude) VALUES "
                  f"({rank}, {name}, {code}, {price}, {percent}, {my_range}, {volume}, {amount}, {amplitude})")
            # 执行插入语句
            cursor.execute("""
                INSERT INTO stock_prices (rank_position, stock_name, stock_code, price, percent, myRange, volume, amount, amplitude)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (rank, name, code, price, percent, my_range, volume, amount, amplitude))
            # 提交事务
            connection.commit()
        except pymysql.MySQLError as err:
            print(f"################ Error: {err}")
            self.logger.error(f"Error while connecting to MySQL: {err}")
        finally:
            # 关闭游标和连接
            if cursor:
                cursor.close()
            if connection:
                connection.close()
