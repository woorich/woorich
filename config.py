import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
# db = {
#     # 데이터베이스에 접속할 사용자 아이디
#     'user': 'root',
#     # 사용자 비밀번호
#     'password': '0000',
#     # 접속할 데이터베이스의 주소 (같은 컴퓨터에 있는 데이터베이스에 접속하기 때문에 localhost)
#     'host': '127.0.0.1',
#     # 관계형 데이터베이스는 주로 3306 포트를 통해 연결됨
#     'port': '3306',
#     # 실제 사용할 데이터베이스 이름
#     'database': 'woorichi2'
# }

# SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"
print(SQLALCHEMY_DATABASE_URI)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"