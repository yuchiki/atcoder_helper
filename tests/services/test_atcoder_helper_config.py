"""Tests for atcoder_helper_config."""


from typing import Type

import mock
import pytest

from atcoder_helper.models.atcoder_helper_config import AtCoderHelperConfig
from atcoder_helper.models.atcoder_helper_config import LanguageConfig
from atcoder_helper.repositories.atcoder_helper_config_repo import ConfigRepository
from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.errors import WriteError
from atcoder_helper.services.atcoder_helper_config import AtCoderHelperConfigServiceImpl
from atcoder_helper.services.errors import ConfigAccessError
from atcoder_helper.services.errors import UndefinedLanguage


def _get_sut(
    config_repo: ConfigRepository = mock.MagicMock(),
    default_config_repo: ConfigRepository = mock.MagicMock(),
) -> AtCoderHelperConfigServiceImpl:
    return AtCoderHelperConfigServiceImpl(
        config_repo=config_repo, default_config_repo=default_config_repo
    )


_default_config = AtCoderHelperConfig(
    languages={
        "c": LanguageConfig(
            name="c", template_dir=None, use_default_template=False, build=[], run=[]
        ),
        "csharp": LanguageConfig(
            name="csharp",
            template_dir=None,
            use_default_template=False,
            build=[],
            run=[],
        ),
        "cpp": LanguageConfig(
            name="cpp", template_dir=None, use_default_template=False, build=[], run=[]
        ),
    },
    default_language="c",
)

_test_config_use_parameters = {
    "OK": [
        mock.MagicMock(read=mock.MagicMock(return_value=_default_config)),
        "c",
        None,
    ],
    "設定しようとしている言語が存在しなかったらエラー": [
        mock.MagicMock(read=mock.MagicMock(return_value=_default_config)),
        "fsharp",
        UndefinedLanguage,
    ],
    "設定ファイルの読み込みに失敗したらエラー": [
        mock.MagicMock(read=mock.MagicMock(side_effect=ReadError())),
        "cpp",
        ConfigAccessError,
    ],
    "設定ファイルの書き込みに失敗したらエラー": [
        mock.MagicMock(
            read=mock.MagicMock(return_value=_default_config),
            write=mock.MagicMock(side_effect=WriteError()),
        ),
        "c",
        ConfigAccessError,
    ],
}


@pytest.mark.parametrize(
    argnames=("config_repo_mock", "language", "exception"),
    argvalues=list(_test_config_use_parameters.values()),
    ids=list(_test_config_use_parameters.keys()),
)
def test_config_use(
    config_repo_mock: mock.MagicMock, language: str, exception: Type[Exception]
) -> None:
    """config_useのテスト."""
    sut = _get_sut(config_repo=config_repo_mock)

    if exception is not None:
        with pytest.raises(exception):
            sut.config_use(language)
    else:
        sut.config_use(language)


def test_config_default_language() -> None:
    """config_default_languageのテスト."""


def test_config_languages() -> None:
    """config_languagesのテスト."""


def test_init_config() -> None:
    """init_configのテスト."""
