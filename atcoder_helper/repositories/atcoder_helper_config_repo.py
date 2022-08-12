"""AtcoderHelperConfigを永続化する層."""

import os

import yaml

from atcoder_helper.models.atcoder_helper_config import AtCoderHelperConfig


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
        """
        with open(self._filename) as file:
            config_dict = yaml.safe_load(file)
            return AtCoderHelperConfig.from_dict(config_dict)

    def write(self, config: AtCoderHelperConfig) -> None:
        """書き込みを行う."""
        os.makedirs(name=os.path.dirname(self._filename), exist_ok=True)

        with open(self._filename, "w") as file:
            config_dict = config.to_dict()
            yaml.dump(config_dict, file)
