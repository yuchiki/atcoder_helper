"""デフォルト言語を取得する."""


from atcoder_helper.models.atcoder_helper_config import LanguageConfig
from atcoder_helper.repositories.atcoder_helper_config_repo import (
    AtCoderHelperConfigRepository,
)
from atcoder_helper.services.util import get_atcoder_helper_config_filepath


def config_default_language() -> LanguageConfig:
    """デフォルト言語を取得する.

    Returns:
        LanguageConfig: デフォルト言語
    """
    config_repo = AtCoderHelperConfigRepository(get_atcoder_helper_config_filepath())
    config = config_repo.read()
    return config.languages[config.default_language]
