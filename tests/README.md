# テストコード用ディレクトリ

ここはテスト用のディレクトリです。
PyTestとSQLAlchemyを使用して、データベースのテストを行います。

# テストの実行方法

## 必要なもの

- Docker環境
    - Docker composeが使えること

## テスト方法

1. 接続情報を生成するために、以下のコマンドを実行してください
    ```bash
    $ bash ./makeenv.sh
    ```
2. テストを実行します、DBを起動して、テストコンテナを起動します。
    ```bash
    $ docker compose up --build -d
    $ docker compose exec shell uv run pytest
    $ docker compose down -v --rmi all
    ```
    