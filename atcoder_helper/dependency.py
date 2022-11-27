"""依存性注入モジュール."""

import os
from typing import Final
from typing import Type
from typing import TypeVar

from injector import Binder
from injector import Injector

import atcoder_helper
from atcoder_helper.adapter.infrastructure.atcoder_helper_config_repo import (
    ConfigRepositoryImpl,
)
from atcoder_helper.adapter.infrastructure.atcoder_logged_in_session_repo import (
    AtCoderLoggedInSessionRepositoryImpl,
)
from atcoder_helper.adapter.infrastructure.atcoder_test_case_repo import (
    AtCoderTestCaseRepositoryImpl,
)
from atcoder_helper.adapter.infrastructure.local_test_case_repo import (
    LocalTestCaseRepositoryImpl,
)
from atcoder_helper.adapter.infrastructure.logged_in_session_repo import (
    LoggedInSessionRepositoryImpl,
)
from atcoder_helper.adapter.infrastructure.login_status_repo import LoginStatusRepoImpl
from atcoder_helper.adapter.infrastructure.task_config_repo import (
    TaskConfigRepositoryImpl,
)
from atcoder_helper.application.interactors.atcoder_helper_config import (
    AtCoderHelperConfigInteractor,
)
from atcoder_helper.application.interactors.auth import AuthInteractor
from atcoder_helper.application.interactors.execute_test import ControllerBuilder
from atcoder_helper.application.interactors.execute_test import ControllerBuilderImpl
from atcoder_helper.application.interactors.execute_test import ExecuteTestInteractor
from atcoder_helper.application.interactors.fetch_task import FetchTaskInteractor
from atcoder_helper.application.interactors.init_task import InitTaskDirInteractor
from atcoder_helper.application.interactors.util import (
    get_atcoder_helper_config_filepath,
)
from atcoder_helper.application.repositories.atcoder_helper_config_repo import (
    ConfigRepository,
)
from atcoder_helper.application.repositories.atcoder_logged_in_session_repo import (
    AtCoderLoggedInSessionRepository,
)
from atcoder_helper.application.repositories.atcoder_test_case_repo import (
    AtCoderTestCaseRepository,
)
from atcoder_helper.application.repositories.local_test_case_repo import (
    LocalTestCaseRepository,
)
from atcoder_helper.application.repositories.logged_in_session_repo import (
    LoggedInSessionRepository,
)
from atcoder_helper.application.repositories.login_status_repo import LoginStatusRepo
from atcoder_helper.application.repositories.task_config_repo import (
    TaskConfigRepository,
)
from atcoder_helper.application.usecases.atcoder_helper_config import (
    AtCoderHelperConfigUsecase,
)
from atcoder_helper.application.usecases.auth import AuthUsecase
from atcoder_helper.application.usecases.execute_test import ExecuteTestUsecase
from atcoder_helper.application.usecases.fetch_task import FetchTaskUsecase
from atcoder_helper.application.usecases.init_task import InitTaskDirUsecase

T = TypeVar("T")


testcase_filename = "testcases.yaml"
default_session_file: Final[str] = os.path.join(
    os.path.expanduser("~"), ".atcoder_helper", "session", "session_dump.pkl"
)
default_task_config_filename = ".atcoder_helper_task_config.yaml"
default_config_filename = os.path.join(
    atcoder_helper.__path__[0],
    "default_configs",
    "default_config.yaml",
)


class Dependency:
    """依存性の注入を管理する."""

    _injector: Injector

    def __init__(self) -> None:
        """init."""
        self._injector = Injector(self.__class__.config)

    @staticmethod
    def config(binder: Binder) -> None:
        """依存性の注入を行う."""
        binder.bind(AuthUsecase, AuthInteractor)  # type: ignore[type-abstract]

        binder.bind(
            AtCoderHelperConfigUsecase,  # type: ignore[type-abstract]
            lambda: AtCoderHelperConfigInteractor(
                config_repo=ConfigRepositoryImpl(get_atcoder_helper_config_filepath()),
                default_config_repo=ConfigRepositoryImpl(default_config_filename),
            ),
        )
        binder.bind(
            ExecuteTestUsecase,  # type: ignore[type-abstract]
            ExecuteTestInteractor,
        )
        binder.bind(
            FetchTaskUsecase,  # type: ignore[type-abstract]
            FetchTaskInteractor,
        )
        binder.bind(
            InitTaskDirUsecase,  # type: ignore[type-abstract]
            InitTaskDirInteractor,
        )

        binder.bind(
            ControllerBuilder, ControllerBuilderImpl  # type: ignore[type-abstract]
        )

        binder.bind(
            ConfigRepository,  # type: ignore[type-abstract]
            lambda: ConfigRepositoryImpl(get_atcoder_helper_config_filepath()),
        )
        binder.bind(
            AtCoderLoggedInSessionRepository,  # type: ignore[type-abstract]
            AtCoderLoggedInSessionRepositoryImpl,
        )
        binder.bind(
            AtCoderTestCaseRepository,  # type: ignore[type-abstract]
            AtCoderTestCaseRepositoryImpl,
        )
        binder.bind(
            LocalTestCaseRepository,  # type: ignore[type-abstract]
            lambda: LocalTestCaseRepositoryImpl(testcase_filename),
        )

        binder.bind(
            LoggedInSessionRepository,  # type: ignore[type-abstract]
            lambda: LoggedInSessionRepositoryImpl(default_session_file),
        )
        binder.bind(LoginStatusRepo, LoginStatusRepoImpl)  # type: ignore[type-abstract]

        binder.bind(
            TaskConfigRepository,  # type: ignore[type-abstract]
            lambda: TaskConfigRepositoryImpl(default_task_config_filename),
        )

    def resolve(self, cls: Type[T]) -> T:
        """Class のインスタンスを生成する."""
        return self._injector.get(cls)
