"""atcoderとの通信を行う層."""
import os
import pickle
from typing import Final
from typing import List
from typing import cast

import requests
from bs4 import BeautifulSoup

from atcoder_helper.models.test_case import AtcoderTestCase


class AlreadyLoggedIn(Exception):
    """既にログインしているエラー."""

    pass


class AtCoderRepository:
    """AtCoderとの通信を抽象化するためのクラス."""

    _atcoder_url: Final[str] = "https://atcoder.jp"
    _login_url: Final[str] = f"{_atcoder_url}/login"

    def _contest_url(self, contest: str) -> str:
        return f"{self._atcoder_url}/contests/{contest}"

    def _task_url(self, contest: str, task: str) -> str:
        return f"{self._contest_url(contest)}/tasks/{contest}_{task}"

    def _submit_url(self, contest: str) -> str:
        return f"{self._contest_url(contest)}/submit"

    def __init__(self, session_filename: str):
        """__init__.

        Args:
            session_filename (str): セッションを保存しておくファイル名
        """
        self._session_filename = session_filename
        if os.path.isfile(session_filename):
            with open(session_filename, "rb") as file:
                self._session = pickle.load(file)
        else:
            self._session = requests.session()

    def _write_session(self) -> None:
        with open(self._session_filename, "wb") as file:
            pickle.dump(self._session, file)

    def _get_csrf_token(self) -> str:
        login_page = self._session.get(self._login_url, cookies="")
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

        Returns:
            bool: ログインに成功したかどうかを返す
        """
        if self.is_logged_in():
            raise AlreadyLoggedIn("すでにloginしています")

        csrf_token = self._get_csrf_token()

        res = self._session.post(
            self._login_url,
            params={
                "username": username,
                "password": password,
                "csrf_token": csrf_token,
            },
            allow_redirects=0,
        )

        if res.headers["Location"] == "/home":
            self._write_session()
            return True
        else:
            return False

    def logout(self) -> None:
        """logoutする.loginしていない状態でも何も検査しない."""
        self._session = requests.session()
        self._write_session()

    def is_logged_in(self) -> bool:
        """loginしているかどうかを判定する.

        Returns:
            bool: loginしているか否か
        """
        # たたもさんの atcoder-cli を参考にしている
        #  https://github.com/Tatamo/atcoder-cli/blob/0ca0d088f28783a4804ad90d89fc56eb7ddd6ef4/src/atcoder.ts#L46

        res = cast(
            requests.Response,
            self._session.get(self._submit_url("abc001"), allow_redirects=0),
        )  # TODO(any処理)
        return res.status_code == 200  # login していなければ302 redirect になる

    def fetch_test_cases(self, contest: str, task: str) -> List[AtcoderTestCase]:
        """テストケーススイートを取得する.

        Args:
            contest (str): コンテスト名
            task (str): タスク名

        Returns:
            List[TestCase]: テストケーススイート
        """

        def normalize_newline(text: str) -> str:
            return "\n".join(text.splitlines())

        task_page = self._session.get(self._task_url(contest, task))
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

        return [
            AtcoderTestCase(f"case-{name}", given, output_sections[name])
            for (name, given) in input_sections.items()
        ]
