"""Taskディレクトリを初期化するためのservice."""
import os
import shutil

import yaml

from atcoder_helper.models.atcoder_helper_config import LanguageConfig
from atcoder_helper.repositories.atcoder_helper_config_repo import (
    AtCoderHelperConfigRepository,
)


class DirectoryNotEmpty(Exception):
    """Directoryが空でないエラー."""

    pass


def _is_empty(dir: str) -> bool:
    return len(os.listdir(dir)) == 0


def _init_task(task_dir: str, languageConfig: LanguageConfig) -> None:
    if not _is_empty(task_dir):
        raise DirectoryNotEmpty(f"directory {task_dir} is not empty")

    if languageConfig.resolved_template_dir is not None:
        for filename in os.listdir(languageConfig.resolved_template_dir):
            shutil.copy(
                os.path.join(languageConfig.resolved_template_dir, filename), task_dir
            )

    task_config_dict = {"build": languageConfig.build, "run": languageConfig.run}

    with open(os.path.join(task_dir, ".atcoder_helper_task_config.yaml"), "w") as file:
        yaml.dump(task_config_dict, file, sort_keys=False)


def _get_atcoder_helper_config_filepath() -> str:
    filepath = os.environ.get("ATCODER_HELPER_CONFIG_FILEPATH")
    if filepath:
        return filepath
    else:
        return os.path.join(os.path.expanduser("~"), ".atcoder_helper", "config.yaml")


def init_task() -> None:
    """taskディレクトリを初期化します."""
    config_repo = AtCoderHelperConfigRepository(_get_atcoder_helper_config_filepath())
    config = config_repo.read()

    _init_task(os.path.join(os.getcwd()), config.default_language_config)
