"""TaskConfigを定義する."""

from dataclasses import dataclass
from typing import Dict
from typing import List


@dataclass
class TaskConfig:
    """タスクごとの設定を保持する."""

    build: List[str]
    run: List[str]

    @classmethod
    def from_dict(cls, task_config_dict: Dict[str, List[str]]) -> "TaskConfig":
        """辞書からTaskConfig型に変換する."""
        return TaskConfig(build=task_config_dict["build"], run=task_config_dict["run"])
