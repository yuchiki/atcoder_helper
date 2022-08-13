"""testcasesを取得し、指定したtestcasesファイルに書き込むサービス."""
import sys
from typing import Optional

from atcoder_helper.repositories.atcoder_repo import AtCoderRepository
from atcoder_helper.repositories.task_conifg_repo import TaskConfigRepository
from atcoder_helper.repositories.test_case_repo import TestCaseRepository


def fetch_task(contest: Optional[str], task: Optional[str]) -> None:
    """testcasesを取得し、指定したtestcasesファイルに書き込む.

    Args:
        contest (str): コンテスト名。AtCoderのコンテストページのURLに現れる形式で渡す
        task (str): タスク名。AtCoderのコンテストページのURLに現れる形から、"コンテスト名_"の部分を除いたもの
    """
    atcoder_repo = AtCoderRepository()
    task_config_repo = TaskConfigRepository(".atcoder_helper_task_config.yaml")
    test_case_repo = TestCaseRepository("testcases.yaml")

    task_config = task_config_repo.read()

    if contest is None:
        contest = task_config.contest

    if task is None:
        task = task_config.task

    if contest is None:
        print("contest is None. use --contest <contest>", file=sys.stderr)
        print(
            "or add `contest: <contest>` in .atcoder_helper_task_config.yaml",
            file=sys.stderr,
        )
        sys.exit(1)

    if task is None:
        print("task is None. use --task <contest>", file=sys.stderr)
        print(
            "or add `task: <task>` in .atcoder_helper_task_config.yaml", file=sys.stderr
        )
        sys.exit(1)

    test_cases = atcoder_repo.fetch_test_cases(contest, task)

    test_case_repo.write(test_cases)


if __name__ == "__main__":
    fetch_task(sys.argv[1], sys.argv[2])
