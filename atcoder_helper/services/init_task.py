"""Taskディレクトリを初期化するためのservice."""


import os
import shutil
from typing import List
from typing import Optional

import yaml

import atcoder_helper


class DirectoryNotEmpty(Exception):
    """Directoryが空でないエラー."""

    pass


def _is_empty(dir: str) -> bool:
    return len(os.listdir(dir)) == 0


def _init_task(
    task_dir: str, build: List[str], run: List[str], template_dir: Optional[str]
) -> None:
    if not _is_empty(task_dir):
        raise DirectoryNotEmpty(f"directory {task_dir} is not empty")

    if template_dir is not None:
        for filename in os.listdir(template_dir):
            shutil.copy(os.path.join(template_dir, filename), task_dir)

    task_config_dict = {"build": build, "run": run}

    with open(os.path.join(task_dir, ".atcoder_helper_task_config.yaml"), "w") as file:
        yaml.dump(task_config_dict, file, sort_keys=False)


def init_task() -> None:
    """taskディレクトリを初期化します."""

    _init_task(
        os.path.join(os.getcwd(), "hoge"),
        ["g++", "main.cpp", "-o", "main"],
        ["./main"],
        os.path.join(
            atcoder_helper.__path__[0],
            "sample_configs",
            ".atcoder_helper",
            "templates",
            "cpp",
        ),
    )
