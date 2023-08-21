import dotenv
import os
from flask_wtf.csrf import CSRFProtect

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)  # .env 파일 로드

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')  # .env 파일에서 SECRET_KEY 가져오기
    WTF_CSRF_SECRET_KEY = SECRET_KEY  
    # Debug print statements
    print("SECRET_KEY:", SECRET_KEY)
    print("WTF_CSRF_SECRET_KEY:", WTF_CSRF_SECRET_KEY)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.environ.get('RDS_USERNAME')}:{os.environ.get('RDS_PASSWORD')}@{os.environ.get('RDS_HOST')}:{os.environ.get('RDS_PORT', 3306)}/{os.environ.get('RDS_DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
class ProductionConfig(Config):
    DEBUG = False
    # 다른 환경에 대한 설정 추가
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
# 기본 설정: 개발 환경 설정으로 설정합니다.
app_config = DevelopmentConfig

# CSRF 보호 활성화
csrf = CSRFProtect()