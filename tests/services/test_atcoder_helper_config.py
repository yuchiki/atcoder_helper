"""Tests for atcoder_helper_config."""


from typing import Dict
from typing import Type

import mock
import pytest

from atcoder_helper.entities.atcoder_helper_config import AtCoderHelperConfig
from atcoder_helper.entities.atcoder_helper_config import LanguageConfig
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

_default_language_config = LanguageConfig(
    name="c", template_dir=None, use_default_template=False, build=[], run=[]
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


_test_config_default_language_parameters = {
    "OK": [
        mock.MagicMock(read=mock.MagicMock(return_value=_default_config)),
        None,
        _default_language_config,
    ],
    "読み取りエラー時にエラー": [
        mock.MagicMock(read=mock.MagicMock(side_effect=ReadError())),
        ConfigAccessError,
        "",
    ],
}


@pytest.mark.parametrize(
    argnames=("config_repo_mock", "exception", "return_value"),
    argvalues=list(_test_config_default_language_parameters.values()),
    ids=list(_test_config_default_language_parameters.keys()),
)
def test_config_default_language(
    config_repo_mock: mock.MagicMock,
    exception: Type[Exception],
    return_value: LanguageConfig,
) -> None:
    """config_default_languageのテスト."""
    sut = _get_sut(config_repo=config_repo_mock)

    if exception is not None:
        with pytest.raises(exception):
            sut.config_default_language()
    else:
        assert return_value == sut.config_default_language()


_test_config_languages_parameters = {
    "OK": [
        mock.MagicMock(read=mock.MagicMock(return_value=_default_config)),
        None,
        _default_config.languages,
    ],
    "読み取りエラー時にエラー": [
        mock.MagicMock(read=mock.MagicMock(side_effect=ReadError())),
        ConfigAccessError,
        "",
    ],
}


@pytest.mark.parametrize(
    argnames=("config_repo_mock", "exception", "return_value"),
    argvalues=list(_test_config_languages_parameters.values()),
    ids=list(_test_config_languages_parameters.keys()),
)
def test_config_languages(
    config_repo_mock: mock.MagicMock,
    exception: Type[Exception],
    return_value: Dict[str, LanguageConfig],
) -> None:
    """config_languagesのテスト."""
    sut = _get_sut(config_repo=config_repo_mock)

    if exception is not None:
        with pytest.raises(exception):
            sut.config_languages()
    else:
        assert return_value == sut.config_languages()


_test_init_config_parameter = {
    "OK": [
        mock.MagicMock(),
        mock.MagicMock(read=mock.MagicMock(return_value=_default_config)),
        None,
        _default_config,
    ],
    "デフォルトファイルを読み込めなかったらエラー": [
        mock.MagicMock(),
        mock.MagicMock(read=mock.MagicMock(side_effect=ReadError())),
        ConfigAccessError,
        "",
    ],
    "設定を書き込めなかったらエラー": [
        mock.MagicMock(write=mock.MagicMock(side_effect=WriteError())),
        mock.MagicMock(read=mock.MagicMock(return_value=_default_config)),
        ConfigAccessError,
        "",
    ],
}


@pytest.mark.parametrize(
    ("config_repo_mock", "default_config_repo_mock", "exception", "value_to_write"),
    argvalues=list(_test_init_config_parameter.values()),
    ids=list(_test_init_config_parameter.keys()),
)
def test_init_config(
    config_repo_mock: mock.MagicMock,
    default_config_repo_mock: mock.MagicMock,
    exception: Type[Exception],
    value_to_write: AtCoderHelperConfig,
) -> None:
    """init_configのテスト."""
    sut = _get_sut(
        config_repo=config_repo_mock,
        default_config_repo=default_config_repo_mock,
    )

    if exception is not None:
        with pytest.raises(exception):
            sut.init_config()
    else:
        sut.init_config()
        config_repo_mock.write.assert_called_once_with(value_to_write)
