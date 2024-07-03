from .immediateSoundPlayerManagerInterface import ImmediateSoundPlayerManagerInterface
from .soundAlert import SoundAlert
from .soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..timber.timberInterface import TimberInterface


class ImmediateSoundPlayerManager(ImmediateSoundPlayerManagerInterface):

    def __init__(
        self,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        timber: TimberInterface
    ):
        if not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__soundPlayerManagerProvider: SoundPlayerManagerProviderInterface = soundPlayerManagerProvider
        self.__timber: TimberInterface = timber

    async def playSoundAlert(self, alert: SoundAlert) -> bool:
        if not isinstance(alert, SoundAlert):
            raise TypeError(f'alert argument is malformed: \"{alert}\"')

        soundPlayerManager = self.__soundPlayerManagerProvider.constructSoundPlayerManagerInstance()
        return await soundPlayerManager.playSoundAlert(alert)

    async def playSoundFile(self, filePath: str | None) -> bool:
        if filePath is not None and not isinstance(filePath, str):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')

        soundPlayerManager = self.__soundPlayerManagerProvider.constructSoundPlayerManagerInstance()
        return await soundPlayerManager.playSoundFile(filePath)
