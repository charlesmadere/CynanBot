from dataclasses import dataclass

from .shotgunProviderUseParameters import ShotgunProviderUseParameters


@dataclass(frozen = True)
class UseRandomAmountShotgunParameters(ShotgunProviderUseParameters):
    maxAmount: int
    minAmount: int
