"""repositories.errorsの定義."""


class ReadError(Exception):
    """読み込めなかったエラー."""


class WriteError(Exception):
    """書き込めなかったエラー."""


class ParseError(Exception):
    """パースに失敗したエラー."""


class AlreadyLoggedIn(Exception):
    """既にログインしているエラー."""


class DirectoryNotEmpty(Exception):
    """Directoryが空でないエラー."""


class CopyError(Exception):
    """Copy時のエラー."""


class LoginFailure(Exception):
    """loginに失敗した."""


class ConnectionError(Exception):
    """通信に失敗した."""
