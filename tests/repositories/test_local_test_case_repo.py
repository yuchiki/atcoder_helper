"""local_test_case_repoのテスト."""

from typing import Type

import mock
import pytest
import yaml
from mock import ANY
from pytest import MonkeyPatch

from atcoder_helper.models.atcoder_test_case import AtcoderTestCase
from atcoder_helper.repositories.errors import ParseError
from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.errors import WriteError
from atcoder_helper.repositories.local_test_case_repo import LocalTestCaseRepositoryImpl

testcases = [AtcoderTestCase(name="foo_case", given="given")]


test_write_parameters = {
    "OK": [mock.MagicMock(), None],
    "Error(書き込み失敗)": [mock.MagicMock(side_effect=OSError()), WriteError],
}


@pytest.mark.parametrize(
    argnames=("dump_mock", "exception"),
    argvalues=test_write_parameters.values(),
    ids=test_write_parameters.keys(),
)
def test_write(
    dump_mock: mock.MagicMock, exception: Type[Exception], monkeypatch: MonkeyPatch
) -> None:
    """writeのテスト."""
    filename = "foo_file"

    open_mock = mock.MagicMock()
    monkeypatch.setattr(yaml, "dump", dump_mock)
    monkeypatch.setattr("builtins.open", open_mock)

    sut = LocalTestCaseRepositoryImpl(filename)

    if exception:
        with pytest.raises(exception):
            sut.write(testcases)
    else:
        sut.write(testcases)

    open_mock.assert_called_once_with(filename, "wt")
    dump_mock.assert_called_once_with([testcases[0].dict()], ANY, sort_keys=False)


test_read_parameters = {
    "OK": [mock.MagicMock(return_value=[testcases[0]]), None],
    "Error(読み込み失敗)": [mock.MagicMock(side_effect=OSError()), ReadError],
    "Error(Parse失敗)": [mock.MagicMock(return_value=["foo"]), ParseError],
}


@pytest.mark.parametrize(
    argnames=("safe_load_mock", "exception"),
    argvalues=test_read_parameters.values(),
    ids=test_read_parameters.keys(),
)
def test_read(
    safe_load_mock: mock.MagicMock, exception: Type[Exception], monkeypatch: MonkeyPatch
) -> None:
    """readのテスト."""
    filename = "foo_file"
    open_mock = mock.MagicMock()
    monkeypatch.setattr("builtins.open", open_mock)
    monkeypatch.setattr(yaml, "safe_load", safe_load_mock)

    sut = LocalTestCaseRepositoryImpl(filename)

    if exception:
        with pytest.raises(exception):
            sut.read()
    else:
        result = sut.read()
        assert result == testcases
