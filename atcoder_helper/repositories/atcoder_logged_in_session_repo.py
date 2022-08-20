"""atcoderからlogin済みのセッションを取得するrepository."""


from typing import cast

import requests
from bs4 import BeautifulSoup

from atcoder_helper.repositories.errors import LoginFailure
from atcoder_helper.repositories.utils import AtCoderURLProvider


class AtCoderLoggedInSessionRepository:
    """atcoder からlogin済みのセッションを取得するrepository."""

    _url_provider = AtCoderURLProvider

    def _get_csrf_token(self, session: requests.Session) -> str:
        login_page = session.get(self._url_provider.login_url)
        html = BeautifulSoup(login_page.text, "html.parser")

        token = html.find("input").attrs["value"]
        return cast(str, token)  # TODO(ちゃんと例外処理をする)

    def read(self, username: str, password: str) -> requests.Session:
        """atcoderにloginする.入力したユーザーネームとパスワードは保存されず、代わりにセッションが保存される.

        Args:
            username (str): username
            password (str): password

        Raises:
            AlreadyLoggedIn: 既にログインしていた
            ConnectionError: POSTに失敗
            LoginFailure: ログイン失敗

        Returns:
            requests.Session: セッションを返す.
        """
        session = requests.Session()
        csrf_token = self._get_csrf_token(session)

        try:
            res = session.post(
                self._url_provider.login_url,
                params={
                    "username": username,
                    "password": password,
                    "csrf_token": csrf_token,
                },
                allow_redirects=False,
            )
        except Exception as e:
            raise ConnectionError(
                f"cannot post to {self._url_provider.login_url}"
            ) from e

        if res.headers["Location"] == "/home":
            return session
        else:
            raise LoginFailure("ログインに失敗しました.")
