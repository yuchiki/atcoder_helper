"""atcoder_test_case_repoのテスト."""

from typing import Type

import mock
import pytest
import requests
from pytest import MonkeyPatch

from atcoder_helper.repositories.atcoder_test_case_repo import (
    AtCoderTestCaseRepositoryImpl,
)
from atcoder_helper.repositories.errors import ParseError

fetch_test_cases_parameters = {
    "OK": [
        mock.MagicMock(
            return_value=mock.MagicMock(
                text='<div id="task-statement"><span class="lang-ja"></span></div>'
            )
        ),
        None,
    ],
    "Error(通信エラー)": [
        mock.MagicMock(side_effect=Exception()),
        ConnectionError,
    ],
    "Error(parse error)": [
        mock.MagicMock(return_value=mock.MagicMock(text="<foo />")),
        ParseError,
    ],
}


@pytest.mark.parametrize(
    argnames=("get_mock", "exception"),
    argvalues=fetch_test_cases_parameters.values(),
    ids=fetch_test_cases_parameters.keys(),
)
def test_fetch_test_cases(
    get_mock: mock.MagicMock, exception: Type[Exception], monkeypatch: MonkeyPatch
) -> None:
    """fetch_test_casesのテスト."""
    contest = "foo_contest"
    task = "bar_task"
    session = requests.Session()

    sut = AtCoderTestCaseRepositoryImpl()

    monkeypatch.setattr(requests.Session, "get", get_mock)

    if exception:
        with pytest.raises(exception):
            sut.fetch_test_cases(session, contest, task)
    else:
        sut.fetch_test_cases(session, contest, task)
