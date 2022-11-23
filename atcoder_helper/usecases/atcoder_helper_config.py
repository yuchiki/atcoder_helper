"""デフォルト言語を変更する."""


import os
from typing import Dict
from typing import Protocol

import atcoder_helper
from atcoder_helper.entities.atcoder_helper_config import LanguageConfig
from atcoder_helper.infrastructure import errors as repository_errors
from atcoder_helper.infrastructure.atcoder_helper_config_repo import ConfigRepository
from atcoder_helper.infrastructure.atcoder_helper_config_repo import (
    ConfigRepositoryImpl,
)
from atcoder_helper.infrastructure.atcoder_helper_config_repo import (
    get_default_config_repository,
)
from atcoder_helper.usecases.errors import ConfigAccessError
from atcoder_helper.usecases.errors import UndefinedLanguage


class AtCoderHelperConfigUsecase(Protocol):
    """AtCoderHelperConfigを操作する Usecaseのプロトコル."""

    def config_use(self, language: str) -> None:
        """デフォルト言語を変更する.

        Raises:
            UndefinedLanguage: 存在しない言語をデフォルトに設定しようとした
            ConfigAccessError: 通信層のエラー
        """

    def config_default_language(self) -> LanguageConfig:
        """デフォルト言語を取得する.

        Raises:
            ConfigAccerssError: 設定ファイル読み書きのエラー

        Returns:
            LanguageConfig: デフォルト言語
        """

    def config_languages(self) -> Dict[str, LanguageConfig]:
        """使用可能な言語の一覧を取得する.

        Raises:
            ConfigAccessError: 設定ファイルの読み書きの失敗

        Returns:
            Dict[str, LanguageConfig]: 言語名から言語設定をひく辞書
        """

    def init_config(
        self,
    ) -> None:
        """configを初期化するためのusecase.

        Raises:
            ConfigAccessError:
        """


def get_default_atcoder_helper_config_usecase() -> AtCoderHelperConfigUsecase:
    """AtCoderHelperConfigUsecaseの標準実装を返す.

    Returns:
        AtCoderHelperConfigUsecase:
    """
    return AtCoderHelperConfigInteractor(
        config_repo=get_default_config_repository(),
        default_config_repo=ConfigRepositoryImpl(
            os.path.join(
                atcoder_helper.__path__[0], "default_configs", "default_config.yaml"
            )
        ),
    )


class AtCoderHelperConfigInteractor:
    """AtCoderHelperConfigを操作する Usecase."""

    _config_repo: ConfigRepository
    _default_config_repo: ConfigRepository

    def __init__(
        self, config_repo: ConfigRepository, default_config_repo: ConfigRepository
    ):
        """_init_.

        Args:
            config_repo (ConfigRepository, optional): _
            default_config_repo (ConfigRepository, optional): _
        """
        self._config_repo = config_repo
        self._default_config_repo = default_config_repo

    def config_use(self, language: str) -> None:
        """デフォルト言語を変更する.

        Raises:
            UndefinedLanguage: 存在しない言語をデフォルトに設定しようとした
            ConfigAccessError: 通信層のエラー
        """
        try:
            config = self._config_repo.read()
            if language not in config.languages:
                raise UndefinedLanguage(f"言語{language}は設定の中に存在しません。")

            config.default_language = language
            self._config_repo.write(config)
        except (
            repository_errors.WriteError,
            repository_errors.ReadError,
            repository_errors.ParseError,
        ) as e:
            raise ConfigAccessError("設定ファイルの読み書きに失敗しました。") from e

    def config_default_language(self) -> LanguageConfig:
        """デフォルト言語を取得する.

        Raises:
            ConfigAccerssError: 設定ファイル読み書きのエラー

        Returns:
            LanguageConfig: デフォルト言語
        """
        try:
            config = self._config_repo.read()
        except (repository_errors.ReadError, repository_errors.ParseError) as e:
            raise ConfigAccessError("設定ファイルの読み込みに失敗しました") from e

        return config.languages[config.default_language]

    def config_languages(self) -> Dict[str, LanguageConfig]:
        """使用可能な言語の一覧を取得する.

        Raises:
            ConfigAccessError: 設定ファイルの読み書きの失敗

        Returns:
            Dict[str, LanguageConfig]: 言語名から言語設定をひく辞書
        """
        try:
            config = self._config_repo.read()
        except (repository_errors.ReadError, repository_errors.ParseError) as e:
            raise ConfigAccessError("設定ファイルの読み込みに失敗しました") from e

        return config.languages

    def init_config(
        self,
    ) -> None:
        """configを初期化するためのusecase.

        Raises:
            ConfigAccessError:
        """
        try:
            default_atcoder_config = self._default_config_repo.read()
        except (repository_errors.ReadError, repository_errors.ParseError) as e:
            raise ConfigAccessError("デフォルト設定ファイルの読み込みに失敗しました.") from e

        try:
            self._config_repo.write(default_atcoder_config)
        except repository_errors.WriteError as e:
            raise ConfigAccessError("設定ファイルの書き込みに失敗しました.") from e
