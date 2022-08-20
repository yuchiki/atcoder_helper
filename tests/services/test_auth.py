"""Tests for AuthServiceImpl."""


import mock
import pytest

from atcoder_helper.services.auth import AuthServiceImpl


class TestAuthServiceImpl:
    """AuthServiceをテストするクラス."""

    @staticmethod
    def _get_sut(
        atcoder_session_repo: mock.MagicMock,
        local_session_repo: mock.MagicMock,
        login_status_repo: mock.MagicMock,
    ) -> AuthServiceImpl:
        return AuthServiceImpl(
            atcoder_session_repo=atcoder_session_repo,
            local_session_repo=local_session_repo,
            login_status_repo=login_status_repo,
        )

    @pytest.mark.skip()
    @staticmethod
    def test_login() -> None:
        """loginのテスト."""

    @pytest.mark.skip()
    @staticmethod
    def test_logout() -> None:
        """logoutのテスト."""

    @pytest.mark.skip()
    @staticmethod
    def test_status() -> None:
        """statusのテスト."""
