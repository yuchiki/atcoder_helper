"""AtcoderHelperConfigを永続化する層."""

import os
from typing import cast

import yaml

from atcoder_helper.models.atcoder_helper_config import AtCoderHelperConfig
from atcoder_helper.models.atcoder_helper_config import AtCoderHelperConfigDict
from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.errors import WriteError


class AtCoderHelperConfigRepository:
    """AtCoderHelperConfigを永続化する層."""

    _filename: str

    def __init__(self, filename: str) -> None:
        """__init__."""
        self._filename = filename

    def read(self) -> AtCoderHelperConfig:
        """読み込みを行う.

        Returns:
            AtCoderHelperConfig: 読み込まれたAtcoderHelperConfig
        Raises:
            ReadError: 読み込みに失敗した
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
