"""Taskディレクトリを初期化するためのservice."""
import os
import shutil
from typing import Any
from typing import Optional

import yaml

from atcoder_helper.models.atcoder_helper_config import LanguageConfig
from atcoder_helper.repositories.atcoder_helper_config_repo import (
    AtCoderHelperConfigRepository,
)
from atcoder_helper.services.util import get_atcoder_helper_config_filepath


class DirectoryNotEmpty(Exception):
    """Directoryが空でないエラー."""

    pass


def _is_empty(dir: str) -> bool:
    return len(os.listdir(dir)) == 0


def _init_task(
    task_dir: str,
    languageConfig: LanguageConfig,
    contest: Optional[str],
    task: Optional[str],
) -> None:
    os.makedirs(task_dir, exist_ok=True)
    if not _is_empty(task_dir):
        raise DirectoryNotEmpty(f"directory {task_dir} is not empty")

    if languageConfig.resolved_template_dir is not None:
        for filename in os.listdir(languageConfig.resolved_template_dir):
            shutil.copy(
                os.path.join(languageConfig.resolved_template_dir, filename), task_dir
            )

    task_config_dict: dict[str, Any] = {
        "build": languageConfig.build,
        "run": languageConfig.run,
    }

    if contest is not None:
        task_config_dict["contest"] = contest

    if task is not None:
        task_config_dict["task"] = task

    with open(os.path.join(task_dir, ".atcoder_helper_task_config.yaml"), "w") as file:
        yaml.dump(task_config_dict, file, sort_keys=False)


def init_task(dir: Optional[str], contest: Optional[str], task: Optional[str]) -> None:
    """taskディレクトリを初期化します."""
    config_repo = AtCoderHelperConfigRepository(get_atcoder_helper_config_filepath())
    config = config_repo.read()

    if dir is None:
        dir = os.getcwd()

    _init_task(dir, config.default_language_config, contest, task)
