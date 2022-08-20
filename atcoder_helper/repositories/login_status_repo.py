"""loginしているかどうかを取得するrepository."""

import requests

from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.utils import AtCoderURLProvider


class LoginStatusRepo:
    """login情報を取得するrepository."""

    _url_provider = AtCoderURLProvider
    _session: requests.Session

    def __init__(self, session: requests.Session):
        """__init__.

        Args:
            session (requests.Session): セッション情報
        """
        self._sesion = session

    def is_logged_in(self) -> bool:
        """loginしているかどうかを判定する.

        Raises:
            ReadError: タスクGETに失敗

        Returns:
            bool: loginしているか否か
        """
        # たたもさんの atcoder-cli を参考にしている
        #  https://github.com/Tatamo/atcoder-cli/blob/0ca0d088f28783a4804ad90d89fc56eb7ddd6ef4/src/atcoder.ts#L46

        try:
            res = self._session.get(
                self._url_provider.submit_url("abc001"),
                allow_redirects=False,
            )
        except Exception as e:
            raise ReadError(
                f"cannot GET {self._url_provider.submit_url('abc001')}"
            ) from e

        return res.status_code == 200  # login していなければ302 redirect になる
