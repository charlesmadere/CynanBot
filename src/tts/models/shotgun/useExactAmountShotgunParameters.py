from dataclasses import dataclass

from .shotgunProviderUseParameters import ShotgunProviderUseParameters


@dataclass(frozen = True, slots = True)
class UseExactAmountShotgunParameters(ShotgunProviderUseParameters):
    amount: int
