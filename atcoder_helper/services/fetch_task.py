"""testcasesを取得し、指定したtestcasesファイルに書き込むサービス."""
from typing import Optional
from typing import Protocol
from typing import Tuple

from atcoder_helper.repositories import errors as repository_error
from atcoder_helper.repositories.atcoder_test_case_repo import AtCoderTestCaseRepository
from atcoder_helper.repositories.atcoder_test_case_repo import (
    get_default_atcoder_test_case_repository,
)
from atcoder_helper.repositories.local_test_case_repo import LocalTestCaseRepository
from atcoder_helper.repositories.local_test_case_repo import (
    get_default_local_test_case_repository,
)
from atcoder_helper.repositories.logged_in_session_repo import LoggedInSessionRepository
from atcoder_helper.repositories.logged_in_session_repo import (
    get_default_session_repository,
)
from atcoder_helper.repositories.task_config_repo import TaskConfigRepository
from atcoder_helper.repositories.task_config_repo import (
    get_default_task_config_repository,
)
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
    return FetchTaskServiceImpl(
        task_config_repo=get_default_task_config_repository(),
        test_case_repo=get_default_local_test_case_repository(),
        session_repo=get_default_session_repository(),
        atcoder_testcase_repo=(get_default_atcoder_test_case_repository()),
    )


class FetchTaskServiceImpl:
    """atcoderサイトからテストケースを取得するサービス."""

    _task_config_repo: TaskConfigRepository
    _test_case_repo: LocalTestCaseRepository
    _session_repo: LoggedInSessionRepository
    _atcoder_testcase_repo: AtCoderTestCaseRepository

    def __init__(
        self,
        task_config_repo: TaskConfigRepository,
        test_case_repo: LocalTestCaseRepository,
        session_repo: LoggedInSessionRepository,
        atcoder_testcase_repo: AtCoderTestCaseRepository,
    ) -> None:
        """__init__."""
        self._task_config_repo = task_config_repo
        self._test_case_repo = test_case_repo
        self._session_repo = session_repo
        self._atcoder_testcase_repo = atcoder_testcase_repo

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
        (contest, task) = self._get_task_info(contest, task)

        try:
            session = self._session_repo.read()
        except repository_error.ReadError as e:
            raise ConfigAccessError("セッションの読み込みに失敗") from e

        try:
            test_cases = self._atcoder_testcase_repo.fetch_test_cases(
                session=session, contest=contest, task=task
            )
        except (repository_error.ConnectionError, repository_error.ParseError) as e:
            raise AtcoderAccessError("テストケースの取得に失敗しました") from e

        try:
            self._test_case_repo.write(test_cases)
        except repository_error.WriteError as e:
            raise ConfigAccessError("テストケースの書き込みに失敗しました") from e

    def _get_task_info(
        self, given_contest: Optional[str], given_task: Optional[str]
    ) -> Tuple[str, str]:
        """contestとtaskを得る.

        Raises:
            ConfigAccessError: 設定に問題がある

        Returns:
            Tuple[str, str]: contest, task
        """
        try:
            task_config = self._task_config_repo.read()
        except (repository_error.ReadError, repository_error.ParseError) as e:
            raise ConfigAccessError("設定ファイルの読み込みに失敗しました") from e

        contest = task_config.contest if given_contest is None else given_contest
        task = task_config.task if given_task is None else given_task

        if contest is None:
            raise ConfigAccessError("contest is not set.")

        if task is None:
            raise ConfigAccessError("task is not set.")

        return (contest, task)
