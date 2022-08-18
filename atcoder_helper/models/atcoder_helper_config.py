"""AtcoderHelperConfigを定義する."""

import os
from typing import List
from typing import Optional
from typing import TypedDict

from pydantic import BaseModel
from typing_extensions import NotRequired

import atcoder_helper


class LanguageConfigDict(TypedDict):
    """LanguageConfigのdict版."""

    name: str
    template_dir: NotRequired[str]
    use_default_template: bool
    build: List[str]
    run: List[str]


class LanguageConfig(BaseModel):
    """言語ごとの設定を保持する."""

    name: str
    template_dir: Optional[str]
    use_default_template: Optional[bool]
    build: List[str]
    run: List[str]

    @classmethod
    def from_dict(cls, language_dict: LanguageConfigDict) -> "LanguageConfig":
        """辞書型からLanguageConfig型に変換する."""
        return LanguageConfig(
            name=language_dict["name"],
            template_dir=language_dict.get("template_dir"),
            use_default_template=bool(language_dict.get("use_default_template")),
            build=language_dict["build"],
            run=language_dict["run"],
        )

    def to_dict(self) -> LanguageConfigDict:
        """LanguageConfig型から辞書型へ変換する."""
        if self.template_dir is None:
            return {
                "name": self.name,
                "use_default_template": (bool)(self.use_default_template),
                "build": self.build,
                "run": self.run,
            }
        else:
            return {
                "name": self.name,
                "template_dir": self.template_dir,
                "use_default_template": (bool)(self.use_default_template),
                "build": self.build,
                "run": self.run,
            }

    @property
    def resolved_template_dir(self) -> Optional[str]:
        """実際に使用するtemplate_directory."""
        if self.use_default_template:
            return os.path.join(
                atcoder_helper.__path__[0],
                "default_configs",
                "templates",
                self.name,
            )
        else:
            return self.template_dir


class AtCoderHelperConfigDict(TypedDict):
    """AtcCoderHelperConfig の　辞書版."""

    languages: List[LanguageConfigDict]
    default_language: str


class AtCoderHelperConfig(BaseModel):
    """atcoder_helper アプリ全体の設定を保持する."""

    languages: dict[str, LanguageConfig]
    default_language: str

    @classmethod
    def from_dict(cls, config_dict: AtCoderHelperConfigDict) -> "AtCoderHelperConfig":
        """辞書型からAtCoderHelperConfig型に変換する."""
        return AtCoderHelperConfig(
            languages={
                language["name"]: LanguageConfig.from_dict(language)
                for language in config_dict["languages"]
            },
            default_language=config_dict["default_language"],
        )

    def to_dict(self) -> AtCoderHelperConfigDict:
        """AtCoderHelperConfig型から辞書型へ変換する."""
        return {
            "languages": [language.to_dict() for language in self.languages.values()],
            "default_language": self.default_language,
        }

    @property
    def default_language_config(self) -> LanguageConfig:
        """デフォルトの言語設定."""
        return self.languages[self.default_language]
