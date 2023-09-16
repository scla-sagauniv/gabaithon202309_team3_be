# 環境構築

レポジトリーをクーロンする

```
git clone https://github.com/scla-sagauniv/gabaithon202309_team3_be.git backend
```

パッケージをインストールする

- 仮想環境の場合  
    ```
    pip install pipenv
    pipenv --python 3.10
    pipenv install fastapi uvicorn firebase-admin
    pipenv shell
    ```
- 通常の場合
    ```
    pip install fastapi uvicorn firebase-admin
    ```

Firebase認証情報を設定する

1. プロジェクト画面のプロジェクトの設定を開く
2. サービスアカウントタグにある新しい秘密鍵の生成ボタンを押す
3. ポップアップでキーを生成ボタンを押すとJSONファイルがダウンロードされ、`credentials.json` で保存し、backend の中に配置する

APIを起動する
```
uvicorn main:app --reload

# http://127.0.0.1:5000/test で確認する
```