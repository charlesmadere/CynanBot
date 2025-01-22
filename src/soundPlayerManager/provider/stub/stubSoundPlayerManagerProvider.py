from ..soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...stub.stubSoundPlayerManager import StubSoundPlayerManager


class StubSoundPlayerManagerProvider(SoundPlayerManagerProviderInterface):

    def __init__(self):
        self.__instance: SoundPlayerManagerInterface = StubSoundPlayerManager()

    def constructNewSoundPlayerManagerInstance(self) -> SoundPlayerManagerInterface:
        # this method kinda breaks contract, but it's fine in this case
        return self.__instance

    def getSharedSoundPlayerManagerInstance(self) -> SoundPlayerManagerInterface:
        return self.__instance
