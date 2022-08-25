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
from atcoder_helper.repositories.errors import WriteError

helper_config = AtCoderHelperConfig(
    languages={"foo": LanguageConfig(name=" foo", build=[], run=[])},
    default_language="foo",
)


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
