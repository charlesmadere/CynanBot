from ..soundAlert import SoundAlert
from ..soundPlayerRandomizerHelperInterface import SoundPlayerRandomizerHelperInterface


class StubSoundPlayerRandomizerHelper(SoundPlayerRandomizerHelperInterface):

    async def chooseRandomFromDirectorySoundAlert(self, directoryPath: str | None) -> str | None:
        return None

    async def chooseRandomSoundAlert(self) -> SoundAlert | None:
        return None

    async def clearCaches(self):
        pass
