from dataclasses import dataclass

from .pkmnCatchType import PkmnCatchType


@dataclass(frozen = True, slots = True)
class PkmnCatchBoosterPack:
    catchType: PkmnCatchType | None
    rewardId: str
