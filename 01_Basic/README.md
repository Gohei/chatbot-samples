# 01 Basic: シンプルな質問応答チャットボット 💬

## はじめに 🌟
この実装ステップでは、AIを活用したシンプルな質問応答チャットボットを作成します。  
バックエンドとフロントエンドの両方を開発し、基本的なチャットボットの仕組みを学びます。


## システムの動作フロー 🏄‍♂️
1. ユーザーがフロントエンドでメッセージを入力
2. フロントエンドがバックエンドAPIにリクエストを送信
3. バックエンドがリクエストを受信し、AIモデルに転送
4. AIモデルが質問に対する応答を生成
5. 生成された応答をバックエンドからフロントエンドに返信
6. フロントエンドが応答をユーザーに表示

## 開発ステップ 🏗️

### 1. バックエンド開発
FastAPIを使用してチャットボットのAPIサーバーを構築し、  
LangChainを通じてOpenAIのAIモデルと連携します。  
詳細な手順は[バックエンドの実装ガイド](./backend/README.md)を参照してください。

### 2. フロントエンド開発
Chainlitを使用してチャットインターフェースを構築します。  
このインターフェースを通じて、ユーザーはチャットボットと対話することができます。  
詳細な手順は[フロントエンドの実装ガイド](./frontend/README.md)を参照してください。