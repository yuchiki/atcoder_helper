"""デフォルト言語を取得する."""


from atcoder_helper.models.atcoder_helper_config import LanguageConfig
from atcoder_helper.repositories import errors as repository_errors
from atcoder_helper.repositories.atcoder_helper_config_repo import (
    AtCoderHelperConfigRepository,
)
from atcoder_helper.services.errors import ConfigAccessError
from atcoder_helper.services.util import get_atcoder_helper_config_filepath


def config_default_language() -> LanguageConfig:
    """デフォルト言語を取得する.

    Raises:
        ConfigAccerssError: 設定ファイル読み書きのエラー

    Returns:
        LanguageConfig: デフォルト言語
    """
    config_repo = AtCoderHelperConfigRepository(get_atcoder_helper_config_filepath())

    try:
        config = config_repo.read()
    except repository_errors.ReadError as e:
        raise ConfigAccessError("設定ファイルの読み込みに失敗しました") from e

    return config.languages[config.default_language]
