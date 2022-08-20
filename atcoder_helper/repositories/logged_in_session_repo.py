"""SessionRepo."""

import os
import pickle
from typing import cast

import requests

from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.errors import WriteError


class LoggedInSessionRepository:
    """Login済みセッションの永続化層."""

    _session_filename: str

    def __init__(self, session_filename: str):
        """__init__.

        Args:
            session_filename (str): session filename
        """
        self._session_filename = session_filename

    def write(self, session: requests.Session) -> None:
        """_write.

        Raises:
            WriteError: 書き込みに失敗
        """
        os.makedirs(os.path.dirname(self._session_filename), exist_ok=True)

        try:
            with open(self._session_filename, "wb") as file:
                pickle.dump(session, file)
        except OSError as e:
            raise WriteError(f"cannot write to {self._session_filename}") from e

    def read(self) -> requests.Session:
        """read. ファイルが存在しない場合はデフォルトsessionを返す.

        Raises:
            ReadError: 読み込みに失敗した

        Return:
            requests.Session: 取得したsession
        """
        if self.doesExist():
            try:
                with open(self._session_filename, "rb") as file:
                    return cast(requests.Session, pickle.load(file))
            except OSError as e:
                raise ReadError(f"cannot open or parse {self._session_filename}") from e
        else:
            return requests.session()

    def doesExist(self) -> bool:
        """sessionがすでに存在するかどうか確認する.

        Returns:
            bool: 存在するかどうか
        """
        return os.path.isfile(self._session_filename)

    def delete(self) -> None:
        """session 情報を削除します。"""
        self.write(requests.Session())
