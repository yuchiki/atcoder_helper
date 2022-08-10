"""TaskConfigを取得する."""
import yaml

from atcoder_helper.models.task_config import TaskConfig


class TaskConfigRepository:
    """TaskConfigを取得する.

    TaskConfig用ファイルは、Taskディレクトリにおかれていることを想定している.
    """

    _filename: str

    def __init__(self, filename: str):
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
