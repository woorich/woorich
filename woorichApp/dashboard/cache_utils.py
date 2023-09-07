import redis
import pandas as pd
import json
import os
import pymysql
# from io import StringIO
import pickle

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
try:
    r = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=100)
    if r.ping() is False:
        raise ConnectionError("Redis 서버에 연결할 수 없습니다.")
except redis.ConnectionError as e:
    print(f"Redis 연결 에러: {e}")
    r = None

def get_data(query: str) -> pd.DataFrame:
    cache_key = f"{query}"

    if r:
        try:
            cached_data = r.get(cache_key)
            if cached_data:
                # return pd.read_json(StringIO(cached_data.decode('utf-8')))
                return pickle.loads(r.get(cache_key))
        except redis.ConnectionError as e:
            print(f"Redis 연결 에러1: {e}")

    try:
        data = pd.read_sql(query, conn)
        if r:
            try:
                # r.setex(cache_key, 36000, data.to_json())
                r.set(cache_key, pickle.dumps(data))
            except redis.ConnectionError as e:
                print(f"Redis 연결 에러2: {e}")
        return data
    except pymysql.MySQLError as e:
        print(f"MySQL 에러: {e}")
        return pd.DataFrame()