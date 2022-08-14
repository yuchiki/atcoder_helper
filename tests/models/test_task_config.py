"""Tests for models.TaskConfig."""

from atcoder_helper.models.task_config import TaskConfig
from atcoder_helper.models.task_config import TaskConfigDict


def test_atcoder_test_case_from_dict() -> None:
    """Test for TaskConfig.from_dict()."""
    input_dict: TaskConfigDict = {
        "contest": "A",
        "task": "B",
        "build": ["foo", "bar", "baz"],
        "run": ["qux", "quux"],
    }
    expected = TaskConfig(
        contest="A", task="B", build=["foo", "bar", "baz"], run=["qux", "quux"]
    )
    actual = TaskConfig.from_dict(input_dict)
    assert actual == expected
