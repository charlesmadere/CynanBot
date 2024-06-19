import CynanBot.misc.utils as utils
from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.soundPlayerManager.soundPlayerManagerProviderInterface import \
    SoundPlayerManagerProviderInterface
from CynanBot.streamAlertsManager.immediateStreamAlertsManagerInterface import \
    ImmediateStreamAlertsManagerInterface
from CynanBot.timber.timberInterface import TimberInterface


class ImmediateStreamAlertsManager(ImmediateStreamAlertsManagerInterface):

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

    async def playSoundAlert(self, alert: SoundAlert):
        if not isinstance(alert, SoundAlert):
            raise TypeError(f'alert argument is malformed: \"{alert}\"')

        soundPlayerManager = self.__soundPlayerManagerProvider.constructSoundPlayerManagerInstance()
        await soundPlayerManager.playSoundAlert(alert)

    async def playSoundFile(self, filePath: str):
        if not utils.isValidStr(filePath):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')

        soundPlayerManager = self.__soundPlayerManagerProvider.constructSoundPlayerManagerInstance()
        await soundPlayerManager.playSoundFile(filePath)