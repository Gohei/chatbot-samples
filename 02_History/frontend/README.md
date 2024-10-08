# 02 History / frontend

## 会話履歴を考慮したチャットフロントエンドの実装

---

### はじめに 🌟
この実装ステップでは、01_Basicで作成したチャットフロントエンドに、  
バックエンドの会話履歴機能に対応するための小さな変更を加えます。  
Chainlitインターフェース自体には変更を加えず、  
APIリクエスト時にセッションIDを含める修正を行います。


### 目標 🎯
- バックエンドの会話履歴機能に対応するためのAPI呼び出しの修正
- 固定のセッションIDを使用したリクエストの実装
- 会話の文脈を考慮したチャット機能の動作確認

### 開発ステップ 🚀

1. 開発環境のセットアップ 🛠️  
2. 実装 💻  
3. テスト 🧪

---

### 1. 開発環境のセットアップ 🛠️
※ 注意: [事前準備](/SETUP.md) を完了させてから、以下のステップを進めてください。  

---

#### 1. VSCodeでプロジェクトを開く ⛹️‍♂️
`02_History`フォルダの`frontend`フォルダをドラッグドロップをして、VSCodeで開きます。

---

##### 2. 仮想環境の作成 🔮
1. VSCode 画面上部のメニューから 表示 -> ターミナル ( View -> Terminal ) を選択してターミナルを表示します。
2. ターミナルで次のコマンドを入力して仮想環境を構築します。
```bash
python -m venv venv
```
このコマンドを実行すると、現在のフォルダに venv という名前のフォルダが作成されます。  

###### 注意事項 🚨
- 仮想環境（venvフォルダ）はGitリポジトリにコミットしないのが一般的です。  
仮想環境をコミットするとリポジトリの容量が大きく増加します。  
リポジトリの容量が大きくなるとサイズ制限やタイムアウトに起因する問題が発生するリスクが高まります。

- .gitignore ファイルを使用して、仮想環境を追跡対象から除外することをおすすめします。  
本リポジトリでも、.gitignoreファイルでvenvフォルダを除外しています。

---

##### 3. 仮想環境の有効化 🪄
仮想環境を有効化します：
- Windowsの場合：
    ```bash
    venv\Scripts\activate
    ```
- macOS/Linuxの場合：
    ```bash
    source venv/bin/activate
    ```

---

##### 4. 必要なライブラリのインストール 📚
仮想環境が有効になっていることを確認し、  
ターミナルで次のコマンドを入力して必要なライブラリをインストールします：
```bash
pip install -r requirements.txt
```

---

### 2. 実装 💻  

次に、実装フェーズに進みます。  
02_History では、APIリクエスト時に固定のセッションIDを含める小さな変更を行います。  
以下のファイルを開いて、変更点を確認しましょう。

[frontend_app.py](./frontend_app.py)

---

### 3. テスト 🧪

実装を確認したら、フロントエンドアプリケーションを起動して実際に動作をテストしましょう。

1. バックエンドサーバーの起動確認
まず、バックエンドサーバーが起動していることを確認してください。  
起動していない場合は、バックエンドのREADMEを参照して起動してください。

2. フロントエンドアプリケーションの起動  
ターミナルで以下のコマンドを実行し、フロントエンドアプリケーションを起動します:  
    ```bash
    chainlit run frontend_app.py
    ```

3. ブラウザでアクセス  
アプリケーションが起動したら、ブラウザで以下のURLにアクセスします:  
    ```
    http://localhost:8000
    ```

4. チャットインターフェースのテスト  
    1. チャットインターフェースが表示されることを確認します。
    2. メッセージ入力欄に質問を入力し、送信します。
    3. バックエンドAPIからの応答が表示されることを確認します。
    4. 複数の質問を連続して送信し、会話の文脈が維持されていることを確認します。  
       (注: 文脈の維持はバックエンドの機能であり、フロントエンドの変更ではありません)


---

## 次のステップ
基本的なチャットAPIの実装が完了したら、以下の機能を追加したバージョンに挑戦してみましょう：

- [03_RAG](/03_RAG/README.md): 外部知識を活用した回答生成機能を追加
- [04_Streaming](/04_Streaming/README.md): 回答のリアルタイム表示機能を追加
- [05_Auth](/04_Streaming/README.md): ログイン機能を実装