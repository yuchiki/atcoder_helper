"""AtcoderHelperConfigを永続化する層."""

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
