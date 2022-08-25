"""Tests for atcoder_helper_config_repository."""


import os
from typing import Type

import mock
import pytest
import yaml
from mock import ANY
from pytest import MonkeyPatch

from atcoder_helper.models.atcoder_helper_config import AtCoderHelperConfig
from atcoder_helper.models.atcoder_helper_config import LanguageConfig
from atcoder_helper.repositories.atcoder_helper_config_repo import ConfigRepositoryImpl
from atcoder_helper.repositories.errors import ParseError
from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.errors import WriteError

helper_config = AtCoderHelperConfig(
    languages={"foo": LanguageConfig(name="foo", build=[], run=[])},
    default_language="foo",
)

helper_config_dict = {
    "languages": [{"name": "foo", "build": [], "run": []}],
    "default_language": "foo",
}


test_config_repository_impl_read_parameters = {
    "OK": [mock.MagicMock(return_value=helper_config_dict), None, helper_config],
    "Error(読み込み失敗)": [mock.MagicMock(side_effect=OSError), ReadError, ANY],
    "Error(パース失敗)": [mock.MagicMock(return_value={}), ParseError, ANY],
}


@pytest.mark.parametrize(
    argnames=("safe_load_mock", "exception", "result"),
    argvalues=test_config_repository_impl_read_parameters.values(),
    ids=test_config_repository_impl_read_parameters.keys(),
)
def test_config_repository_impl_read(
    safe_load_mock: mock.MagicMock,
    exception: Type[Exception],
    result: AtCoderHelperConfig,
    monkeypatch: MonkeyPatch,
) -> None:
    """readのテスト."""
    filename = "file_foo"

    monkeypatch.setattr("builtins.open", mock.MagicMock())
    monkeypatch.setattr(yaml, "safe_load", safe_load_mock)

    sut = ConfigRepositoryImpl(filename=filename)

    if exception:
        with pytest.raises(exception):
            sut.read()
    else:
        result = sut.read()
        assert result == helper_config


@pytest.mark.parametrize(
    argnames=("dump_mock", "exception"),
    argvalues=[
        [mock.MagicMock(), None],
        [mock.MagicMock(side_effect=OSError()), WriteError],
    ],
    ids=["OK", "dumpのエラーでエラー"],
)
def test_config_repository_impl_write(
    dump_mock: mock.MagicMock, exception: Type[Exception], monkeypatch: MonkeyPatch
) -> None:
    """writeのテスト."""
    filename = "file_foo"
    sut = ConfigRepositoryImpl(filename=filename)

    open_mock = mock.MagicMock()

    monkeypatch.setattr(os, "makedirs", mock.MagicMock())
    monkeypatch.setattr("builtins.open", open_mock)
    monkeypatch.setattr(yaml, "dump", dump_mock)

    if exception:
        with pytest.raises(exception):
            sut.write(helper_config)
    else:
        sut.write(helper_config)

    open_mock.assert_called_once_with(filename, "wt")
    dump_mock.assert_called_once_with(helper_config.dict(), ANY)
