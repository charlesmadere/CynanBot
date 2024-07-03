from .soundAlertCheerActionHelperInterface import \
    SoundAlertCheerActionHelperInterface
from ..cheerAction import CheerAction
from ..cheerActionBitRequirement import CheerActionBitRequirement
from ..cheerActionType import CheerActionType
from ...misc import utils as utils
from ...soundPlayerManager.immediateSoundPlayerManagerInterface import \
    ImmediateSoundPlayerManagerInterface
from ...soundPlayerManager.soundPlayerRandomizerHelperInterface import \
    SoundPlayerRandomizerHelperInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.isLiveOnTwitchRepositoryInterface import \
    IsLiveOnTwitchRepositoryInterface
from ...users.userInterface import UserInterface


class SoundAlertCheerActionHelper(SoundAlertCheerActionHelperInterface):

    def __init__(
        self,
        immediateSoundPlayerManager: ImmediateSoundPlayerManagerInterface,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface,
        soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface,
        timber: TimberInterface
    ):
        if not isinstance(immediateSoundPlayerManager, ImmediateSoundPlayerManagerInterface):
            raise TypeError(f'immediateSoundPlayerManager argument is malformed: \"{immediateSoundPlayerManager}\"')
        elif not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise TypeError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
        elif not isinstance(soundPlayerRandomizerHelper, SoundPlayerRandomizerHelperInterface):
            raise TypeError(f'soundPlayerRandomizerHelper argument is malformed: \"{soundPlayerRandomizerHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__immediateSoundPlayerManager: ImmediateSoundPlayerManagerInterface = immediateSoundPlayerManager
        self.__isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface = isLiveOnTwitchRepository
        self.__soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface = soundPlayerRandomizerHelper
        self.__timber: TimberInterface = timber

    async def handleSoundAlertCheerAction(
        self,
        bits: int,
        actions: list[CheerAction],
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 0 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not isinstance(actions, list):
            raise TypeError(f'actions argument is malformed: \"{actions}\"')
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

        if not user.areSoundAlertsEnabled():
            return False

        soundAlertActions: list[CheerAction] = list()
        for action in actions:
            if action.actionType is CheerActionType.SOUND_ALERT:
                soundAlertActions.append(action)

        if len(soundAlertActions) == 0:
            return False

        soundAlertActions.sort(key = lambda action: action.amount, reverse = True)
        soundAlertAction: CheerAction | None = None

        for action in soundAlertActions:
            if action.bitRequirement is CheerActionBitRequirement.EXACT and bits == action.amount:
                soundAlertAction = action
                break

        if soundAlertAction is None:
            for action in soundAlertActions:
                if action.bitRequirement is CheerActionBitRequirement.GREATER_THAN_OR_EQUAL_TO and bits >= action.amount:
                    soundAlertAction = action
                    break

        if soundAlertAction is None:
            return False
        elif not utils.isValidStr(soundAlertAction.tag):
            self.__timber.log('SoundAlertCheerActionHelper', f'Encountered a valid sound alert CheerAction instance but it has no tag value, this should be impossible ({user.getHandle()=}) ({soundAlertAction=})')
            return False
        elif not await self.__isLiveOnTwitchRepository.isLive(broadcasterUserId):
            self.__timber.log('SoundAlertCheerActionHelper', f'Received a sound alert CheerAction but the streamer is not currently live ({user.getHandle()=}) ({soundAlertAction=})')
            return False

        return await self.__playSoundAlert(
            bits = bits,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            tag = soundAlertAction.tag,
            twitchChannelId = broadcasterUserId,
            user = user
        )

    async def __playSoundAlert(
        self,
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        tag: str,
        twitchChannelId: str,
        user: UserInterface
    ) -> bool:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(tag):
            raise TypeError(f'tag argument is malformed: \"{tag}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if not user.areSoundAlertsEnabled():
            return False

        soundAlertPath = await self.__soundPlayerRandomizerHelper.chooseRandomFromDirectorySoundAlert(
            directoryPath = tag
        )

        if not utils.isValidStr(soundAlertPath):
            return False

        return await self.__immediateSoundPlayerManager.playSoundFile(
            filePath = soundAlertPath
        )
