"""デフォルト言語を変更する."""


from typing import Dict

from injector import inject

from atcoder_helper.application.repositories import errors as repository_errors
from atcoder_helper.application.repositories.atcoder_helper_config_repo import (
    ConfigRepository,
)
from atcoder_helper.application.usecases.errors import ConfigAccessError
from atcoder_helper.application.usecases.errors import UndefinedLanguage
from atcoder_helper.entities.atcoder_helper_config import LanguageConfig


class AtCoderHelperConfigInteractor:
    """AtCoderHelperConfigを操作する Usecase."""

    _config_repo: ConfigRepository
    _default_config_repo: ConfigRepository

    @inject
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
