"""テストケースにまつわるデータ構造を定義する."""
import subprocess
from dataclasses import dataclass
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from typing import cast

from colorama import Fore
from colorama import Style
from yaml import YAMLObject


class TestStatus(Enum):
    """テスト結果の状態を保持する."""

    AC = 1
    WA = 2
    ERROR = 3
    JUSTSHOW = 4

    def _dye(self, message: str, color: str) -> str:
        return cast(str, color + message + Style.RESET_ALL)

    @property
    def dyed(self) -> str:
        """テスト結果の状態をふさわしい色に染めた文字列を返す."""
        table = {
            TestStatus.AC: Fore.GREEN,
            TestStatus.WA: Fore.YELLOW,
            TestStatus.ERROR: Fore.RED,
            TestStatus.JUSTSHOW: Fore.BLUE,
        }

        return self._dye(self.name, table[self])


@dataclass
class TestResult:
    """入力と出力からなる一度のテストに対して、テスト実行にまつわる結果を保持する."""

    name: str
    status: TestStatus
    actual: str
    error: str
    expected: Optional[str] = None


@dataclass
class AtcoderTestCase(YAMLObject):
    """テストケースを表す."""

    name: str
    given: str
    expected: Optional[str]

    def to_dict(self) -> Dict[str, str]:
        """テストケースを辞書型に変換する."""
        if self.expected is None:
            return {"name": self.name, "input": self.given}
        else:
            return {"name": self.name, "input": self.given, "expected": self.expected}

    @classmethod
    def from_dict(cls, test_case_dict: Dict[str, str]) -> "AtcoderTestCase":
        """辞書からテストケース型に変換する."""
        return AtcoderTestCase(
            test_case_dict["name"],
            test_case_dict["input"] + "\n",
            test_case_dict["expected"] + "\n" if "expected" in test_case_dict else None,
        )

    def execute(self, run_command: List[str]) -> TestResult:
        """テストを実行する."""
        completed_process = subprocess.run(
            run_command, input=self.given, text=True, capture_output=True
        )

        if completed_process.returncode != 0:
            return TestResult(
                self.name,
                TestStatus.ERROR,
                actual=completed_process.stdout,
                error=completed_process.stderr,
            )

        if self.expected is None:
            return TestResult(
                self.name,
                TestStatus.JUSTSHOW,
                actual=completed_process.stdout,
                error="",
            )

        if self.expected == completed_process.stdout:
            return TestResult(
                self.name, TestStatus.AC, actual=completed_process.stdout, error=""
            )
        else:
            return TestResult(
                self.name,
                TestStatus.WA,
                actual=completed_process.stdout,
                expected=self.expected,
                error="",
            )
