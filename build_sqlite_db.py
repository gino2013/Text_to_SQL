import sqlite3
import csv

# 連接到SQLite數據庫
conn = sqlite3.connect('medical_insurance.db')
cursor = conn.cursor()

with open('Insurance.csv', 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)
    # 創建表
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS Insurance ({','.join([' '.join([header, 'text']) for header in headers])})")
    for row in reader:
        cursor.execute(
            f"INSERT INTO Insurance VALUES ({','.join(['?' for header in headers])})", row)

# 提交事務並關閉連接
conn.commit()
conn.close()
