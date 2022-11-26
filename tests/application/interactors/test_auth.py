"""Tests for AuthInteractor."""


from typing import Type

import mock
import pytest
import requests

from atcoder_helper.application.interactors.auth import AuthInteractor
from atcoder_helper.application.repositories.errors import ConnectionError
from atcoder_helper.application.repositories.errors import LoginFailure
from atcoder_helper.application.repositories.errors import ParseError
from atcoder_helper.application.repositories.errors import ReadError
from atcoder_helper.application.repositories.errors import WriteError
from atcoder_helper.application.usecases.errors import AtcoderAccessError
from atcoder_helper.application.usecases.errors import ConfigAccessError


def _get_sut(
    atcoder_session_repo: mock.MagicMock,
    local_session_repo: mock.MagicMock,
    login_status_repo: mock.MagicMock,
) -> AuthInteractor:
    return AuthInteractor(
        atcoder_session_repo=atcoder_session_repo,
        local_session_repo=local_session_repo,
        login_status_repo=login_status_repo,
    )


test_login_input = {
    "OK": [
        mock.MagicMock(read=mock.MagicMock(return_value=requests.Session())),
        mock.MagicMock(),
        mock.MagicMock(is_logged_in=mock.MagicMock(return_value=False)),
        None,
    ],
    "atcoder_session_repoがConnection Errorのときエラー": [
        mock.MagicMock(read=mock.MagicMock(side_effect=ConnectionError())),
        mock.MagicMock(),
        mock.MagicMock(),
        AtcoderAccessError,
    ],
    "atcoder_session_repoがParse Errorのときエラー": [
        mock.MagicMock(read=mock.MagicMock(side_effect=ParseError())),
        mock.MagicMock(),
        mock.MagicMock(),
        AtcoderAccessError,
    ],
    "atcoder_session_repoがLogin Failureのときエラー": [
        mock.MagicMock(read=mock.MagicMock(side_effect=LoginFailure())),
        mock.MagicMock(),
        mock.MagicMock(),
        AtcoderAccessError,
    ],
    "session_repoがWriteErrorのときエラー": [
        mock.MagicMock(read=mock.MagicMock(return_value=requests.Session())),
        mock.MagicMock(write=mock.MagicMock(side_effect=WriteError)),
        mock.MagicMock(),
        ConfigAccessError,
    ],
}


@pytest.mark.parametrize(
    argnames=(
        "atcoder_session_repo",
        "local_session_repo",
        "login_status_repo",
        "exception",
    ),
    argvalues=test_login_input.values(),
    ids=test_login_input.keys(),
)
def test_login(
    atcoder_session_repo: mock.MagicMock,
    local_session_repo: mock.MagicMock,
    login_status_repo: mock.MagicMock,
    exception: Type[Exception],
) -> None:
    """loginのテスト."""
    username = "foo"
    password = "bar"

    sut = _get_sut(atcoder_session_repo, local_session_repo, login_status_repo)

    if exception:
        with pytest.raises(exception):
            sut.login(username, password)
    else:
        sut.login(username, password)


test_logout_input = {
    "OK": [mock.MagicMock(), None],
    "delete がerrorを返したらエラー": [
        mock.MagicMock(delete=mock.MagicMock(side_effect=WriteError)),
        ConfigAccessError,
    ],
}


@pytest.mark.parametrize(
    argnames=(
        "local_session_repo",
        "exception",
    ),
    argvalues=test_logout_input.values(),
    ids=test_logout_input.keys(),
)
def test_logout(local_session_repo: mock.MagicMock, exception: Type[Exception]) -> None:
    """logoutのテスト."""
    sut = _get_sut(
        atcoder_session_repo=mock.MagicMock(),
        local_session_repo=local_session_repo,
        login_status_repo=mock.MagicMock(),
    )

    if exception:
        with pytest.raises(exception):
            sut.logout()
    else:
        sut.logout()


test_status_input = {
    "OK": [
        mock.MagicMock(read=mock.MagicMock(return_value=requests.Session())),
        mock.MagicMock(),
        None,
    ],
    "session readに失敗したらエラー": [
        mock.MagicMock(read=mock.MagicMock(side_effect=ReadError)),
        mock.MagicMock(),
        ConfigAccessError,
    ],
    "is_logged_in に失敗したらエラー": [
        mock.MagicMock(read=mock.MagicMock(return_value=requests.Session())),
        mock.MagicMock(is_logged_in=mock.MagicMock(side_effect=ReadError())),
        AtcoderAccessError,
    ],
}


@pytest.mark.parametrize(
    argnames=(
        "local_session_repo",
        "login_status_repo",
        "exception",
    ),
    argvalues=test_status_input.values(),
    ids=test_status_input.keys(),
)
def test_status(
    local_session_repo: mock.MagicMock,
    login_status_repo: mock.MagicMock,
    exception: Type[Exception],
) -> None:
    """statusのテスト."""
    sut = _get_sut(mock.MagicMock(), local_session_repo, login_status_repo)

    if exception:
        with pytest.raises(exception):
            sut.status()
    else:
        sut.status()
