"""AtcoderHelperConfigを永続化する層."""

import os
from typing import Protocol
from typing import cast

import yaml

from atcoder_helper.models.atcoder_helper_config import AtCoderHelperConfig
from atcoder_helper.models.atcoder_helper_config import AtCoderHelperConfigDict
from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.errors import WriteError
from atcoder_helper.services.util import get_atcoder_helper_config_filepath


class ConfigRepository(Protocol):
    """AtCoderHelperConfigを永続化するプロトコル."""

    def __init__(self, filename: str):
        """__init__."""

    def read(self) -> AtCoderHelperConfig:
        """読み込みを行う.

        Raises:
            ReadError: 読み込みに失敗した

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


def get_default_config_repository() -> ConfigRepository:
    """ConfigRepositoryの標準実装を返す."""
    return ConfigRepositoryImpl()


class ConfigRepositoryImpl:
    """AtCoderHelperConfigを永続化する層."""

    _filename: str

    def __init__(self, filename: str = get_atcoder_helper_config_filepath()) -> None:
        """__init__."""
        self._filename = filename

    def read(self) -> AtCoderHelperConfig:
        """読み込みを行う.

        Raises:
            ReadError: 読み込みに失敗した

        Returns:
            AtCoderHelperConfig: 読み込まれたAtcoderHelperConfig
        """
        try:
            with open(self._filename, "rt") as file:
                config_dict = cast(
                    AtCoderHelperConfigDict, yaml.safe_load(file)
                )  # TODO(validate)
        except OSError as e:
            raise ReadError(f"cannot read from {self._filename}.") from e

        return AtCoderHelperConfig.from_dict(config_dict)

    def write(self, config: AtCoderHelperConfig) -> None:
        """書き込みを行う.

        Args:
            config (AtCoderHelperConfig): _description_

        Raises:
            WriteError: 書き込みに失敗した
        """
        os.makedirs(name=os.path.dirname(self._filename), exist_ok=True)

        config_dict = config.to_dict()

        try:
            with open(self._filename, "wt") as file:
                yaml.dump(config_dict, file)
        except OSError as e:
            raise WriteError("cannot write to {self._filename}.") from e
