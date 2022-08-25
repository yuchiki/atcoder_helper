"""認証周りのサービス."""


from typing import Protocol

import atcoder_helper.repositories.errors as repository_error
from atcoder_helper.repositories.atcoder_logged_in_session_repo import (
    AtCoderLoggedInSessionRepository,
)
from atcoder_helper.repositories.atcoder_logged_in_session_repo import (
    get_default_atcoder_session_repository,
)
from atcoder_helper.repositories.logged_in_session_repo import LoggedInSessionRepository
from atcoder_helper.repositories.logged_in_session_repo import (
    get_default_session_repository,
)
from atcoder_helper.repositories.login_status_repo import LoginStatusRepo
from atcoder_helper.repositories.login_status_repo import get_default_login_status_repo
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
            ConfigAccessError: 設定ファイルのエラー
            AtcoderAccessError: atcoderから情報を取得する際のエラー
            AlreadyLoggedIn: 既にログインしている # 今は返さないけど今後かなりの高確率で返しうるので書いておく
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
    return AuthServiceImpl(
        atcoder_session_repo=(get_default_atcoder_session_repository()),
        local_session_repo=(get_default_session_repository()),
        login_status_repo=get_default_login_status_repo(),
    )


class AuthServiceImpl:
    """auth を扱うサービス."""

    _atcoder_session_repo: AtCoderLoggedInSessionRepository
    _local_session_repo: LoggedInSessionRepository
    _login_status_repo: LoginStatusRepo

    def __init__(
        self,
        atcoder_session_repo: AtCoderLoggedInSessionRepository,
        local_session_repo: LoggedInSessionRepository,
        login_status_repo: LoginStatusRepo,
    ):
        """__init__.

        Args:
            atcoder_repo (AtCoderRepository, optional): _
            atcoder_session_repo (AtCoderLoggedInSessionRepository, optional): _
            local_session_repo (LoggedInSessionRepository, optional): _
            login_status_repo (LoginStatusRepo, optional): _
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
            ConfigAccessError: 設定ファイルのエラー
            AtcoderAccessError: atcoderから情報を取得する際のエラー
            AlreadyLoggedInError: 既にログインしている
        """
        try:
            session = self._atcoder_session_repo.read(username, password)
        except repository_error.ConnectionError as e:
            raise AtcoderAccessError("通信に失敗しました") from e
        except repository_error.ParseError as e:
            raise AtcoderAccessError("パースに失敗しました.") from e
        except repository_error.LoginFailure as e:
            raise AtcoderAccessError("ログインに失敗しました") from e

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
        except (repository_error.WriteError) as e:
            raise ConfigAccessError("設定ファイルの書き込みに失敗しました") from e

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
