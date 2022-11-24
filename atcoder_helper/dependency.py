"""依存性注入モジュール."""

from typing import Type
from typing import TypeVar

from injector import Binder
from injector import Injector

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

T = TypeVar("T")


class Dependency:
    """依存性の注入を管理する."""

    _injector: Injector

    def __init__(self) -> None:
        """init."""
        self._injector = Injector(self.__class__.config)

    @staticmethod
    def config(binder: Binder) -> None:
        """依存性の注入を行う."""
        binder.bind(
            AuthUsecase, get_default_auth_usecase  # type: ignore[type-abstract]
        )
        binder.bind(
            AtCoderHelperConfigUsecase,  # type: ignore[type-abstract]
            get_default_atcoder_helper_config_usecase,
        )
        binder.bind(
            ExecuteTestUsecase,  # type: ignore[type-abstract]
            get_default_execute_test_usecase,
        )
        binder.bind(
            FetchTaskUsecase,  # type: ignore[type-abstract]
            get_default_fetch_task_usecase,
        )
        binder.bind(
            InitTaskDirUsecase,  # type: ignore[type-abstract]
            get_default_init_task_dir_usecase,
        )

    def resolve(self, cls: Type[T]) -> T:
        """Class のインスタンスを生成する."""
        return self._injector.get(cls)
