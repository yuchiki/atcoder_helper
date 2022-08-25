"""AtCoderからテストケースを取得するリポジトリ."""


from typing import List
from typing import Protocol

import requests
from bs4 import BeautifulSoup

from atcoder_helper.models.atcoder_test_case import AtcoderTestCase
from atcoder_helper.repositories.errors import ParseError
from atcoder_helper.repositories.utils import AtCoderURLProvider


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


def get_default_atcoder_test_case_repository() -> AtCoderTestCaseRepository:
    """AtCoderTestCaseRepositoryのデフォルト実装を作成する.

    Returns:
        AtCoderTestCaseRepository: デフォルト実装
    """
    return AtCoderTestCaseRepositoryImpl()


class AtCoderTestCaseRepositoryImpl:
    """AtCoderからテストケースを取得するリポジトリ."""

    _url_provider = AtCoderURLProvider

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

        def normalize_newline(text: str) -> str:
            return "\n".join(text.splitlines())

        try:
            task_page = session.get(self._url_provider.task_url(contest, task))
        except Exception as e:
            raise ConnectionError(
                f"cannot GET {self._url_provider.task_url(contest, task)}"
            ) from e

        try:
            html = BeautifulSoup(task_page.text, "html.parser")

            sections = (
                html.find("div", id="task-statement")
                .find("span", attrs={"class": "lang-ja"})
                .find_all("section")
            )

            input_sections = {
                section.find("h3").text.split()[1]: normalize_newline(
                    section.find("pre").text
                )
                for section in sections
                if "入力例" in section.find("h3").text
            }

            output_sections = {
                section.find("h3").text.split()[1]: normalize_newline(
                    section.find("pre").text
                )
                for section in sections
                if "出力例" in section.find("h3").text
            }
        except Exception as e:
            raise ParseError() from e

        return [
            AtcoderTestCase(
                name=f"case-{name}", given=given, expected=output_sections[name]
            )
            for (name, given) in input_sections.items()
        ]
