"""TaskConfigを定義する."""

from typing import List
from typing import Optional

from pydantic import BaseModel


class TaskConfig(BaseModel):
    """タスクごとの設定を保持する."""

    build: List[str]
    run: List[str]
    contest: Optional[str] = None
    task: Optional[str] = None
