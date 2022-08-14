"""TaskConfigを取得する."""
from typing import Final
from typing import cast

import yaml

from atcoder_helper.models.task_config import TaskConfig
from atcoder_helper.models.task_config import TaskConfigDict
from atcoder_helper.repositories.errors import ReadError


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

        Raises:
            ReadError: データの読み込みに失敗した
        """
        try:
            with open(self._filename) as file:
                object = cast(TaskConfigDict, yaml.safe_load(file))  # TODO(validate)
        except OSError as e:
            raise ReadError(f"cannot read from {file}") from e

        return TaskConfig.from_dict(object)
