import os
from datetime import timedelta

# 生成適合加密使用的大小24字節的字符串
SECRET_KEY = os.urandom(24)

# session.permanent=True的情况下的期限(remember me)
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

# 項目根路徑
BASE_DIR = os.path.dirname(__file__)

# 數據庫
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'pet'

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False


## token過期時間設定
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
## token位置設定
JWT_TOKEN_LOCATION = ['headers', 'query_string']

## 每頁數據量
PER_PAGE_COUNT = 10
