"""Services共通のutil."""

import os


def get_atcoder_helper_config_filepath() -> str:
    """atcoder_helper_configのパスを決定する."""
    filepath = os.environ.get("ATCODER_HELPER_CONFIG_FILEPATH")
    if filepath:
        return filepath
    else:
        return os.path.join(os.path.expanduser("~"), ".atcoder_helper", "config.yaml")
