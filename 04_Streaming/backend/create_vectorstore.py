import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


# .envファイルから環境変数を読み込む
load_dotenv()

# OpenAI APIキーの確認
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OpenAI APIキーが設定されていません")


# テキストファイルの読み込み
text_path = "kintaro.txt"
loader = TextLoader(text_path, encoding="utf-8")
documents = loader.load()


# テキストの分割
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
split_documents = text_splitter.split_documents(documents)


# ベクトルストアの作成
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(
    documents=split_documents,
    embedding=embeddings,
    persist_directory="chroma",
)

print("ベクトルストアの作成が完了しました")
