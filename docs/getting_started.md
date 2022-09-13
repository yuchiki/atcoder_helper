# 開発を始める

## 事前準備

atcoderにloginできる検証用のusernameとpasswordを `integration_test/secret.env` に以下の形式で記載してください。


```env
ATCODER_HELPER_NAME=your_user_name
ATCODER_HELPER_PASSWORD=your_password
```

このファイルは`.gitignore`されており、remoteにアップロードされることはありません。
この情報はlocalでintegration_testを実施するために必要となります。


## 開発環境

vscodeのremote container環境で開発されています。


## localでのチェック

`make` を実行すると、諸々のコードチェック・テストなどが走るようになっています。詳細はMakefileを参照。
