"""テストケース実行のためのメソッド."""

from textwrap import indent
from typing import Any
from typing import Callable
from typing import List
from typing import Protocol

from atcoder_helper.entities.atcoder_test_case import AtCoderTestResult
from atcoder_helper.entities.atcoder_test_case import AtCoderTestStatus
from atcoder_helper.infrastructure import errors as repository_error
from atcoder_helper.infrastructure.local_test_case_repo import LocalTestCaseRepository
from atcoder_helper.infrastructure.local_test_case_repo import (
    get_default_local_test_case_repository,
)
from atcoder_helper.infrastructure.task_config_repo import TaskConfigRepository
from atcoder_helper.infrastructure.task_config_repo import (
    get_default_task_config_repository,
)
from atcoder_helper.program_executor import ProgramExecutor
from atcoder_helper.program_executor import get_default_program_executor
from atcoder_helper.usecases.errors import ConfigAccessError

ControllerBuilder = Callable[[List[str], List[str]], ProgramExecutor]


class ExecuteTestUsecase(Protocol):
    """テストを実行するサービス."""

    def execute_test(self) -> None:
        """testcaseに基づき、テストを実行する関数.

        Raises:
            ConfigAccessError: 設定ファイル読み書きのエラー
        """


def get_default_execute_test_usecase() -> ExecuteTestUsecase:
    """ExecuteTestUsecaseの標準実装を返す.

    Returns:
        ExecuteTestUsecase:
    """
    return ExecuteTestInteractor(
        task_config_repo=get_default_task_config_repository(),
        test_case_repo=get_default_local_test_case_repository(),
        controller_builder=get_default_program_executor,
    )


class ExecuteTestInteractor:
    """テストを実行するサービス."""

    _task_config_repo: TaskConfigRepository
    _test_case_repo: LocalTestCaseRepository

    # 本当は ControllerBuilder型なんだがmypyのバグにより型付けに失敗するので Any
    # see also https://github.com/python/mypy/issues/5485
    _controller_builder: Any

    def __init__(
        self,
        task_config_repo: TaskConfigRepository,
        test_case_repo: LocalTestCaseRepository,
        controller_builder: ControllerBuilder,
    ):
        """__init__.

        Args:
            task_config_repo (TaskConfigRepository, optional): _
            test_case_repo (TestCaseRepository, optional): _
            controller_builder (Callable[[List[str], List[str]], ProgramExecutor]): _
        """
        self._task_config_repo = task_config_repo
        self._test_case_repo = test_case_repo
        self._controller_builder = controller_builder

    def execute_test(self) -> None:
        """testcaseに基づき、テストを実行する関数.

        Raises:
            ConfigAccessError: 設定ファイル読み書きのエラー
        """
        try:
            task_config = self._task_config_repo.read()
            test_cases = self._test_case_repo.read()
        except (repository_error.ReadError, repository_error.ParseError):
            raise ConfigAccessError("設定ファイルの読み込みに失敗しました")

        controller = self._controller_builder(task_config.build, task_config.run)

        controller.build()  # TODO(ビルド失敗で止まるようにする)

        results = []
        for test_case in test_cases:
            print("-----------------------------------")
            print(f"executing {test_case.name}...")
            result = controller.execute(test_case)
            results.append(result)
            self._show_result(result)
        self._show_summary(results)

    def _show_result(self, result: AtCoderTestResult) -> None:
        print("-----------------------------------")
        print(f"{result.name:<15}: {result.status.dyed}")

        if result.status == AtCoderTestStatus.JUSTSHOW:
            print("    output:")
            print(indent(result.actual, "       >"))
        if result.status == AtCoderTestStatus.ERROR:
            print(result.error)
        if result.status == AtCoderTestStatus.WA:
            if result.expected is None:
                raise Exception("internal error")

            print("    expected:")
            print(indent(result.expected, "       >"))
            print("    but got:")
            print(indent(result.actual, "       >"))

    def _show_summary(self, results: List[AtCoderTestResult]) -> None:
        print("========================================")
        print("SUMMARY:")
        for result in results:
            print(f"{result.name:<15}: {result.status.dyed}")