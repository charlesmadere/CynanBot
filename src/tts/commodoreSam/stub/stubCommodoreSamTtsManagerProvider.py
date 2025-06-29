from ..commodoreSamTtsManagerInterface import CommodoreSamTtsManagerInterface
from ..commodoreSamTtsManagerProviderInterface import CommodoreSamTtsManagerProviderInterface


class StubCommodoreSamTtsManagerProvider(CommodoreSamTtsManagerProviderInterface):

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> CommodoreSamTtsManagerInterface | None:
        return None

    def getSharedInstance(self) -> CommodoreSamTtsManagerInterface | None:
        return None
