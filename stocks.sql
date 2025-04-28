CREATE DATABASE stocks_db;

USE stocks_db;

CREATE TABLE stock_prices (
    rank_position INT,                      -- 排名
    stock_code VARCHAR(20),                  -- 股票代码
    stock_name VARCHAR(255),                 -- 股票名称
    price DECIMAL(10, 2),                    -- 价格，保留两位小数
    percent DECIMAL(5, 2),                   -- 涨幅，保留两位小数
    myRange DECIMAL(10, 2),                    -- 涨跌额度，保留两位小数
    volume BIGINT,                           -- 成交量（手），使用 BIGINT 处理大数字
    amount DECIMAL(15, 2),                   -- 成交额，保留两位小数
    amplitude DECIMAL(5, 2)                  -- 振幅，保留两位小数
);


