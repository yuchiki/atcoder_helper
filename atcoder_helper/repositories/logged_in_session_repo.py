"""SessionRepo."""

import os
import pickle

import requests

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
