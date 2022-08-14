"""atcoder_helperコマンドの実行時情報を保持するクラス."""
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
from atcoder_helper.services.init_task import InitTaskDirService
from atcoder_helper.services.init_task import get_default_init_task_dir_service


class Executor:
    """実行時に必要な情報を持ちまわるためのクラス."""

    _auth_service: AuthService
    _atcoder_helper_config_service: AtCoderHelperConfigService
    _execute_test_service: ExecuteTestService
    _fetch_task_service: FetchTaskService
    _init_task_dir_service: InitTaskDirService

    def __init__(self) -> None:
        """__init__."""
        self._auth_service = get_default_auth_service()
        self._atcoder_helper_config_service = (
            get_default_atcoder_helper_config_service()
        )
        self._execute_test_service = get_default_execute_test_service()
        self._fetch_task_service = get_default_fetch_task_service()
        self._init_task_dir_service = get_default_init_task_dir_service()

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
            self._init_task_dir_service.init_task()
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
            self._init_task_dir_service.init_task(
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
