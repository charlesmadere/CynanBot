from .stubSoundPlayerManager import StubSoundPlayerManager
from ..soundPlayerManagerInterface import SoundPlayerManagerInterface
from ..soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface


class StubSoundPlayerManagerProvider(SoundPlayerManagerProviderInterface):

    def constructSoundPlayerManagerInstance(self) -> SoundPlayerManagerInterface:
        return StubSoundPlayerManager()
