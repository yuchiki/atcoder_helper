"""atcoderからlogin済みのセッションを取得するrepository."""


import requests
from bs4 import BeautifulSoup

from atcoder_helper.adapter.infrastructure.utils import AtCoderURLProvider
from atcoder_helper.application.repositories.errors import ConnectionError
from atcoder_helper.application.repositories.errors import LoginFailure
from atcoder_helper.application.repositories.errors import ParseError


class AtCoderLoggedInSessionRepositoryImpl:
    """atcoder からlogin済みのセッションを取得するrepository."""

    _url_provider = AtCoderURLProvider

    def _get_csrf_token(self, session: requests.Session) -> str:
        """_.

        Args:
            session (requests.Session): _description_

        Raises:
            ConnectionError: _description_
            ParseError: _description_

        Returns:
            str: _description_
        """
        try:
            login_page = session.get(self._url_provider.login_url)
        except Exception as e:
            raise ConnectionError("fail to get url") from e

        try:
            html = BeautifulSoup(login_page.text, "html.parser")
            token = html.find("input").attrs["value"]
            if not isinstance(token, str):
                raise ParseError("input value is not a string")
        except Exception as e:
            raise ParseError("input value cannot be parsed") from e

        return token

    def read(self, username: str, password: str) -> requests.Session:
        """atcoderにloginしたsessionを返す.入力したユーザーネームとパスワードは保存されず、代わりにセッションが保存される.

        Args:
            username (str): username
            password (str): password

        Raises:
            ConnectionError: GETかPOSTに失敗
            ParseError: パースに失敗
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
