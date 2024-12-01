from collections.abc import Collection

from .soundAlertCheerActionHelperInterface import SoundAlertCheerActionHelperInterface
from ..absCheerAction import AbsCheerAction
from ..soundAlertCheerAction import SoundAlertCheerAction
from ...misc import utils as utils
from ...soundPlayerManager.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManager.soundPlayerRandomizerHelperInterface import SoundPlayerRandomizerHelperInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from ...users.userInterface import UserInterface


class SoundAlertCheerActionHelper(SoundAlertCheerActionHelperInterface):

    def __init__(
        self,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface,
        timber: TimberInterface
    ):
        if not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise TypeError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(soundPlayerRandomizerHelper, SoundPlayerRandomizerHelperInterface):
            raise TypeError(f'soundPlayerRandomizerHelper argument is malformed: \"{soundPlayerRandomizerHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface = isLiveOnTwitchRepository
        self.__soundPlayerManagerProvider: SoundPlayerManagerProviderInterface = soundPlayerManagerProvider
        self.__soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface = soundPlayerRandomizerHelper
        self.__timber: TimberInterface = timber

    async def handleSoundAlertCheerAction(
        self,
        actions: Collection[AbsCheerAction],
        bits: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        if not isinstance(actions, Collection):
            raise TypeError(f'actions argument is malformed: \"{actions}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(moderatorTwitchAccessToken):
            raise TypeError(f'moderatorTwitchAccessToken argument is malformed: \"{moderatorTwitchAccessToken}\"')
        elif not utils.isValidStr(moderatorUserId):
            raise TypeError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise TypeError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if not user.areSoundAlertsEnabled:
            return False

        soundAlertAction: SoundAlertCheerAction | None = None

        for action in actions:
            if isinstance(action, SoundAlertCheerAction) and action.isEnabled and action.bits == bits:
                soundAlertAction = action
                break

        if soundAlertAction is None:
            return False

        return await self.__playSoundAlert(
            action = soundAlertAction,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            twitchChannelId = broadcasterUserId,
            user = user
        )

    async def __playSoundAlert(
        self,
        action: SoundAlertCheerAction,
        cheerUserId: str,
        cheerUserName: str,
        twitchChannelId: str,
        user: UserInterface
    ) -> bool:
        if not isinstance(action, SoundAlertCheerAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if not await self.__isLiveOnTwitchRepository.isLive(twitchChannelId):
            self.__timber.log('SoundAlertCheerActionHelper', f'Received a sound alert CheerAction but the streamer is not currently live ({user.getHandle()=}) ({action=})')
            return False

        soundAlertPath = await self.__soundPlayerRandomizerHelper.chooseRandomFromDirectorySoundAlert(
            directoryPath = action.directory
        )

        if not utils.isValidStr(soundAlertPath):
            return False

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewSoundPlayerManagerInstance()

        return await soundPlayerManager.playSoundFile(
            filePath = soundAlertPath
        ) is not None
