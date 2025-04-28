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
## StockSpider类中，定义方法：
### def __init__(self) 
进行初始化
### def start_requests(self) 
开始发送请求
### def close_ad(self) 
负责关闭最开始访问页面时弹出的广告（可根据实际情况调整/删除）
### def parse(self, response) 
解析页面数据，分页读取并尝试点击下一页
### def convert_percent_to_float(percent_str)
将百分比字符串转为浮动类型（例如 '9.25%' 转为 9.25）
### def convert_to_numeric(value)
将带有'万'和'亿'单位的字符串转换为相应的数值
### def extract_stock_data(self, response)
获取 HTML 响应内容（部分），并保存我们需要的数据项
### def save_to_csv(self, rank, name, code, price, percent, range, volume, amount, amplitude)
将指定的数据项保存到工作目录下的csv文件中
### def save_to_mysql(self, rank, name, code, price, percent, my_range, volume, amount, amplitude)
将指定的数据项保存到数据库中，注意修改为你的用户名和密码！

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








