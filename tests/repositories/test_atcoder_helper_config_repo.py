"""Tests for atcoder_helper_config_repository."""


from atcoder_helper.repositories.atcoder_helper_config_repo import ConfigRepositoryImpl


def _get_sut() -> ConfigRepositoryImpl:
    return ConfigRepositoryImpl("dummy_config.yaml")
