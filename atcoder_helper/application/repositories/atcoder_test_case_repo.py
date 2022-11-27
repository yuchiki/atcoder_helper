"""AtCoderからテストケースを取得するリポジトリ."""


from typing import List
from typing import Protocol

import requests

from atcoder_helper.entities.atcoder_test_case import AtcoderTestCase


class AtCoderTestCaseRepository(Protocol):
    """AtCoderからテストケースを取得するリポジトリのプロトコル."""

    def fetch_test_cases(
        self, session: requests.Session, contest: str, task: str
    ) -> List[AtcoderTestCase]:
        """テストケーススイートを取得する.

        Args:
            contest (str): コンテスト名
            task (str): タスク名

        Raises:
            ConnectionError: GETに失敗
            ParseError: Parseに失敗

        Returns:
            List[TestCase]: テストケーススイート
        """
