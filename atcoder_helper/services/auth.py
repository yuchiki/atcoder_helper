"""認証周りのサービス."""


from typing import Protocol

import atcoder_helper.repositories.errors as repository_error
from atcoder_helper.repositories.atcoder_logged_in_session_repo import (
    AtCoderLoggedInSessionRepository,
)
from atcoder_helper.repositories.logged_in_session_repo import LoggedInSessionRepository
from atcoder_helper.repositories.login_status_repo import LoginStatusRepo
from atcoder_helper.services.errors import AlreadyLoggedIn
from atcoder_helper.services.errors import AtcoderAccessError
from atcoder_helper.services.errors import ConfigAccessError


class AuthService(Protocol):
    """auth を扱うサービスのプロトコル."""

    def login(self, username: str, password: str) -> None:
        """ログインする.

        Args:
            username (str): username
            password (str): password

        Raises:
            AlreadyLoggedIn: 既にログインしている
            ConfigAccessError: 設定ファイルのエラー
            AtcoderAccessError: atcoderから情報を取得する際のエラー
        """

    def logout(self) -> None:
        """logout.

        Raises:
            ConfigAccessError: 設定ファイル読み書きのエラー
        """

    def status(self) -> bool:
        """loginしているかどうかを返す.

        Returns:
            bool: loginしているか

        Raises:
            AtcoderAccessError: atcoder access error
        """


def get_default_auth_service() -> AuthService:
    """AuthServiceの標準実装を返す."""
    return AuthServiceImpl()


class AuthServiceImpl:
    """auth を扱うサービス."""

    _atcoder_session_repo: AtCoderLoggedInSessionRepository
    _local_session_repo: LoggedInSessionRepository
    _login_status_repo: LoginStatusRepo

    def __init__(
        self,
        atcoder_session_repo: AtCoderLoggedInSessionRepository = (
            AtCoderLoggedInSessionRepository()
        ),
        local_session_repo: LoggedInSessionRepository = LoggedInSessionRepository(),
        login_status_repo: LoginStatusRepo = LoginStatusRepo(),
    ):
        """__init__.

        Args:
            atcoder_repo (AtCoderRepository, optional): . Defaults
                to get_default_atcoder_repository().
            atcoder_session_repo (AtCoderLoggedInSessionRepository, optional): _
                Defaults to AtCoderLoggedInSessionRepository().
            local_session_repo (LoggedInSessionRepository, optional): _
                Defaults to LoggedInSessionRepository().
            login_status_repo (LoginStatusRepo, optional): _
                Defaults to LoginStatusRepo().
        """
        self._atcoder_session_repo = atcoder_session_repo
        self._local_session_repo = local_session_repo
        self._login_status_repo = login_status_repo

    def login(self, username: str, password: str) -> None:
        """ログインする.

        Args:
            username (str): username
            password (str): password

        Raises:
            AlreadyLoggedIn: 既にログインしている
            ConfigAccessError: 設定ファイルのエラー
            AtcoderAccessError: atcoderから情報を取得する際のエラー
        """
        try:
            session = self._atcoder_session_repo.read(username, password)
        except (repository_error.ReadError) as e:
            raise ConfigAccessError("設定ファイルの読み込みに失敗しました") from e
        except (repository_error.ConnectionError) as e:
            raise AtcoderAccessError("通信に失敗しました") from e
        except (repository_error.LoginFailure) as e:
            raise AtcoderAccessError("ログインに失敗しました") from e

        if self._login_status_repo.is_logged_in(session):
            raise AlreadyLoggedIn("既にログインしています")

        try:
            self._local_session_repo.write(session)
        except (repository_error.WriteError) as e:
            raise ConfigAccessError("セッションの保存に失敗しました") from e

    def logout(self) -> None:
        """logout.

        Raises:
            ConfigAccessError: 設定ファイル読み書きのエラー
        """
        try:
            self._local_session_repo.delete()
        except (repository_error.ReadError, repository_error.WriteError) as e:
            raise ConfigAccessError("設定ファイルの読み書きに失敗しました") from e

    def status(self) -> bool:
        """loginしているかどうかを返す.

        Returns:
            bool: loginしているか

        Raises:
            AtcoderAccessError: atcoder access error
            ConfigAccessError: config access error
        """
        try:
            session = self._local_session_repo.read()
        except repository_error.ReadError as e:
            raise ConfigAccessError("設定ファイルの読み込みに失敗しました.") from e

        try:
            status = self._login_status_repo.is_logged_in(session)
        except repository_error.ReadError as e:
            raise AtcoderAccessError("atcoderのページとの通信に失敗しました") from e

        return status
