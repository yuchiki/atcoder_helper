"""logged_in_session_repoのテスト."""


from typing import Type

import mock
import pytest
import requests
from pytest import MonkeyPatch

from atcoder_helper.repositories.atcoder_logged_in_session_repo import (
    AtCoderLoggedInSessionRepositoryImpl,
)
from atcoder_helper.repositories.errors import ConnectionError
from atcoder_helper.repositories.errors import LoginFailure
from atcoder_helper.repositories.errors import ParseError

test_read_parameter = {
    "OK": [
        mock.MagicMock(return_value=mock.MagicMock(text='<input value="foo"/>')),
        mock.MagicMock(return_value=mock.MagicMock(headers={"Location": "/home"})),
        None,
    ],
    "error(get失敗)": [
        mock.MagicMock(side_effect=Exception()),
        mock.MagicMock(),
        ConnectionError,
    ],
    "error(parser失敗)": [
        mock.MagicMock(return_value=mock.MagicMock(text="<input/>")),
        mock.MagicMock(return_value=mock.MagicMock(headers={"Location": "/home"})),
        ParseError,
    ],
    "error(POST失敗)": [
        mock.MagicMock(return_value=mock.MagicMock(text='<input value="foo"/>')),
        mock.MagicMock(side_effect=Exception),
        ConnectionError,
    ],
    "error(ログイン失敗)": [
        mock.MagicMock(return_value=mock.MagicMock(text='<input value="foo"/>')),
        mock.MagicMock(return_value=mock.MagicMock(headers={"Location": "/foo"})),
        LoginFailure,
    ],
}


@pytest.mark.parametrize(
    argnames=("get_mock", "post_mock", "exception"),
    argvalues=test_read_parameter.values(),
    ids=test_read_parameter.keys(),
)
def test_read(
    get_mock: mock.MagicMock,
    post_mock: mock.MagicMock,
    exception: Type[Exception],
    monkeypatch: MonkeyPatch,
) -> None:
    """readのテスト.

    sessionの検証は難しいのでやらない
    """
    username = "name"
    password = "password"
    sut = AtCoderLoggedInSessionRepositoryImpl()

    monkeypatch.setattr(requests.Session, "get", get_mock)
    monkeypatch.setattr(requests.Session, "post", post_mock)

    if exception:
        with pytest.raises(exception):
            sut.read(username, password)
    else:
        sut.read(username, password)
