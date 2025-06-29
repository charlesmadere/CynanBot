from ..shotgunTtsManagerInterface import ShotgunTtsManagerInterface
from ..shotgunTtsManagerProviderInterface import ShotgunTtsManagerProviderInterface


class StubShotgunTtsManagerProvider(ShotgunTtsManagerProviderInterface):

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> ShotgunTtsManagerInterface | None:
        return None

    def getSharedInstance(self) -> ShotgunTtsManagerInterface | None:
        return None
