import os
# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv
# OSの環境変数設定で、すでに同じ名前の変数が定義されている場合はそちらが優先して使われてしまうため、overrideで、.envファイルで設定した値を優先して使うようにする
load_dotenv(override=True)

# 環境変数を参照
SLACK_API_TOKEN = os.getenv('SLACK_API_TOKEN')
