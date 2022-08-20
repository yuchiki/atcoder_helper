"""atcoderとの通信を行う層."""
import os
import pickle
from typing import Final
from typing import List
from typing import Protocol
from typing import cast

import requests
from bs4 import BeautifulSoup

from atcoder_helper.models.test_case import AtcoderTestCase
from atcoder_helper.repositories.errors import AlreadyLoggedIn
from atcoder_helper.repositories.errors import ParseError
from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.errors import WriteError
from atcoder_helper.repositories.login_status_repo import LoginStatusRepo
from atcoder_helper.repositories.utils import AtCoderURLProvider


class AtCoderRepository(Protocol):
    """AtCoderとの通信を抽象化するためのプロトコル."""

    def login(self, username: str, password: str) -> bool:
        """atcoderにloginする.入力したユーザーネームとパスワードは保存されず、代わりにセッションが保存される.

        Args:
            username (str): username
            password (str): password

        Raises:
            AlreadyLoggedIn: 既にログインしていたとき
            WriteError: POSTに失敗

        Returns:
            bool: ログインに成功したかどうかを返す
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

    _session: requests.Session

    url_provider = AtCoderURLProvider

    _default_session_file: Final[str] = os.path.join(
        os.path.expanduser("~"), ".atcoder_helper", "session", "session_dump.pkl"
    )

    def __init__(self, session_filename: str = _default_session_file):
        """__init__.

        Args:
            session_filename (str): セッションを保存しておくファイル名

        Raises:
            ReadError: 読み込みに失敗した
        """
        self._session_filename = session_filename
        if os.path.isfile(session_filename):
            try:
                with open(session_filename, "rb") as file:
                    self._session = pickle.load(file)
            except OSError as e:
                raise ReadError(f"cannot open {session_filename}") from e
        else:
            self._session = requests.session()

    def _write_session(self) -> None:
        """_write_session.

        Raises:
            WriteError: 書き込みに失敗
        """
        os.makedirs(os.path.dirname(self._session_filename), exist_ok=True)

        try:
            with open(self._session_filename, "wb") as file:
                pickle.dump(self._session, file)
        except OSError as e:
            raise WriteError(f"cannot write to {self._session_filename}") from e

    def _get_csrf_token(self) -> str:
        login_page = self._session.get(self.url_provider.login_url)
        html = BeautifulSoup(login_page.text, "html.parser")

        token = html.find("input").attrs["value"]
        return cast(str, token)  # TODO(ちゃんと例外処理をする)

    def login(self, username: str, password: str) -> bool:
        """atcoderにloginする.入力したユーザーネームとパスワードは保存されず、代わりにセッションが保存される.

        Args:
            username (str): username
            password (str): password

        Raises:
            AlreadyLoggedIn: 既にログインしていたとき
            WriteError: POSTに失敗

        Returns:
            bool: ログインに成功したかどうかを返す
        """
        if self.is_logged_in():
            raise AlreadyLoggedIn("すでにloginしています")

        csrf_token = self._get_csrf_token()

        try:
            res = self._session.post(
                self.url_provider.login_url,
                params={
                    "username": username,
                    "password": password,
                    "csrf_token": csrf_token,
                },
                allow_redirects=False,
            )
        except Exception as e:
            raise WriteError(f"cannot post to {self.url_provider.login_url}") from e

        if res.headers["Location"] == "/home":
            self._write_session()
            return True
        else:
            return False

    def logout(self) -> None:
        """logoutする. loginしていない状態でも何も検査しない.

        Raises:
            WriteError: セッションの初期化に失敗
        """
        self._session = requests.session()

        self._write_session()

    def is_logged_in(self) -> bool:
        """loginしているかどうかを判定する.

        Raises:
            ReadError: タスクGETに失敗

        Returns:
            bool: loginしているか否か
        """
        status_repo = LoginStatusRepo(self._session)
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

        def normalize_newline(text: str) -> str:
            return "\n".join(text.splitlines())

        try:
            task_page = self._session.get(self.url_provider.task_url(contest, task))
        except Exception as e:
            raise ReadError(
                f"cannot GET {self.url_provider.task_url(contest, task)}"
            ) from e

        try:
            html = BeautifulSoup(task_page.text, "html.parser")

            sections = (
                html.find("div", id="task-statement")
                .find("span", attrs={"class": "lang-ja"})
                .find_all("section")
            )

            input_sections = {
                section.find("h3").text.split()[1]: normalize_newline(
                    section.find("pre").text
                )
                for section in sections
                if "入力例" in section.find("h3").text
            }

            output_sections = {
                section.find("h3").text.split()[1]: normalize_newline(
                    section.find("pre").text
                )
                for section in sections
                if "出力例" in section.find("h3").text
            }
        except Exception as e:
            raise ParseError() from e

        return [
            AtcoderTestCase(
                name=f"case-{name}", given=given, expected=output_sections[name]
            )
            for (name, given) in input_sections.items()
        ]
