"""atcoder_helperコマンドの実行時情報を保持するクラス."""
import argparse
import getpass
import os
import sys
import traceback

from injector import inject

from atcoder_helper._version import __version__
from atcoder_helper.usecases import errors as usecase_errors
from atcoder_helper.usecases.atcoder_helper_config import AtCoderHelperConfigUsecase
from atcoder_helper.usecases.atcoder_helper_config import (
    get_default_atcoder_helper_config_usecase,
)
from atcoder_helper.usecases.auth import AuthUsecase
from atcoder_helper.usecases.auth import get_default_auth_usecase
from atcoder_helper.usecases.execute_test import ExecuteTestUsecase
from atcoder_helper.usecases.execute_test import get_default_execute_test_usecase
from atcoder_helper.usecases.fetch_task import FetchTaskUsecase
from atcoder_helper.usecases.fetch_task import get_default_fetch_task_usecase
from atcoder_helper.usecases.init_task import InitTaskDirUsecase
from atcoder_helper.usecases.init_task import get_default_init_task_dir_usecase


class Controller:
    """実行時に必要な情報を持ちまわるためのクラス."""

    _auth_usecase: AuthUsecase
    _atcoder_helper_config_usecase: AtCoderHelperConfigUsecase
    _execute_test_usecase: ExecuteTestUsecase
    _fetch_task_usecase: FetchTaskUsecase
    _init_task_dir_usecase: InitTaskDirUsecase

    @inject
    def __init__(
        self,
        auth_usecase: AuthUsecase,
        atcoder_helper_config_usecase: AtCoderHelperConfigUsecase,
        execute_test_usecase: ExecuteTestUsecase,
        fetch_task_usecase: FetchTaskUsecase,
        init_task_dir_usecase: InitTaskDirUsecase,
    ) -> None:
        """__init__.

        Args:
            auth_usecase (AuthUsecase, optional): _
            atcoder_helper_config_usecase (AtCoderHelperConfigUsecase, optional): _
            execute_test_usecase (ExecuteTestUsecase, optional): _
            fetch_task_usecase (FetchTaskUsecase, optional): _
            init_task_dir_usecase (InitTaskDirUsecase, optional): _
        """
        self._auth_usecase = auth_usecase
        self._atcoder_helper_config_usecase = atcoder_helper_config_usecase
        self._execute_test_usecase = execute_test_usecase
        self._fetch_task_usecase = fetch_task_usecase
        self._init_task_dir_usecase = init_task_dir_usecase

    def auth_login_handler(self, args: argparse.Namespace) -> None:
        """ログインする."""
        name = args.username if args.username else input("name:")
        password = args.password if args.password else getpass.getpass("password:")
        try:
            self._auth_usecase.login(name, password)
        except usecase_errors.AlreadyLoggedIn:
            print("既にログインしています.")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)
        except usecase_errors.ConfigAccessError:
            print("設定ファイルを正しく読み込めません.")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)
        except usecase_errors.AtcoderAccessError:
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
            self._auth_usecase.logout()
        except usecase_errors.ConfigAccessError:
            print("設定ファイルを正しく読み込めません.")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)

    def auth_status_handler(self, args: argparse.Namespace) -> None:
        """現在ログインしているかどうかを確認する."""
        try:
            stat = self._auth_usecase.status()
        except usecase_errors.AtcoderAccessError:
            print("atcoderと通信できません")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)
        except usecase_errors.ConfigAccessError:
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
            self._init_task_dir_usecase.init_task()
        except usecase_errors.ConfigAccessError:
            print("設定ファイルへの読み書きでエラーが発生しました")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)
        except usecase_errors.DirectoryNotEmpty:
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
            self._init_task_dir_usecase.init_task(
                dir=os.path.join(args.contest, args.task),
                contest=args.contest,
                task=args.task,
            )
        except usecase_errors.ConfigAccessError:
            print("設定ファイルへの読み書きでエラーが発生しました")
            if args.verbose:
                print(traceback.format_exc())
        except usecase_errors.DirectoryNotEmpty:
            print("初期化しようとしているディレクトリが空ではありません")
            if args.verbose:
                print(traceback.format_exc())

    def execute_test_handler(self, args: argparse.Namespace) -> None:
        """テストスイートを実行する.

        Args:
            args (argparse.Namespace): コマンドライン引数
        """
        try:
            self._execute_test_usecase.execute_test()
        except usecase_errors.ConfigAccessError:
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
            self._fetch_task_usecase.fetch_task(args.contest, args.task)
        except usecase_errors.AtcoderAccessError:
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
            self._atcoder_helper_config_usecase.init_config()
        except usecase_errors.ConfigAccessError:
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
            languages = self._atcoder_helper_config_usecase.config_languages()
        except usecase_errors.ConfigAccessError:
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
                self._atcoder_helper_config_usecase.config_default_language()
            )
        except usecase_errors.ConfigAccessError:
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
            self._atcoder_helper_config_usecase.config_use(args.language)
        except usecase_errors.UndefinedLanguage:
            print(f"{args.language}は使用可能な言語の中に存在しません。設定ファイルを変更し、言語設定を追加してください。")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)
        except usecase_errors.ConfigAccessError:
            print("設定ファイルの読み書きに失敗しました")
            if args.verbose:
                print(traceback.format_exc())
            sys.exit(1)

    def version_handler(self, args: argparse.Namespace) -> None:
        """現在のバージョンを表示する.

        Args:
            args (argparse.Namespace): 引数
        """
        print(__version__)


def get_default_controller() -> Controller:
    """標準Controllerを返す."""
    return Controller(
        auth_usecase=get_default_auth_usecase(),
        atcoder_helper_config_usecase=(get_default_atcoder_helper_config_usecase()),
        execute_test_usecase=get_default_execute_test_usecase(),
        fetch_task_usecase=get_default_fetch_task_usecase(),
        init_task_dir_usecase=get_default_init_task_dir_usecase(),
    )
