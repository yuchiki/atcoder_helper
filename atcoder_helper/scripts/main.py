"""atcoder_helperコマンドのエントリポイント."""
import argparse

from atcoder_helper.services.execute_test import execute_test
from atcoder_helper.services.fetch_task import fetch_task
from atcoder_helper.services.init_config import init_config
from atcoder_helper.services.init_task import init_task


def main() -> None:
    """main."""
    root_parser = argparse.ArgumentParser(description="atcoder の手助けをするコマンド")
    root_parser.set_defaults(parser=root_parser)
    root_subparsers = root_parser.add_subparsers()

    parser_exec = root_subparsers.add_parser("exec")
    parser_exec.set_defaults(handler=_execute_test_handler, parser=parser_exec)

    parser_fetch = root_subparsers.add_parser("fetch")
    parser_fetch.set_defaults(handler=_fetch_task_handler, parser=parser_fetch)
    parser_fetch.add_argument("contest")
    parser_fetch.add_argument("task")

    parser_init_task = root_subparsers.add_parser("init_task")
    parser_init_task.set_defaults(handler=_init_task_handler, parser=parser_init_task)

    parser_config = root_subparsers.add_parser("config")
    parser_config.set_defaults(parser=parser_config)

    parser_config_subparsers = parser_config.add_subparsers()

    parser_config_init = parser_config_subparsers.add_parser("init")
    parser_config_init.set_defaults(
        handler=_config_init_handler, parser=parser_config_init
    )

    args = root_parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        args.parser.print_help()


def _init_task_handler(_: argparse.Namespace) -> None:
    init_task()


def _execute_test_handler(_: argparse.Namespace) -> None:
    execute_test()


def _fetch_task_handler(args: argparse.Namespace) -> None:
    fetch_task(args.contest, args.task)


def _config_init_handler(_: argparse.Namespace) -> None:
    init_config()
