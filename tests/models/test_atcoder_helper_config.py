"""atcoder_helper_configのテスト."""

import os
from typing import Optional

import pytest

import atcoder_helper
from atcoder_helper.models.atcoder_helper_config import LanguageConfig


@pytest.mark.parametrize(
    argnames=("conf", "template_dir"),
    argvalues=[
        [LanguageConfig(name="foo", build=[], run=[]), None],
        [
            LanguageConfig(name="foo", template_dir="bar", build=[], run=[]),
            "bar",
        ],
        [
            LanguageConfig(name="foo", use_default_template=True, build=[], run=[]),
            os.path.join(
                atcoder_helper.__path__[0], "default_configs", "templates", "foo"
            ),
        ],
    ],
    ids=["指定なし", "指定あり", "default templateを使う"],
)
def test_language_config_resolved_template_dir(
    conf: LanguageConfig, template_dir: Optional[str]
) -> None:
    """template_dirのテスト."""
    assert conf.resolved_template_dir == template_dir


@pytest.mark.skip(reason="自明なので後で書く")
def test_atcoder_helper_config_dict() -> None:
    """dict()のテスト."""
    pass
