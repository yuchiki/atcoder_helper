"""atcoderとの通信を行う層."""
import os
from typing import Final
from typing import List
from typing import Protocol

from atcoder_helper.models.test_case import AtcoderTestCase
from atcoder_helper.repositories.atcoder_logged_in_session_repo import (
    AtCoderLoggedInSessionRepository,
)
from atcoder_helper.repositories.atcoder_test_case_repo import AtCoderTestCaseRepository
from atcoder_helper.repositories.errors import AlreadyLoggedIn
from atcoder_helper.repositories.logged_in_session_repo import LoggedInSessionRepository
from atcoder_helper.repositories.login_status_repo import LoginStatusRepo
from atcoder_helper.repositories.utils import AtCoderURLProvider


class AtCoderRepository(Protocol):
    """AtCoderとの通信を抽象化するためのプロトコル."""

    def login(self, username: str, password: str) -> None:
        """atcoderにloginする.入力したユーザーネームとパスワードは保存されず、代わりにセッションが保存される.

        Args:
            username (str): username
            password (str): password

        Raises:
            AlreadyLoggedIn: 既にログインしていたとき
            ConnectionError: POSTに失敗
            LoginFailure: ログインに失敗
        """

    def logout(self) -> None:
        """logoutする. loginしていない状態でも何も検査しない.

        Raises:
            WriteError: セッションの初期化に失敗
        """

    def is_logged_in(self) -> bool:
        """loginしているかどうかを判定する.

        Raises:
            ReadError: タスクGETに失敗

        Returns:
            bool: loginしているか否か
        """

    def fetch_test_cases(self, contest: str, task: str) -> List[AtcoderTestCase]:
        """テストケーススイートを取得する.

        Args:
            contest (str): コンテスト名
            task (str): タスク名

        Raises:
            ReadError: GETに失敗
            ParseError: Parseに失敗

        Returns:
            List[TestCase]: テストケーススイート
        """


def get_default_atcoder_repository() -> AtCoderRepository:
    """AtCoderRepositoryの 標準実装を返す."""
    return AtCoderRepositoryImpl()


class AtCoderRepositoryImpl:
    """AtCoderと通信するためのクラス.

    TODO(データに対するrepositoryになっていないので切り分ける必要がある)
    """

    url_provider = AtCoderURLProvider

    _default_session_file: Final[str] = os.path.join(
        os.path.expanduser("~"), ".atcoder_helper", "session", "session_dump.pkl"
    )

    _session_repo: LoggedInSessionRepository

    def __init__(self, session_filename: str = _default_session_file):
        """__init__.

        Args:
            session_filename (str): セッションを保存しておくファイル名

        Raises:
            ReadError: 読み込みに失敗した
        """
        self._session_repo = LoggedInSessionRepository(
            session_filename=session_filename
        )

    def login(self, username: str, password: str) -> None:
        """atcoderにloginする.入力したユーザーネームとパスワードは保存されず、代わりにセッションが保存される.

        Args:
            username (str): username
            password (str): password

        Raises:
            AlreadyLoggedIn: 既にログインしていたとき
            ConnectionError: POSTに失敗
            LoginFailure: ログインに失敗
        """
        if self.is_logged_in():
            raise AlreadyLoggedIn("すでにloginしています")

        atcoder_session_repo = AtCoderLoggedInSessionRepository()
        session = atcoder_session_repo.read(username=username, password=password)

        self._session_repo.write(session)

    def logout(self) -> None:
        """logoutする. loginしていない状態でも何も検査しない.

        Raises:
            WriteError: セッションの初期化に失敗
        """
        self._session_repo.delete()

    def is_logged_in(self) -> bool:
        """loginしているかどうかを判定する.

        Raises:
            ReadError: タスクGETに失敗

        Returns:
            bool: loginしているか否か
        """
        session = self._session_repo.read()
        status_repo = LoginStatusRepo(session)
        return status_repo.is_logged_in()

    def fetch_test_cases(self, contest: str, task: str) -> List[AtcoderTestCase]:
        """テストケーススイートを取得する.

        Args:
            contest (str): コンテスト名
            task (str): タスク名

        Raises:
            ReadError: GETに失敗
            ParseError: Parseに失敗

        Returns:
            List[TestCase]: テストケーススイート
        """
        session = self._session_repo.read()
        atcoder_test_case_repo = AtCoderTestCaseRepository(session)
        return atcoder_test_case_repo.fetch_test_cases(contest, task)
