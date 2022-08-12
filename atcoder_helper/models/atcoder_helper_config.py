"""AtcoderHelperConfigを定義する."""

import os
from dataclasses import dataclass
from typing import Any
from typing import List
from typing import Optional

import atcoder_helper


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

    def to_dict(self) -> dict[str, Any]:
        """LanguageConfig型から辞書型へ変換する."""
        if self.template_dir is None:
            return {
                "name": self.name,
                "use_default_template": self.use_default_template,
                "build": self.build,
                "run": self.run,
            }
        else:
            return {
                "name": self.name,
                "template_dir": self.template_dir,
                "use_default_template": self.use_default_template,
                "build": self.build,
                "run": self.run,
            }

    @property
    def resolved_template_dir(self) -> Optional[str]:
        """実際に使用するtemplate_directory."""
        if self.use_default_template:
            return os.path.join(
                atcoder_helper.__path__[0],
                "sample_configs",
                ".atcoder_helper",
                "templates",
                self.name,
            )
        else:
            return self.template_dir


@dataclass
class AtCoderHelperConfig:
    """atcoder_helper アプリ全体の設定を保持する."""

    languages: dict[str, LanguageConfig]
    default_language: str

    @classmethod
    def from_dict(cls, config_dict: dict[str, Any]) -> "AtCoderHelperConfig":
        """辞書型からAtCoderHelperConfig型に変換する."""
        return AtCoderHelperConfig(
            languages={
                language["name"]: LanguageConfig.from_dict(language)
                for language in config_dict["languages"]
            },
            default_language=config_dict["default_language"],
        )

    def to_dict(self) -> dict[str, Any]:
        """AtCoderHelperConfig型から辞書型へ変換する."""
        return {
            "languages": [language.to_dict() for language in self.languages.values()],
            "default_language": self.default_language,
        }

    @property
    def default_language_config(self) -> LanguageConfig:
        """デフォルトの言語設定."""
        return self.languages[self.default_language]


default_atcoder_config = AtCoderHelperConfig(
    languages={
        "cpp": LanguageConfig(
            name="cpp",
            template_dir=None,
            use_default_template=True,
            build=["g++", "-o", "main", "main.cpp"],
            run=["./main"],
        ),
        "python": LanguageConfig(
            name="python",
            template_dir=None,
            use_default_template=True,
            build=[],
            run=["python main.py"],
        ),
    },
    default_language="cpp",
)
