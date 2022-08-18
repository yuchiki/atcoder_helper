"""TaskConfigを取得する."""
import os
import shutil
from typing import Final
from typing import Optional
from typing import Protocol

import yaml

from atcoder_helper.models.task_config import TaskConfig
from atcoder_helper.repositories.errors import CopyError
from atcoder_helper.repositories.errors import DirectoryNotEmpty
from atcoder_helper.repositories.errors import ParseError
from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.errors import WriteError


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

    def write(
        self, task_config: TaskConfig, template_dir: Optional[str] = None
    ) -> None:
        """TaskConfigを書き込む.

        Args:
            task_config (TaskConfig):
            template_dir (Optional[str]): Defaults to None

        Raises:
            DirectoryNotEmpty: ディレクトリが空でない
            WriteError: タスク設定ファイルの書き込みに失敗
            CopyError: テンプレートのコピーに失敗
        """


def get_default_task_config_repository(
    dir: Optional[str] = None,
) -> TaskConfigRepository:
    """TaskConfigRepositoryの標準実装."""
    if dir is None:
        return TaskConfigRepositoryImpl()
    else:
        return TaskConfigRepositoryImpl(
            os.path.join(dir, TaskConfigRepositoryImpl.default_filename)
        )


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

    def write(
        self, task_config: TaskConfig, template_dir: Optional[str] = None
    ) -> None:
        """TaskConfigを書き込む.

        Args:
            task_config (TaskConfig):
            template_dir (Optional[str]): Defaults to None

        Raises:
            DirectoryNotEmpty: ディレクトリが空でない
            WriteError: タスク設定ファイルの書き込みに失敗
            CopyError: テンプレートのコピーに失敗
        """
        task_dir = os.path.dirname(self._filename)

        def _is_empty(dir: str) -> bool:
            return len(os.listdir(dir)) == 0

        os.makedirs(task_dir, exist_ok=True)
        if not _is_empty(task_dir):
            raise DirectoryNotEmpty(f"directory {task_dir} is not empty")

        if template_dir is not None:
            try:
                for filename in os.listdir(template_dir):
                    shutil.copy(
                        os.path.join(template_dir, filename),
                        task_dir,
                    )
            except OSError as e:
                raise CopyError("テンプレートディレクトリのコピー中にエラーが発生しました") from e

        try:
            with open(
                os.path.join(task_dir, TaskConfigRepositoryImpl.default_filename), "wt"
            ) as file:
                yaml.dump(
                    task_config.dict(exclude_none=True),
                    file,
                    sort_keys=False,
                )
        except OSError as e:
            raise WriteError("タスク設定ファイルの初期化中にエラーが発生しました") from e
