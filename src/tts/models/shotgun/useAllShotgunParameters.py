from dataclasses import dataclass

from .shotgunProviderUseParameters import ShotgunProviderUseParameters


@dataclass(frozen = True, slots = True)
class UseAllShotgunParameters(ShotgunProviderUseParameters):

    pass
