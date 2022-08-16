# プログラム構成について

このプログラムは、サブコマンド方式のCLIコマンドです。
ソースコードはatcoder_helper以下にあります。

## 実行の仕方

README.md 記載の方法でpip installすると、atcoder_helperコマンドとして実行できるようになります.

## 全体の構造

### エントリーポイント

エントリーポイントはscripts/main.py にあります。 `python atcoder_helper/scripts/main.py` です。
プログラムはここから実行されます。

### script層

コマンドラインアプリとしての体裁を整えています。
scriptは実際の処理をservice層に投げています。

### service層

コマンドの実際の処理を行う層です。ファイルアクセス・通信を行い、パースされたデータを取得・書き込みするまでの処理はrepository層に投げ、ビジネスロジックだけに集中しています。

### repository層

ファイルアクセス・通信を行い、パース済みのデータの形でservice層に返す/service層から受け取るための層です。

### model層

層をまたいでやり取りされるデータ構造を定義します。

### program_executor.py

テストケースの事前処理・実行を担います。

### default_config

`config init` コマンドが作成する初期設定のためのファイル群です。
