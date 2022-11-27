"""認証周りのサービス."""


from typing import Protocol


class AuthUsecase(Protocol):
    """auth を扱うサービスのプロトコル."""

    def login(self, username: str, password: str) -> None:
        """ログインする.

        Args:
            username (str): username
            password (str): password

        Raises:
            ConfigAccessError: 設定ファイルのエラー
            AtcoderAccessError: atcoderから情報を取得する際のエラー
            AlreadyLoggedIn: 既にログインしている # 今は返さないけど今後かなりの高確率で返しうるので書いておく
        """

    def logout(self) -> None:
        """logout.

        Raises:
            ConfigAccessError: 設定ファイル読み書きのエラー
        """

    def status(self) -> bool:
        """loginしているかどうかを返す.

        Returns:
            bool: loginしているか

        Raises:
            AtcoderAccessError: atcoder access error
        """
