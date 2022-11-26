"""Taskディレクトリを初期化するためのusecase."""
from typing import Optional
from typing import Protocol


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
