"""Taskディレクトリを初期化するためのservice."""
import os
import shutil
from typing import Optional
from typing import Protocol

import yaml

from atcoder_helper.models.atcoder_helper_config import LanguageConfig
from atcoder_helper.models.task_config import TaskConfig
from atcoder_helper.repositories.atcoder_helper_config_repo import ConfigRepository
from atcoder_helper.repositories.atcoder_helper_config_repo import (
    get_default_config_repository,
)
from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.task_config_repo import TaskConfigRepositoryImpl
from atcoder_helper.repositories.utils import filter_out_none
from atcoder_helper.services.errors import ConfigAccessError
from atcoder_helper.services.errors import DirectoryNotEmpty


class InitTaskDirService(Protocol):
    """TaskDirectoryを初期化するサービスのプロトコル."""

    def init_task(
        self,
        dir: Optional[str] = None,
        contest: Optional[str] = None,
        task: Optional[str] = None,
    ) -> None:
        """taskディレクトリを初期化します.

        Raises:
            DirectoryNotEmpty: 作成しようとしているディレクトリが空でない
            ConfigAccessError: 設定ファイルの読み書きに失敗
        """


def get_default_init_task_dir_service() -> InitTaskDirService:
    """InitTaskDirServiceの標準実装を返す.

    Returns:
        InitTaskDirService: _description_
    """
    return InitTaskDirServiceImpl()


class InitTaskDirServiceImpl:
    """TaskDirectoryを初期化するサービス."""

    _atcoder_helper_config_repo: ConfigRepository

    def __init__(
        self,
        atcoder_helper_config_repo: ConfigRepository = get_default_config_repository(),
    ):
        """__init.

        Args:
            atcoder_helper_config_repo (ConfigRepository, optional): Defaults to
                get_default_config_repository().
        """
        self._atcoder_helper_config_repo = atcoder_helper_config_repo

    def init_task(
        self,
        dir: Optional[str] = None,
        contest: Optional[str] = None,
        task: Optional[str] = None,
    ) -> None:
        """taskディレクトリを初期化します.

        Raises:
            DirectoryNotEmpty: 作成しようとしているディレクトリが空でない
            ConfigAccessError: 設定ファイルの読み書きに失敗
        """
        try:
            config = self._atcoder_helper_config_repo.read()
        except ReadError as e:
            raise ConfigAccessError("全体設定ファイルの読み込みに失敗しました") from e

        if dir is None:
            dir = os.getcwd()

        self._init_task(dir, config.default_language_config, contest, task)

    # TODO(ここにあるのはおかしい気がする。repoに移動するべきか？)
    def _init_task(
        self,
        task_dir: str,
        languageConfig: LanguageConfig,
        contest: Optional[str],
        task: Optional[str],
    ) -> None:
        """_init_task.

        Args:
            task_dir (str):
            languageConfig (LanguageConfig):
            contest (Optional[str]):
            task (Optional[str]):

        Raises:
            DirectoryNotEmpty:
            ConfigAccessError:
        """

        def _is_empty(dir: str) -> bool:
            return len(os.listdir(dir)) == 0

        os.makedirs(task_dir, exist_ok=True)
        if not _is_empty(task_dir):
            raise DirectoryNotEmpty(f"directory {task_dir} is not empty")

        if languageConfig.resolved_template_dir is not None:
            try:
                for filename in os.listdir(languageConfig.resolved_template_dir):
                    shutil.copy(
                        os.path.join(languageConfig.resolved_template_dir, filename),
                        task_dir,
                    )
            except OSError as e:
                raise ConfigAccessError("テンプレートディレクトリのコピー中にエラーが発生しました") from e

        task_config = TaskConfig(
            build=languageConfig.build,
            run=languageConfig.run,
            contest=contest,
            task=task,
        )

        try:
            with open(
                os.path.join(task_dir, TaskConfigRepositoryImpl.default_filename), "wt"
            ) as file:
                yaml.dump(
                    filter_out_none(task_config.dict()),
                    file,
                    sort_keys=False,
                )
        except OSError as e:
            raise ConfigAccessError("タスク設定ファイルの初期化中にエラーが発生しました") from e
