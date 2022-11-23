"""AtcoderHelperConfigを定義する."""

import os
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel

import atcoder_helper


class LanguageConfig(BaseModel):
    """言語ごとの設定を保持する."""

    name: str
    template_dir: Optional[str]
    use_default_template: Optional[bool]
    build: List[str]
    run: List[str]

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


class AtCoderHelperConfig(BaseModel):
    """atcoder_helper アプリ全体の設定を保持する."""

    languages: dict[str, LanguageConfig]
    default_language: str

    @property
    def default_language_config(self) -> LanguageConfig:
        """デフォルトの言語設定."""
        return self.languages[self.default_language]

    def dict(self, **_: Any) -> Dict[str, Any]:
        """辞書に変換."""
        return {
            "languages": [
                language_config.dict(exclude_none=True)
                for language_config in self.languages.values()
            ],
            "default_language": self.default_language,
        }
