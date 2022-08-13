"""使用可能な言語の一覧を取得する."""


from typing import Dict

from atcoder_helper.models.atcoder_helper_config import LanguageConfig
from atcoder_helper.repositories.atcoder_helper_config_repo import (
    AtCoderHelperConfigRepository,
)
from atcoder_helper.services.util import get_atcoder_helper_config_filepath


def config_languages() -> Dict[str, LanguageConfig]:
    """使用可能な言語の一覧を取得する.

    Returns:
        Dict[str, LanguageConfig]: 言語名から言語設定をひく辞書
    """
    config_repo = AtCoderHelperConfigRepository(get_atcoder_helper_config_filepath())
    config = config_repo.read()
    return config.languages
