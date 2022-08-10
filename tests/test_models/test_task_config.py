"""Tests for models.TaskConfig."""

from atcoder_helper.models.task_config import TaskConfig


def test_atcoder_test_case_from_dict() -> None:
    """Test for TaskConfig.from_dict()."""
    input_dict = {"build": ["foo", "bar", "baz"], "run": ["qux", "quux"]}
    expected = TaskConfig(build=["foo", "bar", "baz"], run=["qux", "quux"])
    actual = TaskConfig.from_dict(input_dict)
    assert actual == expected