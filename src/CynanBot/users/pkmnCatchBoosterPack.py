from dataclasses import dataclass

from CynanBot.users.pkmnCatchType import PkmnCatchType


@dataclass(frozen = True)
class PkmnCatchBoosterPack():
    catchType: PkmnCatchType | None
    rewardId: str
