# coffee chat venti の開発の手はず

## Prerequisites

最初に`pip install python-dotenv`で、環境変数を`.env`ファイルから読み込むためのモジュールを入れる

## 実行

後は`python index.py`を実行し、`curl localhost:5000`を叩くと、かりんと Colla のグループトークに対して`Hello World`が送られる

## 簡単な説明

環境変数の仕組みとしては以下の通り

1. `index.py`上部で`config`ファイルを読み込み
2. `config`ファイルで`load_dotenv(override=True)`で、`.env`ファイルを読み込むように設定
3. `SLACK_API_TOKEN`変数は、`.env`ファイルから取得する

`curl localhost:5000`を叩いた後の挙動の大まかな流れとしては、

1. `app.add_routes([web.get("/", handle_requests)])`でパスが`/`の場合を拾う
2. `handle_requests`関数を実行
3. その内部で`post_message`を実行
4. グループトークをオープン
5. オープンしたグループトークに対して、メッセージを投げる

## 開発について

4 つのグループそれぞれに誰が入るのか、ということを事前に分けるということは、それぞれ振り分けられるユーザの ID を手作業で４つのグループに予め分けるということが必要になると予想されるので、そこだけが少し面倒そう

また、今後卒業等で入れ替わりが発生すると思われるので、その際に面倒にならないように工夫ができると良いかも？（やり方は思いつかないが…）

また、Slack の API についてのドキュメントは以下に詳しく載っているので、よくわからなかったら見ると良いと思う

[Web API methods](https://api.slack.com/methods)

今回使う API は

- conversations.open
- chat.postMessagee
- users.list

ぐらいかな？

また、今回は手っ取り早く、`.env`ファイルも含めてzipファイルにして渡しているが、
`.env`ファイルは基本的に外部に見せないようにすること

