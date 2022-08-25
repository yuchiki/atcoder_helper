"""テストケースの永続化を行う."""
from typing import List
from typing import Protocol

import yaml

from atcoder_helper.models.atcoder_test_case import AtcoderTestCase
from atcoder_helper.repositories.errors import ParseError
from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.errors import WriteError


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


def get_default_local_test_case_repository() -> LocalTestCaseRepository:
    """TestCaseRepositoryの標準実装を返す."""
    default_testcase_file = "testcases.yaml"
    return LocalTestCaseRepositoryImpl(default_testcase_file)


class LocalTestCaseRepositoryImpl:
    """テストケースの永続化を行う."""

    def __init__(self, filename: str):
        """__init__.

        Args:
            filename (str): 永続化先のファイル名
        """
        self._filename = filename

    def write(self, test_cases: List[AtcoderTestCase]) -> None:
        """書き込みを行う.

        Args:
            test_cases (List[TestCase]): 取得したテストスイート

        Raises:
            WriteError: 書き込み失敗
        """

        def str_representer(dumper: yaml.dumper.Dumper, data: str) -> yaml.Node:
            if len(data.splitlines()) > 1:  # check for multiline string
                return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
            return dumper.represent_scalar("tag:yaml.org,2002:str", data)

        yaml.add_representer(str, str_representer)

        try:
            with open(self._filename, "wt") as file:
                yaml.dump([case.dict() for case in test_cases], file, sort_keys=False)
        except OSError as e:
            raise WriteError(f"cannot open {self._filename}") from e

    def read(self) -> List[AtcoderTestCase]:
        """読み込みを行う.

        Returns:
            List[TestCase]: 読み込まれたテストスイート

        Raises:
            ReadError: データの読み込みに失敗した
            ParseError: パースに失敗した
        """
        try:
            with open(self._filename, "rt") as file:
                objects = yaml.safe_load(file)
        except OSError as e:
            raise ReadError(f"cannot open {self._filename}") from e

        try:
            return [AtcoderTestCase.parse_obj(object) for object in objects]
        except Exception as e:
            raise ParseError(
                f"failed to parse {self._filename} as AtcoderTestCase"
            ) from e
