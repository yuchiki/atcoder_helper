# atcoder_helper

atcoder出場を手助けするCLIツールです。

# install

`make install`

# 使い方


## 準備

問題を解くディレクトリの中で以下の準備をします

### テストランナーの設定

.atcoder_helper_task_configにビルドコマンドと実行コマンドをyamlで定義します。以下は定義の例です。

```yaml
build:
  - g++
  - main.cpp
  - -o
  - main
run:
  - ./main
```


### テストケースの取得

問題を解くディレクトリで`atcoder_helper fetch`コマンドを実行します。
たとえば ABC160のA問題であれば `atcoder_helper abc160 a` のようにコマンドを打ちます。
取得したテストケースはtestcases.yamlに保存されます。

## 問題を解いているとき

`atcoder_helper exec` で以下のような実行結果を得ることができます。

![出力画像](docs/exec_result.png)


# tips
- testcases.yamlのtestcaseにexpectedを指定しないテストケースを作成すると、そのケースはJUSTSHOW扱いになり、正答との比較はスキップされ、出力結果の表示だけが行われます。
