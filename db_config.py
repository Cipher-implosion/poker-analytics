from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 接続情報を変数で定義
# username = "cipher"   # mac
username = "postgres"   # windows
password = "password"  # パスワードがある場合は入力
host = "localhost"
port = 5432
database = "cipher"

# PostgreSQL の接続情報
DB_URL = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"

# SQLAlchemy エンジンを作成
engine = create_engine(DB_URL, echo=True)  # `echo=True` でSQLログを表示

# セッションメーカーを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)