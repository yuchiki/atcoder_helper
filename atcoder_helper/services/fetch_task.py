"""testcasesを取得し、指定したtestcasesファイルに書き込むサービス."""
from typing import Optional
from typing import Protocol

from atcoder_helper.repositories import errors as repository_error
from atcoder_helper.repositories.atcoder_repo import AtCoderRepository
from atcoder_helper.repositories.atcoder_repo import get_default_atcoder_repository
from atcoder_helper.repositories.task_config_repo import TaskConfigRepository
from atcoder_helper.repositories.task_config_repo import (
    get_default_task_config_repository,
)
from atcoder_helper.repositories.test_case_repo import TestCaseRepository
from atcoder_helper.repositories.test_case_repo import get_default_test_case_repository
from atcoder_helper.services.errors import AtcoderAccessError
from atcoder_helper.services.errors import ConfigAccessError


class FetchTaskService(Protocol):
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


def get_default_fetch_task_service() -> FetchTaskService:
    """FetchTaskServiceの標準実装を返す.

    Returns:
        FetchTaskService:
    """
    return FetchTaskServiceImpl()


class FetchTaskServiceImpl:
    """atcoderサイトからテストケースを取得するサービス."""

    _atcoder_repo: AtCoderRepository
    _task_config_repo: TaskConfigRepository
    _test_case_repo: TestCaseRepository

    def __init__(self) -> None:
        """__init__."""
        self._atcoder_repo = get_default_atcoder_repository()
        self._task_config_repo = get_default_task_config_repository()
        self._test_case_repo = get_default_test_case_repository()

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
        try:
            task_config = self._task_config_repo.read()
        except repository_error.ReadError as e:
            raise ConfigAccessError("設定ファイルの読み込みに失敗しました") from e

        contest = task_config.contest if contest is None else contest
        task = task_config.task if task is None else task

        if contest is None:
            raise ConfigAccessError("contest is not set.")

        if task is None:
            raise ConfigAccessError("task is not set.")

        try:
            test_cases = self._atcoder_repo.fetch_test_cases(contest, task)
        except repository_error.ReadError as e:
            raise AtcoderAccessError("テストケースの取得に失敗しました") from e

        try:
            self._test_case_repo.write(test_cases)
        except repository_error.WriteError as e:
            raise ConfigAccessError("設定ファイルの書き込みに失敗しました") from e
