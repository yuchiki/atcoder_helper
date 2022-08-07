"""testcasesを取得し、指定したtestcasesファイルに書き込むサービス."""
import sys

from atcoder_helper.repositories.atcoder_repo import AtCoderRepository
from atcoder_helper.repositories.test_case_repo import TestCaseRepository


def fetch_task(contest: str, task: str) -> None:
    """testcasesを取得し、指定したtestcasesファイルに書き込む.

    Args:
        contest (str): コンテスト名。AtCoderのコンテストページのURLに現れる形式で渡す
        task (str): タスク名。AtCoderのコンテストページのURLに現れる形から、"コンテスト名_"の部分を除いたもの
    """
    atcoder_repo = AtCoderRepository("session/session_dump.pkl")
    test_case_repo = TestCaseRepository("testcases.yaml")

    test_cases = atcoder_repo.fetch_test_cases(contest, task)

    test_case_repo.write(test_cases)


if __name__ == "__main__":
    fetch_task(sys.argv[1], sys.argv[2])
