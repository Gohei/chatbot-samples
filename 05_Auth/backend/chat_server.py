import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse  # 新規: StreamingResponseのインポート
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 履歴管理のためのモジュールをインポート
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)

# ベクトルストアと埋め込み生成のためのモジュールをインポート
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


# .envファイルから環境変数を読み込む
load_dotenv()

# OpenAI APIキーの確認
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OpenAI APIキーが設定されていません")


# プロンプトテンプレートの作成
system_template = "以下の情報を最優先に参考にし、質問に対して回答を提供してください。一般的な知識や事前の学習内容は使わないでください: {context}"
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("placeholder", "{chat_history}"),
        ("user", "{question}"),
    ],
)

# モデルの作成
model = ChatOpenAI(model="gpt-4o-mini")


# 出力パーサーの作成
parser = StrOutputParser()


# チャット履歴を制限する関数を定義
def limit_history(messages, max_messages=10):
    return messages[-max_messages:]


# 履歴制限機能の作成
history_limiter = RunnablePassthrough.assign(
    chat_history=lambda x: limit_history(x["chat_history"])
)

# チェーンの作成
chain = history_limiter | prompt_template | model | parser


# セッションごとのチャット履歴を保存する辞書を作成
histories = {}


# セッションIDに基づいてチャット履歴を取得する関数を定義
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in histories:
        histories[session_id] = InMemoryChatMessageHistory()
    return histories[session_id]


# 履歴管理機能を追加したチェーンの作成
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)

# Chromaベースのベクトルストアを使用した外部知識検索機能
vectorstore = Chroma(
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
    persist_directory="chroma",
)
retriever = vectorstore.as_retriever(
    search_type="mmr", search_kwargs={"k": 5, "fetch_k": 50}
)


# FastAPIアプリケーションの初期化
# 変更点: タイトルの更新
app = FastAPI(title="Chat with RAG API")


# 新規: チャットストリームの関数を定義
async def stream_chat_response(question: str, session_id: str):
    # セッションIDを設定
    config = {"configurable": {"session_id": session_id}}

    # 質問に基づいて関連情報を取得
    context = retriever.invoke(question)

    # contextを含めてchain_with_historyを呼び出し回答を取得
    async for response_chunk in chain_with_history.astream(
        {"question": question, "context": context}, config=config
    ):
        yield response_chunk


# チャットエンドポイントの定義
@app.get("/chat")
async def get_chat_response(question: str, session_id: str = "default"):
    # 変更点: StreamingResponseを返す
    return StreamingResponse(stream_chat_response(question, session_id))


# サーバーの起動
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
