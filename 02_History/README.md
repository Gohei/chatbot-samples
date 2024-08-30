# 02 History: 過去の会話を記憶するチャットボット 💾💬

## はじめに 🌟
この実装ステップでは、01_Basicで作成したシンプルな質問応答チャットボットに、  
過去の会話を記憶する機能を追加します。  
これにより、チャットボットはより文脈を理解した応答ができるようになります。

## システムの動作フロー 🏄‍♂️
1. ユーザーがフロントエンドでメッセージを入力
2. フロントエンドが`session_id`とともにバックエンドAPIにリクエストを送信
3. バックエンドが該当セッションの履歴を取得・更新
4. 履歴を考慮してAIモデルが応答を生成
5. 生成された応答をバックエンドからフロントエンドに返信
6. フロントエンドが応答をユーザーに表示

## 開発ステップ 🏗️

### 1. バックエンド拡張
FastAPIで構築したチャットボットのAPIサーバーに会話履歴機能を追加します。  
LangChainを通じて会話履歴を管理し、文脈を考慮した回答生成を実装します。  
詳細な手順は[バックエンドの実装ガイド](backend/README.md)を参照してください。

### 2. フロントエンド調整
Chainlitで構築したチャットインターフェースを調整し、セッションIDを扱えるようにします。  
このインターフェースを通じて、ユーザーは文脈を考慮したチャットボットと対話することができます。  
詳細な手順は[フロントエンドの実装ガイド](frontend/README.md)を参照してください。

## 主な変更点 📝

### バックエンド（chat_server.py）:

1. 新規モジュールのインポート:
   - `RunnablePassthrough`
   - `RunnableWithMessageHistory`
   - `BaseChatMessageHistory`,
   - `InMemoryChatMessageHistory`

2. プロンプトテンプレートの拡張:
   - `chat_history`プレースホルダーを追加

3. 履歴管理の実装:
   - `limit_history`関数: 最新の10メッセージに履歴を制限
   - `history_limiter`: `RunnablePassthrough`を使用した履歴制限機能
   - `histories`辞書: セッションごとの履歴を保存
   - `get_session_history`関数: セッションIDに基づく履歴の取得・作成

4. チェーンの拡張:
   - `history_limiter`をチェーンに追加
   - `RunnableWithMessageHistory`を使用して履歴管理機能を統合

5. APIの更新:
   - アプリケーションタイトルを "Chat with History API" に変更
   - `/chat`エンドポイントに`session_id`パラメータを追加
   - `chain_with_history`を使用して応答を生成

### フロントエンド（frontend_app.py）:

1. APIリクエストの更新:
   - `session_id`パラメータを追加（固定値"abc123"を使用）