"""configを初期化するためのservice."""


from atcoder_helper.models.atcoder_helper_config import default_atcoder_config
from atcoder_helper.repositories.atcoder_helper_config_repo import (
    AtCoderHelperConfigRepository,
)
from atcoder_helper.services.util import get_atcoder_helper_config_filepath


def init_config() -> None:
    """configを初期化するためのservice."""
    config_repo = AtCoderHelperConfigRepository(get_atcoder_helper_config_filepath())
    config_repo.write(default_atcoder_config)
