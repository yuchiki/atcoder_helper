"""デフォルト言語を変更する."""


from atcoder_helper.repositories.atcoder_helper_config_repo import (
    AtCoderHelperConfigRepository,
)
from atcoder_helper.services.util import get_atcoder_helper_config_filepath


def config_use(language: str) -> None:
    """デフォルト言語を変更する."""
    config_repo = AtCoderHelperConfigRepository(get_atcoder_helper_config_filepath())
    config = config_repo.read()
    if language not in config.languages:
        raise Exception(f"言語{language}は設定の中に存在しません。")

    config.default_language = language
    config_repo.write(config)
