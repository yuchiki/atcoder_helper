"""Tests for Controller."""


import argparse
from typing import Any
from typing import Optional

import mock
import pytest

from atcoder_helper.application.usecases.atcoder_helper_config import (
    AtCoderHelperConfigUsecase,
)
from atcoder_helper.application.usecases.auth import AuthUsecase
from atcoder_helper.application.usecases.errors import AlreadyLoggedIn
from atcoder_helper.application.usecases.errors import AtcoderAccessError
from atcoder_helper.application.usecases.errors import ConfigAccessError
from atcoder_helper.application.usecases.errors import DirectoryNotEmpty
from atcoder_helper.application.usecases.errors import UndefinedLanguage
from atcoder_helper.application.usecases.execute_test import ExecuteTestUsecase
from atcoder_helper.application.usecases.fetch_task import FetchTaskUsecase
from atcoder_helper.application.usecases.init_task import InitTaskDirUsecase
from atcoder_helper.entities.atcoder_helper_config import LanguageConfig
from atcoder_helper.scripts.controller import Controller


def _get_sut(
    auth_usecase_mock: AuthUsecase = mock.MagicMock(),
    atcoder_helper_config_usecase_mock: AtCoderHelperConfigUsecase = mock.MagicMock(),
    execute_test_usecase_mock: ExecuteTestUsecase = mock.MagicMock(),
    fetch_task_usecase_mock: FetchTaskUsecase = mock.MagicMock(),
    init_task_dir_usecase_mock: InitTaskDirUsecase = mock.MagicMock(),
) -> Controller:
    return Controller(
        auth_usecase=auth_usecase_mock,
        atcoder_helper_config_usecase=atcoder_helper_config_usecase_mock,
        execute_test_usecase=execute_test_usecase_mock,
        fetch_task_usecase=fetch_task_usecase_mock,
        init_task_dir_usecase=init_task_dir_usecase_mock,
    )


def _get_default_namespace(**additional_kwargs: str) -> argparse.Namespace:
    return argparse.Namespace(verbose=False, **additional_kwargs)


@pytest.mark.parametrize(
    argnames=(
        "login_side_effect",
        "should_succeed",
    ),
    argvalues=[
        [None, True],
        [AlreadyLoggedIn(), False],
        [ConfigAccessError(), False],
        [AtcoderAccessError(), False],
    ],
)
def test_auth_login_handler(
    login_side_effect: Optional[Exception], should_succeed: bool
) -> None:
    """auth_login_handlerのテスト."""
    sut = _get_sut(
        auth_usecase_mock=mock.MagicMock(
            login=mock.MagicMock(side_effect=login_side_effect)
        )
    )

    name = "foo"
    password = "bar"

    with (
        mock.patch("builtins.input", return_value=name),
        mock.patch("getpass.getpass", return_value=password),
    ):
        if should_succeed:
            sut.auth_login_handler(_get_default_namespace(username="", password=""))
        else:
            with pytest.raises(SystemExit) as e:
                sut.auth_login_handler(_get_default_namespace(username="", password=""))
            assert e.value.code == 1


@pytest.mark.parametrize(
    argnames=("logout_side_effect", "should_succeed"),
    argvalues=[[None, True], [ConfigAccessError(), False]],
)
def test_auth_logout_handler(
    logout_side_effect: Exception, should_succeed: bool
) -> None:
    """auth_logout_handlerのテスト."""
    sut = _get_sut(
        auth_usecase_mock=mock.MagicMock(
            logout=mock.MagicMock(side_effect=logout_side_effect)
        )
    )
    if should_succeed:
        sut.auth_logout_handler(_get_default_namespace())
    else:
        with pytest.raises(SystemExit) as e:
            sut.auth_logout_handler(_get_default_namespace())
        assert e.value.code == 1


@pytest.mark.parametrize(
    argnames=("status_return_value", "status_side_effect", "message", "should_succeed"),
    argvalues=[
        [True, None, "logged in.\n", True],
        [False, None, "logged out.\n", True],
        [False, AtcoderAccessError(), None, False],
    ],
)
def test_auth_status_handler(
    capfd: Any,
    status_return_value: bool,
    status_side_effect: Exception,
    message: str,
    should_succeed: bool,
) -> None:
    """auth_status_handlerのテスト."""
    sut = _get_sut(
        auth_usecase_mock=mock.MagicMock(
            status=mock.MagicMock(
                side_effect=status_side_effect, return_value=status_return_value
            )
        )
    )

    if should_succeed:
        sut.auth_status_handler(_get_default_namespace())
        assert capfd.readouterr().out == message
    else:
        with pytest.raises(SystemExit) as e:
            sut.auth_status_handler(_get_default_namespace())
        assert e.value.code == 1


@pytest.mark.parametrize(
    argnames=("init_task_side_effect", "should_succeed"),
    argvalues=[[None, True], [ConfigAccessError, False], [DirectoryNotEmpty, False]],
)
def test_task_init_handler(
    init_task_side_effect: Exception, should_succeed: bool
) -> None:
    """task_init_handlerのテスト."""
    sut = _get_sut(
        init_task_dir_usecase_mock=mock.MagicMock(
            init_task=mock.MagicMock(side_effect=init_task_side_effect)
        )
    )

    if should_succeed:
        sut.task_init_handler(_get_default_namespace())
    else:
        with pytest.raises(SystemExit) as e:
            sut.task_init_handler(_get_default_namespace())
        assert e.value.code == 1


@pytest.mark.parametrize(
    argnames=("init_task_side_effect", "should_succeed"),
    argvalues=[
        [None, True],
        [ConfigAccessError(), False],
        [DirectoryNotEmpty(), False],
    ],
)
def test_task_create_handler(
    init_task_side_effect: Exception, should_succeed: bool
) -> None:
    """task_create_handlerのテスト."""
    contest = "foo"
    task = "bar"
    sut = _get_sut(
        init_task_dir_usecase_mock=mock.MagicMock(
            init_task=mock.MagicMock(side_effect=init_task_side_effect)
        )
    )

    namespace = _get_default_namespace(contest=contest, task=task)

    if should_succeed:
        sut.task_init_handler(namespace)
    else:
        with pytest.raises(SystemExit) as e:
            sut.task_init_handler(namespace)
        assert e.value.code == 1


@pytest.mark.parametrize(
    argnames=("execute_test_side_effect", "should_succeed"),
    argvalues=[[None, True], [ConfigAccessError(), False]],
)
def test_execute_test_handler(
    execute_test_side_effect: Exception, should_succeed: bool
) -> None:
    """execute_test_handlerのテスト."""
    sut = _get_sut(
        execute_test_usecase_mock=mock.MagicMock(
            execute_test=mock.MagicMock(side_effect=execute_test_side_effect)
        )
    )

    if should_succeed:
        sut.execute_test_handler(_get_default_namespace())
    else:
        with pytest.raises(SystemExit) as e:
            sut.execute_test_handler(_get_default_namespace())
        assert e.value.code == 1


@pytest.mark.parametrize(
    argnames=("fetch_task_side_effect", "should_succeed"),
    argvalues=[[None, True], [AtcoderAccessError, False]],
)
def test_fetch_task_handler(
    fetch_task_side_effect: Exception, should_succeed: bool
) -> None:
    """fetch_task_handlerのテスト."""
    sut = _get_sut(
        fetch_task_usecase_mock=mock.MagicMock(
            fetch_task=mock.MagicMock(side_effect=fetch_task_side_effect)
        )
    )
    contest = "foo"
    task = "bar"
    args = _get_default_namespace(contest=contest, task=task)

    if should_succeed:
        sut.fetch_task_handler(args)
    else:
        with pytest.raises(SystemExit) as e:
            sut.fetch_task_handler(args)
        assert e.value.code == 1


@pytest.mark.parametrize(
    argnames=("init_config_side_effect", "should_succeed"),
    argvalues=[[None, True], [ConfigAccessError, False]],
)
def test_config_init_handler(
    init_config_side_effect: Exception, should_succeed: bool
) -> None:
    """config_init_handlerのテスト."""
    sut = _get_sut(
        atcoder_helper_config_usecase_mock=mock.MagicMock(
            init_config=mock.MagicMock(side_effect=init_config_side_effect)
        )
    )

    args = _get_default_namespace()

    if should_succeed:
        sut.config_init_handler(args)
    else:
        with pytest.raises(SystemExit) as e:
            sut.config_init_handler(args)
        assert e.value.code == 1


@pytest.mark.parametrize(
    argnames=("config_languages_side_effect", "should_succeed"),
    argvalues=[[None, True], [ConfigAccessError, False]],
)
def test_config_languages_handler(
    config_languages_side_effect: Exception, should_succeed: bool
) -> None:
    """config_languages_handlerのテスト."""
    languages = {"c": LanguageConfig(name="c", build=[], run=[])}

    sut = _get_sut(
        atcoder_helper_config_usecase_mock=mock.MagicMock(
            config_languages=mock.MagicMock(
                side_effect=config_languages_side_effect, return_value=languages
            )
        )
    )

    args = _get_default_namespace()

    if should_succeed:
        sut.config_languages_handler(args)
    else:
        with pytest.raises(SystemExit) as e:
            sut.config_languages_handler(args)
        assert e.value.code == 1


@pytest.mark.parametrize(
    argnames=("default_language_side_effect", "should_succeed"),
    argvalues=[[None, True], [ConfigAccessError(), False]],
)
def test_config_default_language_handler(
    default_language_side_effect: Exception, should_succeed: bool
) -> None:
    """config_default_language_handlerのテスト."""
    language = LanguageConfig(name="c", build=[], run=[])

    sut = _get_sut(
        atcoder_helper_config_usecase_mock=mock.MagicMock(
            config_default_language=mock.MagicMock(
                side_effect=default_language_side_effect, return_value=language
            )
        )
    )

    args = _get_default_namespace()

    if should_succeed:
        sut.config_default_language_handler(args)
    else:
        with pytest.raises(SystemExit) as e:
            sut.config_default_language_handler(args)
        assert e.value.code == 1


@pytest.mark.parametrize(
    argnames=("config_use_side_effect", "should_succeed"),
    argvalues=[
        [None, True],
        [UndefinedLanguage(), False],
        [ConfigAccessError(), False],
    ],
)
def test_config_use_handler(
    config_use_side_effect: Exception, should_succeed: bool
) -> None:
    """config_use_handlerのテスト."""
    language = "csharp"

    sut = _get_sut(
        atcoder_helper_config_usecase_mock=mock.MagicMock(
            config_use=mock.MagicMock(side_effect=config_use_side_effect)
        )
    )

    args = _get_default_namespace(language=language)

    if should_succeed:
        sut.config_use_handler(args)
    else:
        with pytest.raises(SystemExit) as e:
            sut.config_use_handler(args)
        assert e.value.code == 1
