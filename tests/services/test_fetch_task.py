"""Tests for fetch_task."""

from typing import Dict
from typing import Optional
from typing import Type

import mock
import pytest

from atcoder_helper.models.task_config import TaskConfig
from atcoder_helper.models.test_case import AtcoderTestCase
from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.errors import WriteError
from atcoder_helper.repositories.task_config_repo import TaskConfigRepository
from atcoder_helper.repositories.test_case_repo import TestCaseRepository
from atcoder_helper.services.errors import AtcoderAccessError
from atcoder_helper.services.errors import ConfigAccessError


def _default_task_config(
    contest: Optional[str] = None, task: Optional[str] = None
) -> TaskConfig:
    return TaskConfig(
        contest=contest,
        task=task,
        build=["gcc", "-omain", "main.c"],
        run=["./main"],
    )


_default_test_cases = [
    AtcoderTestCase(name="case1", given="input1", expected="expected1"),
    AtcoderTestCase(name="case2", given="input2", expected="expected2"),
    AtcoderTestCase(name="case3", given="input3", expected="expected3"),
]


# def _get_sut(
#    atcoder_repo_mock: AtCoderRepository = mock.MagicMock(),
#    task_config_repo_mock: TaskConfigRepository = mock.MagicMock(),
#    test_case_repo_mock: TestCaseRepository = mock.MagicMock(),
# ) -> FetchTaskServiceImpl:
#    return FetchTaskServiceImpl(
#        atcoder_repo=atcoder_repo_mock,
#        task_config_repo=task_config_repo_mock,
#        test_case_repo=test_case_repo_mock,
#    )


test_fetch_task_params = {
    "taskとconfigは指定されないが設定ファイルから取られる": (
        None,
        None,
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_test_cases)
        ),
        mock.MagicMock(
            read=mock.MagicMock(
                return_value=_default_task_config("foo_config", "bar_config")
            )
        ),
        mock.MagicMock(),
        None,
        {"contest": "foo_config", "task": "bar_config"},
        _default_test_cases,
    ),
    "taskのみ指定されており、contestは設定ファイルから、taskは引数から取られる": (
        None,
        "bar",
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_test_cases)
        ),
        mock.MagicMock(
            read=mock.MagicMock(
                return_value=_default_task_config("foo_config", "bar_config")
            )
        ),
        mock.MagicMock(),
        None,
        {"contest": "foo_config", "task": "bar"},
        _default_test_cases,
    ),
    "contestのみ指定されており、taskは設定ファイルから、contestは引数から取られる": (
        "foo",
        None,
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_test_cases)
        ),
        mock.MagicMock(
            read=mock.MagicMock(
                return_value=_default_task_config("foo_config", "bar_config")
            )
        ),
        mock.MagicMock(),
        None,
        {"contest": "foo", "task": "bar_config"},
        _default_test_cases,
    ),
    "contestもtaskも指定されており、configよりも優先される": (
        "foo",
        "bar",
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_test_cases)
        ),
        mock.MagicMock(
            read=mock.MagicMock(
                return_value=_default_task_config("foo_config", "bar_config")
            )
        ),
        mock.MagicMock(),
        None,
        {"contest": "foo", "task": "bar"},
        _default_test_cases,
    ),
    "flagが指定されていれば、configにcontest/taskがなくてもよい": (
        "foo",
        "bar",
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_test_cases)
        ),
        mock.MagicMock(read=mock.MagicMock(return_value=_default_task_config())),
        mock.MagicMock(),
        None,
        {"contest": "foo", "task": "bar"},
        _default_test_cases,
    ),
    "flagからもconfigからもtaskが取得できないとエラー": (
        "foo",
        None,
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_test_cases)
        ),
        mock.MagicMock(
            read=mock.MagicMock(return_value=_default_task_config("foo_contest", None))
        ),
        mock.MagicMock(),
        ConfigAccessError,
        None,
        None,
    ),
    "flagからもconfigからもcontestが取得できないとエラー": (
        None,
        "bar",
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_test_cases)
        ),
        mock.MagicMock(
            read=mock.MagicMock(return_value=_default_task_config(None, "bar_config"))
        ),
        mock.MagicMock(),
        ConfigAccessError,
        None,
        None,
    ),
    "設定ファイルの読みこみに失敗したらエラー": (
        "foo",
        "bar",
        mock.MagicMock(),
        mock.MagicMock(read=mock.MagicMock(side_effect=ReadError())),
        mock.MagicMock(),
        ConfigAccessError,
        None,
        None,
    ),
    "テストケースの取得に失敗したらエラー": (
        "foo",
        "bar",
        mock.MagicMock(fetch_test_cases=mock.MagicMock(side_effect=ReadError())),
        mock.MagicMock(read=mock.MagicMock(return_value=_default_task_config)),
        mock.MagicMock(),
        AtcoderAccessError,
        None,
        None,
    ),
    "テストケースのン書き込みに失敗したらエラー": (
        "foo",
        "bar",
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_test_cases)
        ),
        mock.MagicMock(
            read=mock.MagicMock(
                return_value=_default_task_config("foo_config", "bar_config")
            )
        ),
        mock.MagicMock(write=mock.MagicMock(side_effect=WriteError())),
        ConfigAccessError,
        {"contest": "foo", "task": "bar"},
        _default_test_cases,
    ),
}


# @pytest.mark.parametrize(
#    (
#        "contest",
#        "task",
#        "atcoder_repo_mock",
#        "task_config_repo_mock",
#        "test_case_repo_mock",
#        "exception",
#        "given_to_atcoder_repo",
#        "given_to_test_case_repo",
#    ),
#    list(test_fetch_task_params.values()),
#    ids=list(test_fetch_task_params.keys()),
# )
@pytest.mark.skip()
def test_fetch_task(
    task_config_repo_mock: TaskConfigRepository,
    test_case_repo_mock: TestCaseRepository,
    contest: Optional[str],
    task: Optional[str],
    exception: Type[Exception],
    given_to_atcoder_repo: Optional[Dict[str, str]],
    given_to_test_case_repo: Optional[AtcoderTestCase],
) -> None:
    """fetch_taskのテスト."""


#    sut = _get_sut(
#        atcoder_repo_mock=atcoder_repo_mock,
#        task_config_repo_mock=task_config_repo_mock,
#        test_case_repo_mock=test_case_repo_mock,
#    )
#
#    if exception:
#        with pytest.raises(exception):
#            sut.fetch_task(contest, task)
#    else:
#        sut.fetch_task(contest, task)
#
#    if given_to_atcoder_repo is not None:
#        repo_fetch_mock = cast(mock.MagicMock, sut._atcoder_repo.fetch_test_cases)
#        repo_fetch_mock.assert_called_once_with(**given_to_atcoder_repo)
#
#    if given_to_test_case_repo is not None:
#        write_mock = cast(mock.MagicMock, sut._test_case_repo.write)
#        write_mock.assert_called_once_with(given_to_test_case_repo)
