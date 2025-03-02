from sqlalchemy import create_engine

# 接続情報を変数で定義
username = "cipher"
password = "password"  # パスワードがある場合は入力
host = "localhost"
port = 5432
database = "cipher"

# PostgreSQL の接続情報
DB_URL = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"

# SQLAlchemy エンジンを作成
engine = create_engine(DB_URL, echo=True)  # `echo=True` でSQLログを表示

# 接続確認
try:
    with engine.connect() as conn:
        print("データベースに接続成功！")
except Exception as e:
    print("データベース接続に失敗:", e)