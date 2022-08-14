"""認証周りのサービス."""


import atcoder_helper.repositories.errors as repository_error
from atcoder_helper.repositories.atcoder_repo import AtCoderRepository
from atcoder_helper.services.errors import AlreadyLoggedIn
from atcoder_helper.services.errors import AtcoderAccessError
from atcoder_helper.services.errors import ConfigAccessError


def login(username: str, password: str) -> bool:
    """ログインする.

    Args:
        username (str): username
        password (str): password

    Raises:
        AlreadyLoggedIn: 既にログインしている
        ConfigAccessError: 設定ファイルのエラー
        AtcoderAccessError: atcoderから情報を取得する際のエラー
    Returns:
        bool: ログインに成功できたかどうか
    """
    try:
        atcoder_repo = AtCoderRepository()
        status = atcoder_repo.login(username, password)
    except repository_error.AlreadyLoggedIn as e:
        raise AlreadyLoggedIn("既にログインしています") from e
    except (repository_error.ReadError) as e:
        raise ConfigAccessError("設定ファイルの読み込みに失敗しました") from e
    except (repository_error.WriteError) as e:
        raise AtcoderAccessError("通信に失敗しました") from e

    return status


def logout() -> None:
    """logout.

    Raises:
        ConfigAccessError: 設定ファイル読み書きのエラー
    """
    try:
        atcoder_repo = AtCoderRepository()

        atcoder_repo.logout()
    except (repository_error.ReadError, repository_error.WriteError) as e:
        raise ConfigAccessError("設定ファイルの読み書きに失敗しました") from e


def status() -> bool:
    """loginしているかどうかを返す.

    Returns:
        bool: loginしているか

    Raises:
        AtcoderAccessError: atcoder access error
    """
    try:
        atcoder_repo = AtCoderRepository()
        status = atcoder_repo.is_logged_in()
    except repository_error.ReadError as e:
        raise AtcoderAccessError("atcoderのページとの通信に失敗しました") from e

    return status
