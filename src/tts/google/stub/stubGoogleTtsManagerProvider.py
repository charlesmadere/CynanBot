from ..googleTtsManagerInterface import GoogleTtsManagerInterface
from ..googleTtsManagerProviderInterface import GoogleTtsManagerProviderInterface


class StubGoogleTtsManagerProvider(GoogleTtsManagerProviderInterface):

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> GoogleTtsManagerInterface | None:
        return None

    def getSharedInstance(self) -> GoogleTtsManagerInterface | None:
        return None
