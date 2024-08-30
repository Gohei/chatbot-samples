import httpx
import chainlit as cl

API_URL = "http://127.0.0.1:9000/chat"


@cl.on_message
async def handle_message(user_message: cl.Message):
    # 空の応答メッセージを作成する
    response_message = cl.Message(content="")

    # 非同期HTTPクライアントを使用してサーバーにリクエストを送信する
    async with httpx.AsyncClient() as client:
        # FastAPIサーバーにGETリクエストを送信し、ストリーミング応答を取得する
        async with client.stream(
            "GET",
            API_URL,
            params={"question": user_message.content, "session_id": "abc123"},
        ) as response:
            # サーバーからの応答をチャンク（分割されたテキスト）単位で受信する
            async for response_chunk in response.aiter_text():
                # 受信したチャンクをユーザーに順次表示する
                # これにより、ユーザーはリアルタイムで応答を見ることができる
                await response_message.stream_token(response_chunk)

    # メッセージ全体を表示して応答処理を完了させる
    # これにより、ストリーミングが終了したことをChainlitに通知する
    await response_message.send()
