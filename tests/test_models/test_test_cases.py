"""test for models.test_case."""

from typing import cast

from atcoder_helper.models.test_case import AtcoderTestCase


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
