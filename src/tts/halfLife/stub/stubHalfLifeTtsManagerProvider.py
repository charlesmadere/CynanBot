from ..halfLifeTtsManagerInterface import HalfLifeTtsManagerInterface
from ..halfLifeTtsManagerProviderInterface import HalfLifeTtsManagerProviderInterface


class StubHalfLifeTtsManagerProvider(HalfLifeTtsManagerProviderInterface):

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True,
    ) -> HalfLifeTtsManagerInterface | None:
        return None

    def getSharedInstance(self) -> HalfLifeTtsManagerInterface | None:
        return None
