"""使用可能な言語の一覧を取得する."""


from typing import Dict

from atcoder_helper.models.atcoder_helper_config import LanguageConfig
from atcoder_helper.repositories import errors as repository_errors
from atcoder_helper.repositories.atcoder_helper_config_repo import ConfigRepository
from atcoder_helper.repositories.atcoder_helper_config_repo import ConfigRepositoryImpl
from atcoder_helper.services.errors import ConfigAccessError
from atcoder_helper.services.util import get_atcoder_helper_config_filepath


def config_languages(
    config_repo: ConfigRepository = ConfigRepositoryImpl(
        get_atcoder_helper_config_filepath()
    ),
) -> Dict[str, LanguageConfig]:
    """使用可能な言語の一覧を取得する.

    Raises:
        ConfigAccessError: 設定ファイルの読み書きの失敗

    Returns:
        Dict[str, LanguageConfig]: 言語名から言語設定をひく辞書
    """
    try:
        config = config_repo.read()
    except repository_errors.ReadError as e:
        raise ConfigAccessError("設定ファイルの読み込みに失敗しました") from e

    return config.languages
