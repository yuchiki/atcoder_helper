"""Taskディレクトリを初期化するためのservice."""
from typing import Optional
from typing import Protocol

import atcoder_helper.repositories.errors as repo_errors
from atcoder_helper.models.atcoder_task_config import TaskConfig
from atcoder_helper.repositories.atcoder_helper_config_repo import ConfigRepository
from atcoder_helper.repositories.atcoder_helper_config_repo import (
    get_default_config_repository,
)
from atcoder_helper.repositories.errors import ParseError
from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.task_config_repo import TaskConfigRepository
from atcoder_helper.repositories.task_config_repo import (
    get_default_task_config_repository,
)
from atcoder_helper.services.errors import ConfigAccessError


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
    return InitTaskDirServiceImpl(
        atcoder_helper_config_repo=get_default_config_repository(),
        task_config_repo=get_default_task_config_repository(),
    )


class InitTaskDirServiceImpl:
    """TaskDirectoryを初期化するサービス."""

    _atcoder_helper_config_repo: ConfigRepository
    _task_config_repo: TaskConfigRepository

    def __init__(
        self,
        atcoder_helper_config_repo: ConfigRepository,
        task_config_repo: TaskConfigRepository,
    ):
        """__init.

        Args:
            atcoder_helper_config_repo (ConfigRepository): _
            task_config_repo (TaskConfigRepository): _
        """
        self._atcoder_helper_config_repo = atcoder_helper_config_repo
        self._task_config_repo = task_config_repo

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
            language_config = (
                self._atcoder_helper_config_repo.read().default_language_config
            )
        except (ReadError, ParseError) as e:
            raise ConfigAccessError("全体設定ファイルの読み込みに失敗しました") from e

        task_config = TaskConfig(
            build=language_config.build,
            run=language_config.run,
            contest=contest,
            task=task,
        )

        try:
            self._task_config_repo.write(
                task_config=task_config,
                template_dir=language_config.resolved_template_dir,
                target_dir=dir,
            )
        except repo_errors.DirectoryNotEmpty as e:
            raise ConfigAccessError("ディレクトリを初期化できません") from e
        except repo_errors.WriteError as e:
            raise ConfigAccessError("タスク設定ファイルの書き込みに失敗しました") from e
        except repo_errors.CopyError as e:
            raise ConfigAccessError("テンプレートによる初期化に失敗しました") from e
