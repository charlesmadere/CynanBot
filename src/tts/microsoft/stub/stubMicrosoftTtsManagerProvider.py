from ..microsoftTtsManagerInterface import MicrosoftTtsManagerInterface
from ..microsoftTtsManagerProviderInterface import MicrosoftTtsManagerProviderInterface


class StubMicrosoftTtsManagerProvider(MicrosoftTtsManagerProviderInterface):

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> MicrosoftTtsManagerInterface | None:
        return None

    def getSharedInstance(self) -> MicrosoftTtsManagerInterface | None:
        return None
