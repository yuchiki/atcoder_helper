"""utils for repos."""


from typing import Dict
from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V")


def filter_out_none(d: Dict[K, V]) -> Dict[K, V]:
    """辞書から値がNoneのキーを除きます."""
    return {k: v for k, v in d.items() if v is not None}
