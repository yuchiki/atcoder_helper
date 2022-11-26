"""Taskディレクトリを初期化するためのusecase."""
from typing import Optional
from typing import Protocol

from injector import inject

import atcoder_helper.infrastructure.errors as repo_errors
from atcoder_helper.application.usecases.errors import ConfigAccessError
from atcoder_helper.entities.atcoder_task_config import TaskConfig
from atcoder_helper.infrastructure.atcoder_helper_config_repo import ConfigRepository
from atcoder_helper.infrastructure.errors import ParseError
from atcoder_helper.infrastructure.errors import ReadError
from atcoder_helper.infrastructure.task_config_repo import TaskConfigRepository


class InitTaskDirUsecase(Protocol):
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


class InitTaskDirInteractor:
    """TaskDirectoryを初期化するサービス."""

    _atcoder_helper_config_repo: ConfigRepository
    _task_config_repo: TaskConfigRepository

    @inject
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
