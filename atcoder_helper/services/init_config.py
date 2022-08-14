"""configを初期化するためのservice."""


import os

import atcoder_helper
from atcoder_helper.repositories import errors as repository_error
from atcoder_helper.repositories.atcoder_helper_config_repo import ConfigRepository
from atcoder_helper.repositories.atcoder_helper_config_repo import ConfigRepositoryImpl
from atcoder_helper.services.errors import ConfigAccessError
from atcoder_helper.services.util import get_atcoder_helper_config_filepath


def init_config(
    default_config_repo: ConfigRepository = ConfigRepositoryImpl(
        os.path.join(
            atcoder_helper.__path__[0], "default_settings", "default_config.yaml"
        )
    ),
    config_repo: ConfigRepository = ConfigRepositoryImpl(
        get_atcoder_helper_config_filepath()
    ),
) -> None:
    """configを初期化するためのservice.

    Raises:
        ConfigAccessError:
    """
    try:
        default_atcoder_config = default_config_repo.read()
    except repository_error.ReadError as e:
        raise ConfigAccessError("デフォルト設定ファイルの読み込みに失敗しました.") from e

    try:
        config_repo.write(default_atcoder_config)
    except repository_error.WriteError as e:
        raise ConfigAccessError("設定ファイルの書き込みに失敗しました.") from e
