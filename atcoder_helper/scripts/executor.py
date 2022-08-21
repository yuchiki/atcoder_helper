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

    def __init__(
        self,
        auth_service: AuthService,
        atcoder_helper_config_service: AtCoderHelperConfigService,
        execute_test_service: ExecuteTestService,
        fetch_task_service: FetchTaskService,
        init_task_dir_service: InitTaskDirService,
    ) -> None:
        """__init__.

        Args:
            auth_service (AuthService, optional): _
            atcoder_helper_config_service (AtCoderHelperConfigService, optional): _
            execute_test_service (ExecuteTestService, optional): _
            fetch_task_service (FetchTaskService, optional): _
            init_task_dir_service (InitTaskDirService, optional): _
        """
        self._auth_service = auth_service
        self._atcoder_helper_config_service = atcoder_helper_config_service
        self._execute_test_service = execute_test_service
        self._fetch_task_service = fetch_task_service
        self._init_task_dir_service = init_task_dir_service

    def auth_login_handler(self, args: argparse.Namespace) -> None:
        """ログインする."""
        name = input("name:")
        password = getpass.getpass("password:")
        try:
            self._auth_service.login(name, password)
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

        print("logged in.")

    def auth_logout_handler(self, args: argparse.Namespace) -> None:
        """ログアウトする.

        Args:
            args (argparse.Namespace): _description_
        """
        try:
            self._auth_service.logout()
        except service_errors.ConfigAccessError:
            print("設定ファイルを正しく読み込めません.")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)

    def auth_status_handler(self, args: argparse.Namespace) -> None:
        """現在ログインしているかどうかを確認する."""
        try:
            stat = self._auth_service.status()
        except service_errors.AtcoderAccessError:
            print("atcoderと通信できません")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)
        except service_errors.ConfigAccessError:
            print("設定ファイルが読み込めません")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)

        if stat:
            print("logged in.")
        else:
            print("logged out.")

    def task_init_handler(self, args: argparse.Namespace) -> None:
        """既存のディレクトリをタスク用に初期化する.

        Args:
            args (argparse.Namespace): 引数
        """
        try:
            self._init_task_dir_service.init_task()
        except service_errors.ConfigAccessError:
            print("設定ファイルへの読み書きでエラーが発生しました")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)
        except service_errors.DirectoryNotEmpty:
            print("初期化しようとしているディレクトリが空ではありません")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)

    def task_create_handler(self, args: argparse.Namespace) -> None:
        """新規にディレクトリを作り、タスク用に初期化する.

        Args:
            args (argparse.Namespace): コマンドライン引数
        """
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

    def execute_test_handler(self, args: argparse.Namespace) -> None:
        """テストスイートを実行する.

        Args:
            args (argparse.Namespace): コマンドライン引数
        """
        try:
            self._execute_test_service.execute_test()
        except service_errors.ConfigAccessError:
            print("設定ファイルの読み書きに失敗しました")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)

    def fetch_task_handler(self, args: argparse.Namespace) -> None:
        """テストケースをフェッチする.

        Args:
            args (argparse.Namespace): コマンドライン引数
        """
        try:
            self._fetch_task_service.fetch_task(args.contest, args.task)
        except service_errors.AtcoderAccessError:
            print("AtCoderサイトからデータを取得する過程でエラーが発生しました")
            if args.verbose:
                print(traceback.format_exc())

            sys.exit(1)

    def config_init_handler(self, args: argparse.Namespace) -> None:
        """atcoder_helper全体設定ファイルを初期化する.

        Args:
            args (argparse.Namespace): 引数
        """
        try:
            self._atcoder_helper_config_service.init_config()
        except service_errors.ConfigAccessError:
            print("設定ファイルの読み書きに失敗しました")
            if args.verbose:
                print(traceback.format_exc())

            sys.exit(1)

    def config_languages_handler(self, args: argparse.Namespace) -> None:
        """使用可能な言語一覧を表示する.

        Args:
            args (argparse.Namespace): 引数
        """
        try:
            languages = self._atcoder_helper_config_service.config_languages()
        except service_errors.ConfigAccessError:
            print("設定ファイルの読み書きに失敗しました")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)

        for language_name in languages:
            print(language_name)

    def config_default_language_handler(self, args: argparse.Namespace) -> None:
        """デフォルトの言語を表示する.

        Args:
            args (argparse.Namespace): 引数
        """
        try:
            default_language = (
                self._atcoder_helper_config_service.config_default_language()
            )
        except service_errors.ConfigAccessError:
            print("設定ファイルの読み書きに失敗しました")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)

        print(default_language.name)

    def config_use_handler(self, args: argparse.Namespace) -> None:
        """デフォルトの言語を設定する.

        Args:
            args (argparse.Namespace): 引数
        """
        try:
            self._atcoder_helper_config_service.config_use(args.language)
        except service_errors.UndefinedLanguage:
            print(f"{args.language}は使用可能な言語の中に存在しません。設定ファイルを変更し、言語設定を追加してください。")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)
        except service_errors.ConfigAccessError:
            print("設定ファイルの読み書きに失敗しました")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)


def get_default_executor() -> Executor:
    """標準Executorを返す."""
    return Executor(
        auth_service=get_default_auth_service(),
        atcoder_helper_config_service=(get_default_atcoder_helper_config_service()),
        execute_test_service=get_default_execute_test_service(),
        fetch_task_service=get_default_fetch_task_service(),
        init_task_dir_service=get_default_init_task_dir_service(),
    )
