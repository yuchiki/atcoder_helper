"""テストケースにまつわるデータ構造を定義する."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from typing import TypedDict
from typing import cast

from colorama import Fore
from colorama import Style
from typing_extensions import NotRequired
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


class AtcoderTestCaseDict(TypedDict):
    """AtcoderTestCaseの辞書版."""

    name: str
    input: str
    expected: NotRequired[str]


@dataclass
class AtcoderTestCase(YAMLObject):
    """テストケースを表す."""

    name: str
    given: str
    expected: Optional[str]

    def to_dict(self) -> AtcoderTestCaseDict:
        """テストケースを辞書型に変換する."""
        if self.expected is None:
            return {"name": self.name, "input": self.given}
        else:
            return {"name": self.name, "input": self.given, "expected": self.expected}

    @classmethod
    def from_dict(cls, test_case_dict: AtcoderTestCaseDict) -> "AtcoderTestCase":
        """辞書からテストケース型に変換する."""
        return AtcoderTestCase(
            test_case_dict["name"],
            test_case_dict["input"] + "\n",
            test_case_dict["expected"] + "\n" if "expected" in test_case_dict else None,
        )
