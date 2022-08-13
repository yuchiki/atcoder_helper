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
        raise AlreadyLoggedIn("既にログインしています")

    return atcoder_repo.login(username, password)
