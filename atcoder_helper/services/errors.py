"""service層のエラーたち."""


class AlreadyLoggedIn(Exception):
    """既にログインしている."""


class ConfigAccessError(Exception):
    """設定ファイル読み書きの起因のエラー."""


class AtcoderAccessError(Exception):
    """atcoderページとの通信起因のエラー."""


class UndefinedLanguage(Exception):
    """未定義の言語."""


class DirectoryNotEmpty(Exception):
    """Directoryが空でないエラー."""
