import pymysql

# 建立数据库连接
try:
    db_connection = pymysql.connect(
        host="localhost",       # 数据库主机地址
        user="root",            # 数据库用户名
        password="123456",      # 数据库密码
        database="stocks_db"    # 数据库名称
    )
    print("数据库连接成功！")

    # 创建一个游标对象
    cursor = db_connection.cursor()

    # 准备插入数据
    rank = 1
    name = 'Sample Stock'
    code = '000001'
    price = 20.5
    percent = 3.4
    range = 0.5
    volume = 10000
    amount = 200000
    amplitude = 2.5

    # 执行插入语句
    insert_query = """
        INSERT INTO stock_prices (rank_position, stock_name, stock_code, price, percent, myRange, volume, amount, amplitude)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (rank, name, code, price, percent, range, volume, amount, amplitude))

    # 提交事务
    db_connection.commit()
    print("数据插入成功！")

except pymysql.MySQLError as e:
    print(f"数据库操作错误: {e}")

finally:
    # 关闭游标和连接
    if cursor:
        cursor.close()
    if db_connection:
        db_connection.close()
