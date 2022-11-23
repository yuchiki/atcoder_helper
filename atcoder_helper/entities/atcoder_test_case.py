"""テストケースにまつわるデータ構造を定義する."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from typing import cast

from colorama import Fore
from colorama import Style
from pydantic import BaseModel


class AtCoderTestStatus(Enum):
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
            AtCoderTestStatus.AC: Fore.GREEN,
            AtCoderTestStatus.WA: Fore.YELLOW,
            AtCoderTestStatus.ERROR: Fore.RED,
            AtCoderTestStatus.JUSTSHOW: Fore.BLUE,
        }

        return self._dye(self.name, table[self])


@dataclass
class AtCoderTestResult:
    """入力と出力からなる一度のテストに対して、テスト実行にまつわる結果を保持する."""

    name: str
    status: AtCoderTestStatus
    actual: str
    error: str
    expected: Optional[str] = None


class AtcoderTestCase(BaseModel):
    """テストケースを表す."""

    name: str
    given: str
    expected: Optional[str]
