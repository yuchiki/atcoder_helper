"""TaskConfigを取得する."""
from typing import Optional
from typing import Protocol

from atcoder_helper.entities.atcoder_task_config import TaskConfig


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
            ParseError: パースに失敗した
        """

    def write(
        self,
        task_config: TaskConfig,
        template_dir: Optional[str] = None,
        target_dir: Optional[str] = None,
    ) -> None:
        """TaskConfigを書き込む.

        Args:
            task_config (TaskConfig):
            template_dir (Optional[str]): Defaults to None
            target_dir (Optional[str]): Defaults to None (current directory)


        Raises:
            DirectoryNotEmpty: ディレクトリが空でない
            WriteError: タスク設定ファイルの書き込みに失敗
            CopyError: テンプレートのコピーに失敗
        """
