from dataclasses import dataclass
from typing import Any

from .userJsonConstant import UserJsonConstant


@dataclass(frozen = True)
class ModifyUserValueResult:
    newValue: Any
    oldValue: Any
    handle: str
    jsonConstant: UserJsonConstant
