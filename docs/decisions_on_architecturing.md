# 設計上の決定

以下は、必ずしもpythonにおけるベストプラクティスかどうかがわからないが、設計のぶれを防ぐために決定した設計方針である。

## 依存について

### インターフェースを多用し、依存性の注入を行う

外部への通信、実ファイルへの読み書きを行うため、これらをモック実装に置き換えやすくするため。」

stack overflow の質問一覧を見る限り、依存性の注入はpythonでも行われうるプラクティスのように思われる。

<https://stackoverflow.com/search?q=python+dependency+injection&s=54ca8726-ee79-4231-a4c8-b92ec25888c2>

## テスト方針について

### patchを最小限に抑え、依存性の注入によるmock注入を用いる

patchによるテストは影響範囲を限定しづらいと考えたため。
monkey patchはあまり使わずに、mock.MagicMockによる依存性の注入をなるべく用いる

好みの問題であると書いてあるstack overflowの問題を見つけたのでそうなのだろう。
<https://github.com/pytest-dev/pytest/issues/4576#issuecomment-449864333>
