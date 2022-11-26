"""テストケースの永続化を行う."""
from typing import List
from typing import Protocol

from atcoder_helper.entities.atcoder_test_case import AtcoderTestCase


class LocalTestCaseRepository(Protocol):
    """テストケースの永続化を行うプロトコル."""

    def write(self, test_cases: List[AtcoderTestCase]) -> None:
        """書き込みを行う.

        Args:
            test_cases (List[TestCase]): 取得したテストスイート

        Raises:
            WriteError: 書き込み失敗
        """

    def read(self) -> List[AtcoderTestCase]:
        """読み込みを行う.

        Returns:
            List[TestCase]: 読み込まれたテストスイート

        Raises:
            ReadError: データの読み込みに失敗した
            ParseError: パースに失敗した
        """
