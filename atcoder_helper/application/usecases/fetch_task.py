"""testcasesを取得し、指定したtestcasesファイルに書き込むサービス."""
from typing import Optional
from typing import Protocol


class FetchTaskUsecase(Protocol):
    """atcoderサイトからテストケースを取得するサービスのプロトコル."""

    def fetch_task(
        self,
        contest: Optional[str],
        task: Optional[str],
    ) -> None:
        """testcasesを取得し、指定したtestcasesファイルに書き込む.

        Raises:
            AtcoderAccessError: atcoderとのデータのやりとりの中でのエラー
            ConfigAccessError: 設定ファイルの読み書きのエラー

        Args:
            contest (str): コンテスト名。AtCoderのコンテストページのURLに現れる形式で渡す
            task (str): タスク名。AtCoderのコンテストページのURLに現れる形から、"コンテスト名_"の部分を除いたもの
        """
