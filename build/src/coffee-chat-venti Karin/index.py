from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError
from aiohttp import web
import config

client = AsyncWebClient(token=config.SLACK_API_TOKEN)

# Define this as an async function
async def post_message():
    try:
        # response = await client.users_list()
        # for member in response['members']:
        #     # print('member.name', member['name'], member['id'])

        # グループトークを開く（実際に通知はいかない）
        conversation = await client.conversations_open(            
            # 今回のVentiなら 4人をここにいれてあげればOKのはず
            # ここではCollaとかりんを指定
            users='U01FSD3EPDK,U01SBD9FX7B'
        )
        print("conversations opened")
        # IDの参考(slackから対象のProfileを開いて、Moreの部分から Copy Member IdでIDが参照できる)
        # U01SE27EDE2 Akio Inoue
        # U01SBD9FX7B Karin Nakano
        # U01FSD3EPDK Collaのアプリ

        await client.chat_postMessage(
            # オープンしたグループトークのidを指定してメッセージを送る
            channel=conversation['channel']['id'],
            # 文言は適当に
            text="Hello World"
        )

    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        raise e


async def handle_requests(request: web.Request):

    try:
        await post_message()
        return web.json_response(data={'message': 'Done!'})
    except SlackApiError as e:
        return web.json_response(data={'message': f"Failed due to {e.response['error']}"})


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([web.get("/", handle_requests)])
    # e.g., 'curl http://localhost:3000'
    web.run_app(app, host="0.0.0.0", port=5000)
