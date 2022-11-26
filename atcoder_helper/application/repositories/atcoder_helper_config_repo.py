"""AtcoderHelperConfigを永続化する層."""

from typing import Protocol

from atcoder_helper.entities.atcoder_helper_config import AtCoderHelperConfig


class ConfigRepository(Protocol):
    """AtCoderHelperConfigを永続化するプロトコル."""

    def __init__(self, filename: str):
        """__init__."""

    def read(self) -> AtCoderHelperConfig:
        """読み込みを行う.

        Raises:
            ReadError: 読み込みに失敗した
            ParseError: パースに失敗した

        Returns:
            AtCoderHelperConfig: 読み込まれたAtcoderHelperConfig
        """

    def write(self, config: AtCoderHelperConfig) -> None:
        """書き込みを行う.

        Args:
            config (AtCoderHelperConfig): _description_

        Raises:
            WriteError: 書き込みに失敗した
        """
