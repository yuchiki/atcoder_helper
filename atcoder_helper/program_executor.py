"""プログラムを実行して結果を取得する."""

import subprocess
from typing import List
from typing import Protocol

from atcoder_helper.models.test_case import AtcoderTestCase
from atcoder_helper.models.test_case import TestResult
from atcoder_helper.models.test_case import TestStatus


class ProgramExecutor(Protocol):
    """プログラムを実行するためのエグゼキューター."""

    def build(self) -> bool:
        """プログラムをビルドする.

        Args:

        Returns:
            bool: ビルドが成功したか
        """

    def execute(self, test_case: AtcoderTestCase) -> TestResult:
        """プログラムを実行し、テスト結果を得る.

        Args:
            test_case (AtcoderTestCase): テストケース

        Returns:
            TestResult: テスト結果
        """


def get_default_program_executor(
    build_command: List[str], run_command: List[str]
) -> ProgramExecutor:
    """ProgramExecutorRepoの標準実装を返す."""
    return ProgramExecutorRepoImpl(build_command, run_command)


class ProgramExecutorRepoImpl:
    """プログラム実行のためのロジックを集約させるためのリポジトリ実装."""

    _build_command: List[str]
    _run_command: List[str]

    def __init__(self, build_command: List[str], run_command: List[str]):
        """__init__."""
        self._build_command = build_command
        self._run_command = run_command

    def build(self) -> bool:
        """プログラムをビルドする.

        Args:

        Returns:
            bool: ビルドが成功したか
        """
        completed_process = subprocess.run(self._build_command)
        return completed_process.returncode == 0

    def execute(self, test_case: AtcoderTestCase) -> TestResult:
        """プログラムを実行し、テスト結果を得る.

        Args:
            test_case (AtcoderTestCase): テストケース

        Returns:
            TestResult: テスト結果
        """
        completed_process = subprocess.run(
            self._run_command, input=test_case.given, text=True, capture_output=True
        )

        if completed_process.returncode != 0:
            return TestResult(
                test_case.name,
                TestStatus.ERROR,
                actual=completed_process.stdout,
                error=completed_process.stderr,
            )

        if test_case.expected is None:
            return TestResult(
                test_case.name,
                TestStatus.JUSTSHOW,
                actual=completed_process.stdout,
                error="",
            )

        if test_case.expected == completed_process.stdout:
            return TestResult(
                test_case.name, TestStatus.AC, actual=completed_process.stdout, error=""
            )
        else:
            return TestResult(
                test_case.name,
                TestStatus.WA,
                actual=completed_process.stdout,
                expected=test_case.expected,
                error="",
            )
