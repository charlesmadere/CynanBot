from dataclasses import dataclass

from .crowdControlInputType import CrowdControlInputType


@dataclass(frozen = True)
class CrowdControlBoosterPack:
    inputType: CrowdControlInputType
    rewardId: str
