# 🧠 Scrapy_Demo - 东方财经网

## 😃😃使用Python的Scrapy库对于东方财经网的沪深京个股的当前信息进行爬取

运行 *** stocks_info/stocks_info/spiders/__init__.py *** 即可运行整个项目。注意：它使用了动态加载技术，所以我们相应地需要使用 Selenium 库进行处理。

## 😆😆Use the Scrapy library of Python to crawl the current information of individual stocks in Shanghai, Shenzhen and Beijing on the Oriental Finance Network.

Run *** stocks_info/stocks_info/spiders/__init__.py *** to run the entire project

## Code Structure
代码的整体结构如下图：

![image](https://github.com/Jerome-ovo/Scrapy_Demo-eastmoney.com/blob/main/img/structure.png)

# 🧠 Details
下面对于项目细节进行说明：
### StockSpider类中方法概览

- `__init__(self)`: 初始化
- `start_requests(self)`: 发送请求
- `close_ad(self)`: 关闭弹出广告
- `parse(self, response)`: 解析数据并分页
- `convert_percent_to_float(percent_str)`: 转换百分比字符串为浮动类型
- `convert_to_numeric(value)`: 转换单位为万/亿的字符串为数值
- `extract_stock_data(self, response)`: 获取并保存 HTML 数据
- `save_to_csv(self, rank, name, code, price, percent, range, volume, amount, amplitude)`: 保存数据到 CSV
- `save_to_mysql(self, rank, name, code, price, percent, my_range, volume, amount, amplitude)`: 保存数据到 MySQL（请修改用户名和密码）


# 🧠 Requirements
### Python 3 以上，安装了 Scrapy、Pymysql、Selenium 即可，但是以防万一，我还是在这里给出详细的版本信息：
| Package        | Version |
|----------------|---------|
| Python         | 3.11.8  |
| Scrapy         | 2.12.0  |
| Pymysql        | 1.4.6   |
| Selenium       | 4.31.0  |

# 🧠 Result
示例网站数据位置（东方财经网的沪深京个股）：
![image](https://github.com/Jerome-ovo/Scrapy_Demo-eastmoney.com/blob/main/img/data_position.png)
运行：
![image](https://github.com/Jerome-ovo/Scrapy_Demo-eastmoney.com/blob/main/img/running.png)
csv数据存储：
![image](https://github.com/Jerome-ovo/Scrapy_Demo-eastmoney.com/blob/main/img/data_csv.png)
sql数据存储：
![image](https://github.com/Jerome-ovo/Scrapy_Demo-eastmoney.com/blob/main/img/data_sql.png)








