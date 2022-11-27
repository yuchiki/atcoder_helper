# プログラム構成について

このプログラムは、サブコマンド方式のCLIコマンドです。
ソースコードはatcoder_helper以下にあります。

## 実行の仕方

README.md 記載の方法でpip installすると、atcoder_helperコマンドとして実行できるようになります.

## 全体の構造


| path | 役割 |
| :-: | :-: |
| entrypoint | エントリーポイント。　`python atcoder_helper/entrypoint/main.py` で実行できる |
| entities   | やりとりするデータ構造 |
| application | ロジックのメイン部 |
| application/usecases | ユースケースのインターフェースの定義 |
| application/interactors | ユースケースの実装 |
| application/repositories | repositoryのインターフェースの定義 |
| adapter     | user、永続化層、インターネット等外界とのやりとり |
| adapter/controller | userとのやりとり |
| adapter/infrastructure | 外界とのやりとり。 repositoryの実装等 |
| default_configs | atcoder_helper が用いる、デフォルトの設定ファイルのテンプレート。 `config init` で生成できる|
| dependency.py | 依存性注入の関係の定義 |
| _version.py| バージョンの定義 |
| __main__.py | packageとして実行したときのエントリポイント |
| program_executor.py | リファクタリングし損ねてここにある。ダメなのでなんとかしたい |

