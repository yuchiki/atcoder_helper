"""認証周りのサービス."""


from atcoder_helper.repositories.atcoder_repo import AtCoderRepository


class AlreadyLoggedIn(Exception):
    """既にログインしている."""

    pass


def login(username: str, password: str) -> bool:
    """ログインする.

    Args:
        username (str): username
        password (str): password

    Raises:
        AlreadyLoggedIn: 既にログインしている

    Returns:
        bool: ログインに成功できたかどうか
    """
    atcoder_repo = AtCoderRepository()

    if atcoder_repo.is_logged_in():
        raise Exception("ログイン失敗")

    return atcoder_repo.login(username, password)


def logout() -> None:
    """logout."""
    atcoder_repo = AtCoderRepository()

    atcoder_repo.logout()


def status() -> bool:
    """loginしているかどうかを返す.

    Returns:
        bool: loginしているか
    """
    atcoder_repo = AtCoderRepository()
    return atcoder_repo.is_logged_in()
