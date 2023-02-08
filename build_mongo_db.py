import pandas as pd
import pymongo

# 讀取 CSV 文件
df = pd.read_csv("insurance.csv")

# 連接到 MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# 創建資料庫
mydb = client["Mongo"]

# 創建集合
insurance = mydb["insurance"]

# 將數據框中的文件插入到集合中
records = df.to_dict("records")
insurance.insert_many(records)

# 查詢文件
for x in insurance.find():
  print(x)
