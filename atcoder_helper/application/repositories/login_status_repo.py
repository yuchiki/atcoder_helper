"""loginしているかどうかを取得するrepository."""

from typing import Protocol

import requests


class LoginStatusRepo(Protocol):
    """login情報を取得するrepositoryのプロトコル."""

    def is_logged_in(self, session: requests.Session) -> bool:
        """loginしているかどうかを判定する.

        Raises:
            ReadError: タスクGETに失敗

        Returns:
            bool: loginしているか否か
        """
