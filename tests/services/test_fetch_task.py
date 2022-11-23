"""Tests for fetch_task."""

from typing import List
from typing import Optional
from typing import Type
from unittest.mock import ANY

import mock
import pytest
import requests

from atcoder_helper.entities.atcoder_task_config import TaskConfig
from atcoder_helper.entities.atcoder_test_case import AtcoderTestCase
from atcoder_helper.repositories.errors import ConnectionError
from atcoder_helper.repositories.errors import ParseError
from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.errors import WriteError
from atcoder_helper.services.errors import AtcoderAccessError
from atcoder_helper.services.errors import ConfigAccessError
from atcoder_helper.services.fetch_task import FetchTaskServiceImpl


def _default_task_config(
    contest: Optional[str] = None, task: Optional[str] = None
) -> TaskConfig:
    return TaskConfig(
        contest=contest,
        task=task,
        build=["gcc", "-omain", "main.c"],
        run=["./main"],
    )


def _default_atcoder_testcases() -> List[AtcoderTestCase]:
    return [AtcoderTestCase(name="foo", given="bar", expected=None)]


def _get_sut(
    task_config_repo_mock: mock.MagicMock,
    test_case_repo_mock: mock.MagicMock,
    session_repo_mock: mock.MagicMock,
    atcoder_testcase_repo_mock: mock.MagicMock,
) -> FetchTaskServiceImpl:
    return FetchTaskServiceImpl(
        task_config_repo=task_config_repo_mock,
        test_case_repo=test_case_repo_mock,
        session_repo=session_repo_mock,
        atcoder_testcase_repo=atcoder_testcase_repo_mock,
    )


test_fetch_task_parameters = {
    "OK(task configではなく、引数でcontest と taskを渡す)": [
        mock.MagicMock(read=mock.MagicMock(return_value=_default_task_config())),
        mock.MagicMock(),
        mock.MagicMock(read=mock.MagicMock(return_value=requests.Session())),
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_atcoder_testcases())
        ),
        "foo_contest",
        "foo_task",
        "foo_contest",
        "foo_task",
        None,
    ],
    "OK(task configと引数でcontest と taskが渡された場合、引数が優先)": [
        mock.MagicMock(
            read=mock.MagicMock(
                return_value=_default_task_config("config_contest", "config_task")
            )
        ),
        mock.MagicMock(),
        mock.MagicMock(read=mock.MagicMock(return_value=requests.Session())),
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_atcoder_testcases())
        ),
        "given_contest",
        "given_task",
        "given_contest",
        "given_task",
        None,
    ],
    "OK(contestがtask configで渡されていれば引数で渡されなくてもよい)": [
        mock.MagicMock(
            read=mock.MagicMock(return_value=_default_task_config(contest="foo"))
        ),
        mock.MagicMock(),
        mock.MagicMock(read=mock.MagicMock(return_value=requests.Session())),
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_atcoder_testcases())
        ),
        None,
        "given_task",
        "foo",
        "given_task",
        None,
    ],
    "OK(taskがtask configで渡されていれば引数で渡されなくてもよい)": [
        mock.MagicMock(
            read=mock.MagicMock(return_value=_default_task_config(task="bar"))
        ),
        mock.MagicMock(),
        mock.MagicMock(read=mock.MagicMock(return_value=requests.Session())),
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_atcoder_testcases())
        ),
        "foo_contest",
        None,
        "foo_contest",
        "bar",
        None,
    ],
    "contestが取得できないとエラー": [
        mock.MagicMock(read=mock.MagicMock(return_value=_default_task_config())),
        mock.MagicMock(),
        mock.MagicMock(read=mock.MagicMock(return_value=requests.Session())),
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_atcoder_testcases())
        ),
        None,
        "foo_task",
        None,
        None,
        ConfigAccessError,
    ],
    "taskが取得できないとエラー": [
        mock.MagicMock(read=mock.MagicMock(return_value=_default_task_config())),
        mock.MagicMock(),
        mock.MagicMock(read=mock.MagicMock(return_value=requests.Session())),
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_atcoder_testcases())
        ),
        "foo_contest",
        None,
        None,
        None,
        ConfigAccessError,
    ],
    "task_config_repo readエラーでエラー": [
        mock.MagicMock(read=mock.MagicMock(side_effect=ReadError)),
        mock.MagicMock(),
        mock.MagicMock(read=mock.MagicMock(return_value=requests.Session())),
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_atcoder_testcases())
        ),
        "foo_contest",
        "foo_task",
        None,
        None,
        ConfigAccessError,
    ],
    "task_config_repo parseエラーでエラー": [
        mock.MagicMock(read=mock.MagicMock(side_effect=ReadError)),
        mock.MagicMock(),
        mock.MagicMock(read=mock.MagicMock(return_value=requests.Session())),
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_atcoder_testcases())
        ),
        "foo_contest",
        "foo_task",
        None,
        None,
        ConfigAccessError,
    ],
    "セッションが読み込めなかったらエラー": [
        mock.MagicMock(read=mock.MagicMock(return_value=_default_task_config())),
        mock.MagicMock(),
        mock.MagicMock(read=mock.MagicMock(side_effect=ReadError())),
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_atcoder_testcases())
        ),
        "foo_contest",
        "foo_task",
        None,
        None,
        ConfigAccessError,
    ],
    "テストケースのフェッチに失敗したらエラー": [
        mock.MagicMock(read=mock.MagicMock(return_value=_default_task_config())),
        mock.MagicMock(),
        mock.MagicMock(read=mock.MagicMock(return_value=requests.Session())),
        mock.MagicMock(fetch_test_cases=mock.MagicMock(side_effect=ConnectionError())),
        "foo_contest",
        "foo_task",
        "foo_contest",
        "foo_task",
        AtcoderAccessError,
    ],
    "テストケースのparseに失敗したらエラー": [
        mock.MagicMock(read=mock.MagicMock(return_value=_default_task_config())),
        mock.MagicMock(),
        mock.MagicMock(read=mock.MagicMock(return_value=requests.Session())),
        mock.MagicMock(fetch_test_cases=mock.MagicMock(side_effect=ParseError())),
        "foo_contest",
        "foo_task",
        "foo_contest",
        "foo_task",
        AtcoderAccessError,
    ],
    "error(テストケースの書き込みに失敗)": [
        mock.MagicMock(read=mock.MagicMock(return_value=_default_task_config())),
        mock.MagicMock(write=mock.MagicMock(side_effect=WriteError())),
        mock.MagicMock(read=mock.MagicMock(return_value=requests.Session())),
        mock.MagicMock(
            fetch_test_cases=mock.MagicMock(return_value=_default_atcoder_testcases())
        ),
        "foo_contest",
        "foo_task",
        "foo_contest",
        "foo_task",
        ConfigAccessError,
    ],
}


@pytest.mark.parametrize(
    argnames=(
        "task_config_repo_mock",
        "test_case_repo_mock",
        "session_repo_mock",
        "atcoder_testcase_repo_mock",
        "contest",
        "task",
        "fetched_contest",
        "fetched_task",
        "exception",
    ),
    argvalues=test_fetch_task_parameters.values(),
    ids=test_fetch_task_parameters.keys(),
)
def test_fetch_task(
    task_config_repo_mock: mock.MagicMock,
    test_case_repo_mock: mock.MagicMock,
    session_repo_mock: mock.MagicMock,
    atcoder_testcase_repo_mock: mock.MagicMock,
    contest: Optional[str],
    task: Optional[str],
    fetched_contest: Optional[str],
    fetched_task: Optional[str],
    exception: Type[Exception],
) -> None:
    """fetch_taskをテストする."""
    sut = _get_sut(
        task_config_repo_mock,
        test_case_repo_mock,
        session_repo_mock,
        atcoder_testcase_repo_mock,
    )

    if exception:
        with pytest.raises(exception):
            sut.fetch_task(contest, task)
    else:
        sut.fetch_task(contest, task)

    if fetched_contest is not None:
        atcoder_testcase_repo_mock.fetch_test_cases.assert_called_with(
            session=ANY, contest=fetched_contest, task=fetched_task
        )
