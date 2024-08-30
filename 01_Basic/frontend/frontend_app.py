import requests
import chainlit as cl

# APIのエンドポイントURL
API_URL = "http://127.0.0.1:9000/chat"


@cl.on_message
async def handle_message(user_message: cl.Message):
    # APIにリクエストを送信
    response = requests.get(
        API_URL,
        params={"question": user_message.content},
    )

    # レスポンスからanswerを取得（取得できない場合は"No answer"を使用）
    answer = response.json().get("answer", "No answer")

    # 応答をチャットに送信
    await cl.Message(answer).send()
