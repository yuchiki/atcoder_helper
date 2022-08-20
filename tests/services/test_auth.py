"""Tests for AuthServiceImpl."""

from typing import Type

import mock
import pytest

from atcoder_helper import repositories
from atcoder_helper.repositories.atcoder_repo import AtCoderRepository
from atcoder_helper.services.auth import AuthServiceImpl
from atcoder_helper.services.errors import AlreadyLoggedIn
from atcoder_helper.services.errors import AtcoderAccessError
from atcoder_helper.services.errors import ConfigAccessError


class TestAuthServiceImpl:
    """AuthServiceをテストするクラス."""

    @staticmethod
    def _get_sut(
        atcoder_repo_mock: AtCoderRepository = mock.MagicMock(),
    ) -> AuthServiceImpl:
        return AuthServiceImpl(atcoder_repo=atcoder_repo_mock)

    @staticmethod
    @pytest.mark.parametrize(
        [
            "repo_login_side_effect",
            "exception",
        ],
        [
            [None, None],
            [None, None],
            [repositories.errors.AlreadyLoggedIn(), AlreadyLoggedIn],
            [repositories.errors.ReadError(), ConfigAccessError],
            [repositories.errors.WriteError(), ConfigAccessError],
            [repositories.errors.LoginFailure(), AtcoderAccessError],
        ],
    )
    def test_login(
        repo_login_side_effect: Exception,
        exception: Type[Exception],
    ) -> None:
        """loginのテスト."""
        username = "foo"
        password = "bar"

        sut = TestAuthServiceImpl._get_sut(
            atcoder_repo_mock=mock.MagicMock(
                login=mock.MagicMock(side_effect=repo_login_side_effect)
            )
        )

        if exception:
            with pytest.raises(exception):
                sut.login(username, password)
        else:
            sut.login(username, password)

    @staticmethod
    @pytest.mark.parametrize(
        ("repo_logout_side_effect", "side_effect"),
        [
            [None, None],
            [repositories.errors.ReadError(), ConfigAccessError],
            [repositories.errors.WriteError(), ConfigAccessError],
        ],
    )
    def test_logout(
        repo_logout_side_effect: Exception, side_effect: Type[Exception]
    ) -> None:
        """logoutのテスト."""
        sut = TestAuthServiceImpl._get_sut(
            atcoder_repo_mock=mock.MagicMock(
                logout=mock.MagicMock(side_effect=repo_logout_side_effect)
            )
        )

        if side_effect:
            with pytest.raises(side_effect):
                sut.logout()
        else:
            sut.logout()

    @staticmethod
    @pytest.mark.parametrize(
        (
            "is_logged_in_side_effect",
            "is_logged_in_return_value",
            "side_effect",
            "return_value",
        ),
        [
            [None, False, None, False],
            [None, True, None, True],
            [repositories.errors.ReadError(), False, AtcoderAccessError, False],
        ],
    )
    def test_status(
        is_logged_in_side_effect: Exception,
        is_logged_in_return_value: bool,
        side_effect: Type[Exception],
        return_value: bool,
    ) -> None:
        """statusのテスト."""
        sut = TestAuthServiceImpl._get_sut(
            atcoder_repo_mock=mock.MagicMock(
                is_logged_in=mock.MagicMock(
                    side_effect=is_logged_in_side_effect,
                    return_value=is_logged_in_return_value,
                )
            )
        )

        if side_effect:
            with pytest.raises(side_effect):
                sut.status()
        else:
            assert sut.status() == return_value
