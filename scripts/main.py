import argparse

from atcoder_helper.services.execute_test import execute_test
from atcoder_helper.services.fetch_task import fetch_task


def main():
    root_parser = argparse.ArgumentParser(description="atcoder の手助けをするコマンド")
    root_subparsers = root_parser.add_subparsers()

    parser_exec = root_subparsers.add_parser("exec")
    parser_exec.set_defaults(handler=execute_test_handler)

    parser_fetch = root_subparsers.add_parser("fetch")
    parser_fetch.set_defaults(handler=fetch_task_handler)
    parser_fetch.add_argument("contest")
    parser_fetch.add_argument("task")

    args = root_parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        root_parser.print_help()


def execute_test_handler(_: argparse.Namespace):
    execute_test()


def fetch_task_handler(args: argparse.Namespace):
    fetch_task(args.contest, args.task)


main()
