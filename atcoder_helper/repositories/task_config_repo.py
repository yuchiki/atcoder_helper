"""TaskConfigを取得する."""
from typing import Final

import yaml

from atcoder_helper.models.task_config import TaskConfig


class TaskConfigRepository:
    """TaskConfigを取得する.

    TaskConfig用ファイルは、Taskディレクトリにおかれていることを想定している.
    """

    default_filename: Final[str] = ".atcoder_helper_task_config.yaml"
    _filename: str

    def __init__(self, filename: str = default_filename):
        """__init__.

        Args:
            filename (str): TaskConfigがおかれているファイル名
        """
        self._filename = filename

    def read(self) -> TaskConfig:
        """読み込みを行う.

        Returns:
            TaskConfig: 読み込んだTaskConfig
        """
        with open(self._filename) as file:
            object = yaml.safe_load(file)
            return TaskConfig.from_dict(object)
