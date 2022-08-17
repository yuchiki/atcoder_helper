"""TaskConfigを取得する."""
from typing import Final
from typing import Protocol

import yaml

from atcoder_helper.models.task_config import TaskConfig
from atcoder_helper.repositories.errors import ParseError
from atcoder_helper.repositories.errors import ReadError


class TaskConfigRepository(Protocol):
    """TaskConfigを取得するプロトコル.

    TaskConfig用ファイルは、Taskディレクトリにおかれていることを想定している.
    """

    def read(self) -> TaskConfig:
        """読み込みを行う.

        Returns:
            TaskConfig: 読み込んだTaskConfig

        Raises:
            ReadError: 読み込みに失敗した
        """


def get_default_task_config_repository() -> TaskConfigRepository:
    """TaskConfigRepositoryの標準実装."""
    return TaskConfigRepositoryImpl()


class TaskConfigRepositoryImpl:
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
            ReadError: 読み込みに失敗した
        """
        try:
            with open(self._filename) as file:
                try:
                    object = yaml.safe_load(file)
                except Exception as e:
                    raise ParseError(f"{file} is not a valid yaml file") from e
        except OSError as e:
            raise ReadError(f"cannot read from {file}") from e

        try:
            return TaskConfig.parse_obj(object)
        except Exception as e:
            raise ParseError(f"{self._filename} can not read as TaskConfig") from e
