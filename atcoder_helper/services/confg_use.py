"""デフォルト言語を変更する."""


from atcoder_helper.repositories import errors as repository_error
from atcoder_helper.repositories.atcoder_helper_config_repo import ConfigRepository
from atcoder_helper.repositories.atcoder_helper_config_repo import (
    get_default_config_repository,
)
from atcoder_helper.services.errors import ConfigAccessError
from atcoder_helper.services.errors import UndefinedLanguage


def config_use(
    language: str, config_repo: ConfigRepository = get_default_config_repository()
) -> None:
    """デフォルト言語を変更する.

    Raises:
        UndefinedLanguage: 存在しない言語をデフォルトに設定しようとした
        ConfigAccessError: 通信層のエラー
    """
    try:
        config = config_repo.read()
        if language not in config.languages:
            raise UndefinedLanguage(f"言語{language}は設定の中に存在しません。")

        config.default_language = language
        config_repo.write(config)
    except (repository_error.WriteError, repository_error.ReadError):
        raise ConfigAccessError("設定ファイルの読み書きに失敗しました。")
