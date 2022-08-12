# atcoder_helper

atcoder出場を手助けするCLIツールです。

# install

`make install`

# 使い方

## 最初の初期化

`atcoder_helper config init`コマンドにより、 `$HOME/.atcoder_helper` 以下に設定ファイルが作成されます。


## 準備

問題を解くディレクトリの中で以下の準備をします。

### ディレクトリの初期化

`atcoder_helper init_task` コマンドを実行し、ディレクトリを初期化します。

問題を解くための雛型が生成されます。また、ビルドコマンド・実行コマンドなどの情報を記したタスク設定ファイル`.atcoder_helper_task_config.yaml`が生成されます。

### テストケースの取得

問題を解くディレクトリで`atcoder_helper fetch`コマンドを実行します。
たとえば ABC160のA問題であれば `atcoder_helper abc160 a` のようにコマンドを打ちます。
取得したテストケースはtestcases.yamlに保存されます。

## 問題を解いているとき

`atcoder_helper exec` で以下のような実行結果を得ることができます。

![出力画像](docs/exec_result.png)


# tips
- testcases.yamlのtestcaseにexpectedを指定しないテストケースを作成すると、そのケースはJUSTSHOW扱いになり、正答との比較はスキップされ、出力結果の表示だけが行われます。
- 古い時代のコンテストには対応していないことを把握しています。
