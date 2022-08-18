"""Tests for execute_test."""

from typing import List
from typing import Type

import mock
import pytest

from atcoder_helper.models.task_config import TaskConfig
from atcoder_helper.models.test_case import AtcoderTestCase
from atcoder_helper.models.test_case import TestResult
from atcoder_helper.models.test_case import TestStatus
from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.task_config_repo import TaskConfigRepository
from atcoder_helper.repositories.test_case_repo import TestCaseRepository
from atcoder_helper.services.errors import ConfigAccessError
from atcoder_helper.services.execute_test import ExecuteTestServiceImpl
from atcoder_helper.services.execute_test import ExecutorBuilder


def _get_sut(
    task_config_repo_mock: TaskConfigRepository = mock.MagicMock(),
    test_case_repo_mock: TestCaseRepository = mock.MagicMock(),
    executor_builder: ExecutorBuilder = mock.MagicMock(),
) -> ExecuteTestServiceImpl:
    return ExecuteTestServiceImpl(
        task_config_repo=task_config_repo_mock,
        test_case_repo=test_case_repo_mock,
        executor_builder=executor_builder,
    )


_task_config = TaskConfig(contest=None, task=None, build=["foo"], run=["bar"])
_test_cases = [
    AtcoderTestCase("test_a", "foo_a", "bar_a"),
    AtcoderTestCase("test_b", "foo_b", "bar_b"),
    AtcoderTestCase("test_c", "foo_c", "bar_c"),
]

_result = TestResult("foo", TestStatus.AC, "actual", "error", None)

test_execute_test_parameters = {
    "OK": [
        mock.MagicMock(read=mock.MagicMock(return_value=_task_config)),
        mock.MagicMock(read=mock.MagicMock(return_value=_test_cases)),
        None,
        _test_cases,
    ],
    "設定読み込みに失敗したらエラー": [
        mock.MagicMock(read=mock.MagicMock(side_effect=ReadError())),
        mock.MagicMock(),
        ConfigAccessError,
        [],
    ],
    "テストケース読み込みに失敗したらエラー": [
        mock.MagicMock(read=mock.MagicMock(return_value=_task_config)),
        mock.MagicMock(read=mock.MagicMock(side_effect=ReadError())),
        ConfigAccessError,
        [],
    ],
}


@pytest.mark.parametrize(
    argnames=(
        "task_config_repo_mock",
        "test_case_repo_mock",
        "exception",
        "execute_called_with",
    ),
    argvalues=list(test_execute_test_parameters.values()),
    ids=list(test_execute_test_parameters.keys()),
)
def test_execute_test(
    task_config_repo_mock: mock.MagicMock,
    test_case_repo_mock: mock.MagicMock,
    exception: Type[Exception],
    execute_called_with: List[AtcoderTestCase],
) -> None:
    """execute_testのテスト."""
    build_mock = mock.MagicMock()
    execute_mock = mock.MagicMock(return_value=_result)
    sut = _get_sut(
        task_config_repo_mock=task_config_repo_mock,
        test_case_repo_mock=test_case_repo_mock,
        executor_builder=mock.MagicMock(
            return_value=mock.MagicMock(
                build=build_mock,
                execute=execute_mock,
            )
        ),
    )

    if exception is not None:
        with pytest.raises(exception):
            sut.execute_test()
    else:
        sut.execute_test()
        build_mock.assert_called_once()
        execute_mock.assert_has_calls(
            [mock.call(testcase) for testcase in execute_called_with]
        )