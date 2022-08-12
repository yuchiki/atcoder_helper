"""Taskディレクトリを初期化するためのservice."""


import os
import shutil
from typing import List
from typing import Optional

import yaml


class DirectoryNotEmpty(Exception):
    """Directoryが空でないエラー."""

    pass


def _is_empty(dir: str) -> bool:
    return len(os.listdir(dir)) == 0


def _init_task(build: List[str], run: List[str], template_dir: Optional[str]) -> None:
    current_dir = os.getcwd()

    if not _is_empty(current_dir):
        raise DirectoryNotEmpty(f"directory {current_dir} is not empty")

    if template_dir is not None:
        shutil.copytree(template_dir, current_dir)

    task_config_dict = {"build": build, "run": run}

    with open(
        os.path.join(current_dir, ".atcoder_helper_task_config.yaml"), "w"
    ) as file:
        yaml.dump(task_config_dict, file, sort_keys=False)
