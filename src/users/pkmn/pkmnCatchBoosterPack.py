from dataclasses import dataclass

from .pkmnCatchType import PkmnCatchType


@dataclass(frozen = True)
class PkmnCatchBoosterPack:
    catchType: PkmnCatchType | None
    rewardId: str
