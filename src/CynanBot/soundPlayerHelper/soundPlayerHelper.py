import CynanBot.misc.utils as utils
from CynanBot.soundPlayerHelper.soundAlert import SoundAlert
from CynanBot.soundPlayerHelper.soundPlayerHelperInterface import \
    SoundPlayerHelperInterface
from CynanBot.soundPlayerHelper.soundPlayerInterface import \
    SoundPlayerInterface
from CynanBot.soundPlayerHelper.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface


class SoundPlayerHelper(SoundPlayerHelperInterface):

    def __init__(
        self,
        soundPlayer: SoundPlayerInterface,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface
    ):
        if not isinstance(soundPlayer, SoundPlayerInterface):
            raise TypeError(f'soundPlayer argument is malformed: \"{soundPlayer}\"')
        elif not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__soundPlayer: SoundPlayerInterface = soundPlayer
        self.__soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = soundPlayerSettingsRepository
        self.__timber: TimberInterface = timber

    async def playSoundAlert(self, soundAlert: SoundAlert):
        if not isinstance(soundAlert, SoundAlert):
            raise TypeError(f'soundAlert argument is malformed: \"{soundAlert}\"')

        if not await self.__soundPlayerSettingsRepository.isEnabled():
            return

        filePath = await self.__soundPlayerSettingsRepository.getFilePathFor(soundAlert)

        if not utils.isValidStr(filePath):
            self.__timber.log('SoundPlayerHelper', f'No file path available for sound alert \"{soundAlert}\" ({filePath=})')
            return

        soundReference = await self.__soundPlayer.load(filePath)
        await soundReference.play()
