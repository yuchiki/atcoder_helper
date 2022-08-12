"""TaskConfigを定義する."""

from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class TaskConfig:
    """タスクごとの設定を保持する."""

    contest: Optional[str]
    task: Optional[str]
    build: List[str]
    run: List[str]

    @classmethod
    def from_dict(cls, task_config_dict: Dict[str, Any]) -> "TaskConfig":
        """辞書からTaskConfig型に変換する."""
        return TaskConfig(
            contest=task_config_dict["contest"]
            if "contest" in task_config_dict
            else None,
            task=task_config_dict["task"] if "task" in task_config_dict else None,
            build=task_config_dict["build"],
            run=task_config_dict["run"],
        )
