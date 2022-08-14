"""テストケースの永続化を行う."""
from typing import Final
from typing import List
from typing import Protocol

import yaml

from atcoder_helper.models.test_case import AtcoderTestCase
from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.errors import WriteError


class TestCaseRepository(Protocol):
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
        """


def get_default_test_case_repository() -> TestCaseRepository:
    """TestCaseRepositoryの標準実装を返す."""
    return TestCaseRepositoryImpl()


class TestCaseRepositoryImpl:
    """テストケースの永続化を行う."""

    default_testcase_file: Final[str] = "testcases.yaml"

    def __init__(self, filename: str = default_testcase_file):
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

        test_case_dicts = [case.to_dict() for case in test_cases]

        try:
            with open(self._filename, "wt") as file:
                yaml.dump(test_case_dicts, file, sort_keys=False)
        except OSError as e:
            raise WriteError(f"cannot open {self._filename}") from e

    def read(self) -> List[AtcoderTestCase]:
        """読み込みを行う.

        Returns:
            List[TestCase]: 読み込まれたテストスイート

        Raises:
            ReadError: データの読み込みに失敗した
        """
        try:
            with open(self._filename, "rt") as file:
                objects = yaml.safe_load(file)  # TODO(validate)
        except OSError as e:
            raise ReadError(f"cannot open {self._filename}") from e
        return [AtcoderTestCase.from_dict(object) for object in objects]
