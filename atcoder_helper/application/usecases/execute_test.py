"""テストケース実行のためのメソッド."""

from typing import List
from typing import Protocol

from atcoder_helper.program_executor import ProgramExecutor
from atcoder_helper.program_executor import ProgramExecutorRepoImpl


class ControllerBuilder(Protocol):
    """ControllerBuilder."""

    @staticmethod
    def build(build_command: List[str], run_command: List[str]) -> ProgramExecutor:
        """build."""
        pass


class ControllerBuilderImpl:
    """ControllerBuilderの実装."""

    @staticmethod
    def build(build_command: List[str], run_command: List[str]) -> ProgramExecutor:
        """ProgramExecutorRepoの標準実装を返す."""
        return ProgramExecutorRepoImpl(build_command, run_command)


class ExecuteTestUsecase(Protocol):
    """テストを実行するサービス."""

    def execute_test(self) -> None:
        """testcaseに基づき、テストを実行する関数.

        Raises:
            ConfigAccessError: 設定ファイル読み書きのエラー
        """
