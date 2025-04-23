from typing import Final

from .stubGoogleTtsManager import StubGoogleTtsManager
from ..googleTtsManagerInterface import GoogleTtsManagerInterface
from ..googleTtsManagerProviderInterface import GoogleTtsManagerProviderInterface
from ...models.ttsProvider import TtsProvider


class StubGoogleTtsManagerProvider(GoogleTtsManagerProviderInterface):

    def __init__(self):
        self.__instance: Final[GoogleTtsManagerInterface] = StubGoogleTtsManager()

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> GoogleTtsManagerInterface:
        # this method kinda breaks contract, but it's fine in this case
        return self.__instance

    def getSharedInstance(self) -> GoogleTtsManagerInterface:
        return self.__instance

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.GOOGLE
