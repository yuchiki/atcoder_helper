"""Tests for execute_test."""

from typing import List
from typing import Type

import mock
import pytest

from atcoder_helper.application.interactors.execute_test import ControllerBuilder
from atcoder_helper.application.interactors.execute_test import ExecuteTestInteractor
from atcoder_helper.application.repositories.errors import ReadError
from atcoder_helper.application.repositories.local_test_case_repo import (
    LocalTestCaseRepository,
)
from atcoder_helper.application.repositories.task_config_repo import (
    TaskConfigRepository,
)
from atcoder_helper.application.usecases.errors import ConfigAccessError
from atcoder_helper.entities.atcoder_task_config import TaskConfig
from atcoder_helper.entities.atcoder_test_case import AtcoderTestCase
from atcoder_helper.entities.atcoder_test_case import AtCoderTestResult
from atcoder_helper.entities.atcoder_test_case import AtCoderTestStatus


def _get_sut(
    task_config_repo_mock: TaskConfigRepository = mock.MagicMock(),
    test_case_repo_mock: LocalTestCaseRepository = mock.MagicMock(),
    controller_builder: ControllerBuilder = mock.MagicMock(),
) -> ExecuteTestInteractor:
    return ExecuteTestInteractor(
        task_config_repo=task_config_repo_mock,
        test_case_repo=test_case_repo_mock,
        controller_builder=controller_builder,
    )


_task_config = TaskConfig(contest=None, task=None, build=["foo"], run=["bar"])
_test_cases = [
    AtcoderTestCase(name="test_a", given="foo_a", expected="bar_a"),
    AtcoderTestCase(name="test_b", given="foo_b", expected="bar_b"),
    AtcoderTestCase(name="test_c", given="foo_c", expected="bar_c"),
]

_result = AtCoderTestResult("foo", AtCoderTestStatus.AC, "actual", "error", None)

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
        controller_builder=mock.MagicMock(
            build=mock.MagicMock(
                return_value=mock.MagicMock(
                    build=build_mock,
                    execute=execute_mock,
                )
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
