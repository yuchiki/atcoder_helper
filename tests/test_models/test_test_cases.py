"""test for models.test_case."""

from typing import cast

import pytest

from atcoder_helper.models.test_case import AtcoderTestCase


def test_atcoder_test_case_to_dict() -> None:
    """AtcdoderTestCase.to_dict() works."""
    test_cases = [
        {
            "name": "with expected",
            "self": AtcoderTestCase("foo", "bar\n", "baz\n"),
            "expected": {"name": "foo", "input": "bar\n", "expected": "baz\n"},
        },
        {
            "name": "without expected",
            "self": AtcoderTestCase("foo", "bar\n", None),
            "expected": {
                "name": "foo",
                "input": "bar\n",
            },
        },
    ]

    for case in test_cases:
        print(case["name"])
        actual = cast(AtcoderTestCase, case["self"]).to_dict()
        assert actual == case["expected"]


def test_atcoder_test_case_from_dict() -> None:
    """Test for AtcoderTestCase.from_dict()."""
    test_cases = [
        {
            "name": "with expected",
            "input": {"name": "foo", "input": "bar", "expected": "baz"},
            "expected": AtcoderTestCase("foo", "bar\n", "baz\n"),
        },
        {
            "name": "without expected",
            "input": {"name": "foo", "input": "bar"},
            "expected": AtcoderTestCase("foo", "bar\n", None),
        },
    ]

    for case in test_cases:
        print(case["name"])
        actual = AtcoderTestCase.from_dict(cast(dict[str, str], case["input"]))
        assert actual == case["expected"]


@pytest.mark.skip(reason="難しいので後でテストを書く")
def test_atcoder_test_case_execute() -> None:
    """Test for AtcoderTestCase.execute() works."""
    pass
