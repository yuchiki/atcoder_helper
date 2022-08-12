"""AtcoderHelperConfigを定義する."""

from dataclasses import dataclass
from typing import Any
from typing import List
from typing import Optional


@dataclass
class LanguageConfig:
    """言語ごとの設定を保持する."""

    name: str
    template_dir: Optional[str]
    use_default_template: bool
    build: List[str]
    run: List[str]

    @classmethod
    def from_dict(cls, language_dict: dict[str, Any]) -> "LanguageConfig":
        """辞書型からLanguageConfig型に変換する."""
        return LanguageConfig(
            name=language_dict["name"],
            template_dir=language_dict.get("template_dir"),
            use_default_template=bool(language_dict.get("use_default_template")),
            build=language_dict["build"],
            run=language_dict["run"],
        )


@dataclass
class AtCoderHelperConfig:
    """atcoder_helper アプリ全体の設定を保持する."""

    languages: List[LanguageConfig]
    default_language: str

    @classmethod
    def from_dict(cls, config_dict: dict[str, Any]) -> "AtCoderHelperConfig":
        """辞書型からAtCoderHelperConfig型に変換する."""
        return AtCoderHelperConfig(
            languages=[
                LanguageConfig.from_dict(language)
                for language in config_dict["languages"]
            ],
            default_language=config_dict["default_language"],
        )
