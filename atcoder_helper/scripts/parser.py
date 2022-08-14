"""parser."""

import argparse

from atcoder_helper.scripts.executor import Executor


def get_root_parser() -> argparse.ArgumentParser:
    """rootParserを返します.

    Returns:
        argparse.ArgumentParser:
    """
    root_parser = argparse.ArgumentParser(description="atcoder の手助けをするコマンド")
    root_parser.set_defaults(parser=root_parser)
    root_parser.add_argument("--verbose", action="store_true")
    root_subparsers = root_parser.add_subparsers()

    _set_auth_parser(root_subparsers.add_parser("auth"))
    _set_exec_parser(root_subparsers.add_parser("exec"))
    _set_fetch_parser(root_subparsers.add_parser("fetch"))
    _set_task_pasrer(root_subparsers.add_parser("task"))
    _set_config_parser(root_subparsers.add_parser("config"))

    return root_parser


def _set_auth_parser(parser_auth: argparse.ArgumentParser) -> None:
    parser_auth.set_defaults(parser=parser_auth)

    parser_auth_subparsers = parser_auth.add_subparsers()

    parser_auth_login = parser_auth_subparsers.add_parser("login")
    parser_auth_login.set_defaults(
        handler=Executor.auth_login_handler, parser=parser_auth_login
    )

    parser_auth_logout = parser_auth_subparsers.add_parser("logout")
    parser_auth_logout.set_defaults(
        handler=Executor.auth_logout_handler, parser=parser_auth_logout
    )

    parser_auth_status = parser_auth_subparsers.add_parser("status")
    parser_auth_status.set_defaults(
        handler=Executor.auth_status_handler, parser=parser_auth_status
    )


def _set_exec_parser(parser_exec: argparse.ArgumentParser) -> None:
    parser_exec.set_defaults(handler=Executor.execute_test_handler, parser=parser_exec)


def _set_fetch_parser(parser_fetch: argparse.ArgumentParser) -> None:
    parser_fetch.set_defaults(handler=Executor.fetch_task_handler, parser=parser_fetch)
    parser_fetch.add_argument("--contest")
    parser_fetch.add_argument("--task")


def _set_task_pasrer(parser_task: argparse.ArgumentParser) -> None:
    parser_task.set_defaults(parser=parser_task)

    parser_task_subparsers = parser_task.add_subparsers()

    parser_task_init = parser_task_subparsers.add_parser("init")
    parser_task_init.set_defaults(
        handler=Executor.task_init_handler, parser=parser_task_init
    )

    parser_task_create = parser_task_subparsers.add_parser("create")
    parser_task_create.set_defaults(
        handler=Executor.task_create_handler, parser=parser_task_create
    )
    parser_task_create.add_argument("contest")
    parser_task_create.add_argument("task")


def _set_config_parser(parser_config: argparse.ArgumentParser) -> None:
    parser_config.set_defaults(parser=parser_config)

    parser_config_subparsers = parser_config.add_subparsers()

    parser_config_init = parser_config_subparsers.add_parser("init")
    parser_config_init.set_defaults(
        handler=Executor.config_init_handler, parser=parser_config_init
    )

    parser_config_languages = parser_config_subparsers.add_parser("languages")
    parser_config_languages.set_defaults(
        handler=Executor.config_languages_handler, parser=parser_config_languages
    )

    parser_config_default_language = parser_config_subparsers.add_parser("default")
    parser_config_default_language.set_defaults(
        handler=Executor.config_default_language_handler,
        parser=parser_config_default_language,
    )

    parser_config_use = parser_config_subparsers.add_parser("use")
    parser_config_use.set_defaults(
        handler=Executor.config_use_handler, parser=parser_config_use
    )
    parser_config_use.add_argument("language")
