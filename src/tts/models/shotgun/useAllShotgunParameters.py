from dataclasses import dataclass

from .shotgunProviderUseParameters import ShotgunProviderUseParameters


@dataclass(frozen = True)
class UseAllShotgunParameters(ShotgunProviderUseParameters):

    pass
