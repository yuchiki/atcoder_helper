"""configを初期化するためのservice."""


import os

import atcoder_helper
from atcoder_helper.repositories.atcoder_helper_config_repo import (
    AtCoderHelperConfigRepository,
)
from atcoder_helper.services.util import get_atcoder_helper_config_filepath


def init_config() -> None:
    """configを初期化するためのservice."""
    default_config_filepath = os.path.join(
        atcoder_helper.__path__[0], "default_settings", "default_config.yaml"
    )
    default_config_repo = AtCoderHelperConfigRepository(default_config_filepath)
    default_atcoder_config = default_config_repo.read()

    config_repo = AtCoderHelperConfigRepository(get_atcoder_helper_config_filepath())
    config_repo.write(default_atcoder_config)
