import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 新規: 履歴管理のためのモジュールをインポート
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)


# .envファイルから環境変数を読み込む
load_dotenv()

# OpenAI APIキーの確認
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OpenAI APIキーが設定されていません")


# プロンプトテンプレートの作成
# 変更点: chat_historyプレースホルダーの追加
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "簡潔で正確な回答を提供してください:"),
        ("placeholder", "{chat_history}"),
        ("user", "{question}"),
    ],
)

# モデルの作成
model = ChatOpenAI(model="gpt-4o-mini")


# 出力パーサーの作成
parser = StrOutputParser()


# 新規: チャット履歴を制限する関数を定義
def limit_history(messages, max_messages=10):
    return messages[-max_messages:]


# 新規: 履歴制限機能の作成
history_limiter = RunnablePassthrough.assign(
    chat_history=lambda x: limit_history(x["chat_history"])
)

# チェーンの作成
# 変更点: history_limiterの追加
chain = history_limiter | prompt_template | model | parser


# 新規: セッションごとのチャット履歴を保存する辞書を作成
histories = {}


# 新規: セッションIDに基づいてチャット履歴を取得する関数を定義
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in histories:
        histories[session_id] = InMemoryChatMessageHistory()
    return histories[session_id]


# 新規: 履歴管理機能を追加したチェーンの作成
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)


# FastAPIアプリケーションの初期化
# 変更点: タイトルの更新
app = FastAPI(title="Chat with History API")


# チャットエンドポイントの定義
# 変更点: session_idパラメータの追加とchain_with_historyの使用
@app.get("/chat")
async def get_chat_response(question: str, session_id: str = "default"):
    # 新規: セッションIDを設定
    config = {"configurable": {"session_id": session_id}}

    # 変更点: chainの代わりにchain_with_historyを使用
    answer = chain_with_history.invoke({"question": question}, config=config)
    return {"answer": answer}


# サーバーの起動
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
