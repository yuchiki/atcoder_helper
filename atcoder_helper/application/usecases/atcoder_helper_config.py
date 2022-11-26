"""デフォルト言語を変更する."""


from typing import Dict
from typing import Protocol

from atcoder_helper.entities.atcoder_helper_config import LanguageConfig


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
