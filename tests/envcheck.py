import os

def get_database_url():
    """接続情報からDBのURLを生成する
    """
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")
    MYSQL_HOST = os.environ.get("MYSQL_HOST")
    MYSQL_USER = os.environ.get("MYSQL_USER")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    DBURL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
    print(f"Using database URL: {DBURL}")
    print(f"""
          MYSQL_DATABASE: {MYSQL_DATABASE}
          MYSQL_HOST: {MYSQL_HOST}
          MYSQL_USER: {MYSQL_USER}
          MYSQL_PASSWORD: {MYSQL_PASSWORD}
    """)
    return DBURL

if __name__ == "__main__":
    get_database_url()