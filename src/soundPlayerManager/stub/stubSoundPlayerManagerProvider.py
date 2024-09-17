from .stubSoundPlayerManager import StubSoundPlayerManager
from ..soundPlayerManagerInterface import SoundPlayerManagerInterface
from ..soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface


class StubSoundPlayerManagerProvider(SoundPlayerManagerProviderInterface):

    async def constructSoundPlayerManagerInstance(self) -> SoundPlayerManagerInterface:
        return StubSoundPlayerManager()
