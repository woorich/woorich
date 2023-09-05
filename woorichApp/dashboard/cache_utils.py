import redis
import pandas as pd
import json
import os
import pymysql

RDS_HOST = os.getenv('RDS_HOST')
RDS_PORT = 3306
RDS_USERNAME = os.getenv('RDS_USERNAME')
RDS_PASSWORD = os.getenv('RDS_PASSWORD')
RDS_DB_NAME1 = os.getenv('RDS_DB_NAME1')

conn = pymysql.connect(
    host=RDS_HOST,     # MySQL Server Address
    port=RDS_PORT,          # MySQL Server Port
    user=RDS_USERNAME,      # MySQL username
    passwd=RDS_PASSWORD,    # password for MySQL username
    db=RDS_DB_NAME1,   # Database name
    charset='utf8mb4'
)

# Redis 연결 설정
r = redis.Redis(host='localhost', port=6379, db=0)

def get_data(query):
    cache_key = f"sql:{query}"  # 쿼리를 기반으로 캐시 키 생성
    cached_data = r.get(cache_key)  # Redis에서 캐시 가져오기

    if cached_data:
        return pd.read_json(cached_data)  # 캐시된 데이터가 있으면 반환
    else:
        data = pd.read_sql(query, conn)
        r.setex(cache_key, 36000, data.to_json())  # 캐시에 데이터 저장, 만료시간 1시간(3600초)
        return data