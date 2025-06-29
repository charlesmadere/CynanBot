from ..decTalkTtsManagerInterface import DecTalkTtsManagerInterface
from ..decTalkTtsManagerProviderInterface import DecTalkTtsManagerProviderInterface


class StubDecTalkTtsManagerProvider(DecTalkTtsManagerProviderInterface):

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> DecTalkTtsManagerInterface | None:
        return None

    def getSharedInstance(self) -> DecTalkTtsManagerInterface | None:
        return None
