import requests
import chainlit as cl

API_URL = "http://127.0.0.1:9000/chat"


@cl.on_message
async def handle_message(user_message: cl.Message):
    response = requests.get(
        API_URL, params={"question": user_message.content, "session_id": "abc123"}
    )
    answer = response.json().get("answer", "No answer")
    await cl.Message(answer).send()
