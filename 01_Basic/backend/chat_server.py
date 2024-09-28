import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


# .envファイルから環境変数を読み込む
load_dotenv()

# OpenAI APIキーの確認
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OpenAI APIキーが設定されていません")


# プロンプトテンプレートの作成
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "簡潔で正確な回答を提供してください:"),
        ("user", "{question}"),
    ],
)

# モデルの作成
model = ChatOpenAI(model="gpt-4o-mini")

# 出力パーサーの作成
parser = StrOutputParser()

# チェーンの作成
chain = prompt_template | model | parser

# FastAPIアプリケーションの初期化
app = FastAPI(title="Basic Chat API")


# チャットエンドポイントの定義
@app.get("/chat")
async def get_chat_response(question: str):
    answer = chain.invoke({"question": question})
    return {"answer": answer}


# サーバーの起動
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
