from ..soundAlert import SoundAlert
from ..soundPlayerRandomizerHelperInterface import SoundPlayerRandomizerHelperInterface


class StubSoundPlayerRandomizerHelper(SoundPlayerRandomizerHelperInterface):

    async def chooseRandomFromDirectorySoundAlert(self, directoryPath: str | None) -> str | None:
        # this method is intentionally empty
        return None

    async def chooseRandomSoundAlert(self) -> SoundAlert | None:
        # this method is intentionally empty
        return None

    async def clearCaches(self):
        # this method is intentionally empty
        pass
