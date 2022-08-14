"""atcoder_helperコマンドのエントリポイント."""
import argparse
import getpass
import os
import sys
import traceback

from atcoder_helper.services import errors as service_errors
from atcoder_helper.services.atcoder_helper_config import AtCoderHelperConfigService
from atcoder_helper.services.atcoder_helper_config import (
    get_default_atcoder_helper_config_service,
)
from atcoder_helper.services.auth import AuthService
from atcoder_helper.services.auth import get_default_auth_service
from atcoder_helper.services.execute_test import ExecuteTestService
from atcoder_helper.services.execute_test import get_default_execute_test_service
from atcoder_helper.services.fetch_task import FetchTaskService
from atcoder_helper.services.fetch_task import get_default_fetch_task_service
from atcoder_helper.services.init_task import init_task


def main() -> None:
    """entrypoint."""
    entrypoint = EntryPoint()
    entrypoint.main()


class EntryPoint:
    """実行時に必要な情報を持ちまわるためのクラス."""

    _auth_service: AuthService
    _atcoder_helper_config_service: AtCoderHelperConfigService
    _execute_test_service: ExecuteTestService
    _fetch_task_service: FetchTaskService

    def __init__(self) -> None:
        """__init__."""
        self._auth_service = get_default_auth_service()
        self._atcoder_helper_config_service = (
            get_default_atcoder_helper_config_service()
        )
        self._execute_test_service = get_default_execute_test_service()
        self._fetch_task_service = get_default_fetch_task_service()

    def main(self) -> None:
        """main."""
        root_parser = argparse.ArgumentParser(description="atcoder の手助けをするコマンド")
        root_parser.set_defaults(parser=root_parser)
        root_parser.add_argument("--verbose", action="store_true")
        root_subparsers = root_parser.add_subparsers()

        _set_auth_parser(root_subparsers.add_parser("auth"))
        _set_exec_parser(root_subparsers.add_parser("exec"))
        _set_fetch_parser(root_subparsers.add_parser("fetch"))
        _set_task_pasrer(root_subparsers.add_parser("task"))
        _set_config_parser(root_subparsers.add_parser("config"))

        args = root_parser.parse_args()
        if hasattr(args, "handler"):
            args.handler(self=self, args=args)
        else:
            args.parser.print_help()

    def _auth_login_handler(self, args: argparse.Namespace) -> None:
        name = input("name:")
        password = getpass.getpass("password:")
        try:
            status = self._auth_service.login(name, password)
        except service_errors.AlreadyLoggedIn:
            print("既にログインしています.")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)
        except service_errors.ConfigAccessError:
            print("設定ファイルを正しく読み込めません.")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)
        except service_errors.AtcoderAccessError:
            print("AtCoderのサイトと正しく通信ができません.")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)

        if status:
            print("logged in.")
        else:
            print("fail to log in.")
            sys.exit(1)

    def _auth_logout_handler(self, args: argparse.Namespace) -> None:
        try:
            self._auth_service.logout()
        except service_errors.ConfigAccessError:
            print("設定ファイルを正しく読み込めません.")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)

    def _auth_status(self, args: argparse.Namespace) -> None:
        try:
            stat = self._auth_service.status()
        except service_errors.AtcoderAccessError:
            print("atcoderと通信できません")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)

        if stat:
            print("logged in.")
        else:
            print("logged out.")

    def _task_init_handler(self, args: argparse.Namespace) -> None:
        try:
            init_task()
        except service_errors.ConfigAccessError:
            print("設定ファイルへの読み書きでエラーが発生しました")
            if args.verbose:
                print(traceback.format_exc())
        except service_errors.DirectoryNotEmpty:
            print("初期化しようとしているディレクトリが空ではありません")
            if args.verbose:
                print(traceback.format_exc())

    def _task_create_handler(self, args: argparse.Namespace) -> None:
        try:
            init_task(
                dir=os.path.join(args.contest, args.task),
                contest=args.contest,
                task=args.task,
            )
        except service_errors.ConfigAccessError:
            print("設定ファイルへの読み書きでエラーが発生しました")
            if args.verbose:
                print(traceback.format_exc())
        except service_errors.DirectoryNotEmpty:
            print("初期化しようとしているディレクトリが空ではありません")
            if args.verbose:
                print(traceback.format_exc())

    def _execute_test_handler(self, args: argparse.Namespace) -> None:
        try:
            self._execute_test_service.execute_test()
        except service_errors.ConfigAccessError:
            print("設定ファイルの読み書きに失敗しました")
            if args.verbose:
                print(traceback.format_exc())

    def _fetch_task_handler(self, args: argparse.Namespace) -> None:
        try:
            self._fetch_task_service.fetch_task(args.contest, args.task)
        except service_errors.AtcoderAccessError:
            print("AtCoderサイトからデータを取得する過程でエラーが発生しました")
            if args.verbose:
                print(traceback.format_exc())

    def _config_init_handler(self, args: argparse.Namespace) -> None:
        try:
            self._atcoder_helper_config_service.init_config()
        except service_errors.ConfigAccessError:
            print("設定ファイルの読み書きに失敗しました")
            if args.verbose:
                print(traceback.format_exc())

    def _config_languages_handler(self, args: argparse.Namespace) -> None:

        try:
            languages = self._atcoder_helper_config_service.config_languages()
        except service_errors.ConfigAccessError:
            print("設定ファイルの読み書きに失敗しました")
            if args.verbose:
                print(traceback.format_exc())

        for language_name in languages:
            print(language_name)

    def _config_default_language_handler(self, args: argparse.Namespace) -> None:
        try:
            default_language = (
                self._atcoder_helper_config_service.config_default_language()
            )
        except service_errors.ConfigAccessError:
            print("設定ファイルの読み書きに失敗しました")
            if args.verbose:
                print(traceback.format_exc())

        print(default_language.name)

    def _config_use_handler(self, args: argparse.Namespace) -> None:
        try:
            self._atcoder_helper_config_service.config_use(args.language)
        except service_errors.UndefinedLanguage:
            print(f"{args.language}は使用可能な言語の中に存在しません。設定ファイルを変更し、言語設定を追加してください。")
            if args.verbose:
                print(traceback.format_exc())
        except service_errors.ConfigAccessError:
            print("設定ファイルの読み書きに失敗しました")
            if args.verbose:
                print(traceback.format_exc())


def _set_auth_parser(parser_auth: argparse.ArgumentParser) -> None:
    parser_auth.set_defaults(parser=parser_auth)

    parser_auth_subparsers = parser_auth.add_subparsers()

    parser_auth_login = parser_auth_subparsers.add_parser("login")
    parser_auth_login.set_defaults(
        handler=EntryPoint._auth_login_handler, parser=parser_auth_login
    )

    parser_auth_logout = parser_auth_subparsers.add_parser("logout")
    parser_auth_logout.set_defaults(
        handler=EntryPoint._auth_logout_handler, parser=parser_auth_logout
    )

    parser_auth_status = parser_auth_subparsers.add_parser("status")
    parser_auth_status.set_defaults(
        handler=EntryPoint._auth_status, parser=parser_auth_status
    )


def _set_exec_parser(parser_exec: argparse.ArgumentParser) -> None:
    parser_exec.set_defaults(
        handler=EntryPoint._execute_test_handler, parser=parser_exec
    )


def _set_fetch_parser(parser_fetch: argparse.ArgumentParser) -> None:
    parser_fetch.set_defaults(
        handler=EntryPoint._fetch_task_handler, parser=parser_fetch
    )
    parser_fetch.add_argument("--contest")
    parser_fetch.add_argument("--task")


def _set_task_pasrer(parser_task: argparse.ArgumentParser) -> None:
    parser_task.set_defaults(parser=parser_task)

    parser_task_subparsers = parser_task.add_subparsers()

    parser_task_init = parser_task_subparsers.add_parser("init")
    parser_task_init.set_defaults(
        handler=EntryPoint._task_init_handler, parser=parser_task_init
    )

    parser_task_create = parser_task_subparsers.add_parser("create")
    parser_task_create.set_defaults(
        handler=EntryPoint._task_create_handler, parser=parser_task_create
    )
    parser_task_create.add_argument("contest")
    parser_task_create.add_argument("task")


def _set_config_parser(parser_config: argparse.ArgumentParser) -> None:
    parser_config.set_defaults(parser=parser_config)

    parser_config_subparsers = parser_config.add_subparsers()

    parser_config_init = parser_config_subparsers.add_parser("init")
    parser_config_init.set_defaults(
        handler=EntryPoint._config_init_handler, parser=parser_config_init
    )

    parser_config_languages = parser_config_subparsers.add_parser("languages")
    parser_config_languages.set_defaults(
        handler=EntryPoint._config_languages_handler, parser=parser_config_languages
    )

    parser_config_default_language = parser_config_subparsers.add_parser("default")
    parser_config_default_language.set_defaults(
        handler=EntryPoint._config_default_language_handler,
        parser=parser_config_default_language,
    )

    parser_config_use = parser_config_subparsers.add_parser("use")
    parser_config_use.set_defaults(
        handler=EntryPoint._config_use_handler, parser=parser_config_use
    )
    parser_config_use.add_argument("language")
