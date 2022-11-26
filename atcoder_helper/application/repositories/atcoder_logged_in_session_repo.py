"""atcoderからlogin済みのセッションを取得するrepository."""


from typing import Protocol

import requests


class AtCoderLoggedInSessionRepository(Protocol):
    """atcoder からlogin済みのセッションを取得するrepositoryのプロトコル."""

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
