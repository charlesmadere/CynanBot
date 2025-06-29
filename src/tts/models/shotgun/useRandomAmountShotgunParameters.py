from dataclasses import dataclass

from .shotgunProviderUseParameters import ShotgunProviderUseParameters


@dataclass(frozen = True)
class UseExactAmountShotgunParameters(ShotgunProviderUseParameters):
    maxAmount: int
    minAmount: int
