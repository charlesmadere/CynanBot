from typing import Final

from frozendict import frozendict

from .soundAlertCheerAction import SoundAlertCheerAction
from .soundAlertCheerActionHelperInterface import SoundAlertCheerActionHelperInterface
from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManager.randomizerHelper.soundPlayerRandomizerHelperInterface import \
    SoundPlayerRandomizerHelperInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.isLive.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from ...users.userInterface import UserInterface


class SoundAlertCheerActionHelper(SoundAlertCheerActionHelperInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface,
        timber: TimberInterface,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise TypeError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(soundPlayerRandomizerHelper, SoundPlayerRandomizerHelperInterface):
            raise TypeError(f'soundPlayerRandomizerHelper argument is malformed: \"{soundPlayerRandomizerHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__isLiveOnTwitchRepository: Final[IsLiveOnTwitchRepositoryInterface] = isLiveOnTwitchRepository
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__soundPlayerRandomizerHelper: Final[SoundPlayerRandomizerHelperInterface] = soundPlayerRandomizerHelper
        self.__timber: Final[TimberInterface] = timber

    async def __checkStreamStatusRequirement(self, action: AbsCheerAction) -> bool:
        streamStatusRequirement = action.getStreamStatusRequirement()

        if streamStatusRequirement is CheerActionStreamStatusRequirement.ANY:
            return True

        isLive = await self.__isLiveOnTwitchRepository.isLive(
            twitchChannelId = action.getTwitchChannelId(),
        )

        match streamStatusRequirement:
            case CheerActionStreamStatusRequirement.ONLINE: return isLive
            case CheerActionStreamStatusRequirement.OFFLINE: return not isLive
            case _: raise ValueError(f'Encountered unknown CheerActionStreamStatusRequirement value: \"{streamStatusRequirement}\"')

    async def handleSoundAlertCheerAction(
        self,
        actions: frozendict[int, AbsCheerAction],
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str | None,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        twitchChannelId: str,
        userTwitchAccessToken: str,
        user: UserInterface,
    ) -> bool:
        if not isinstance(actions, frozendict):
            raise TypeError(f'actions argument is malformed: \"{actions}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(moderatorTwitchAccessToken):
            raise TypeError(f'moderatorTwitchAccessToken argument is malformed: \"{moderatorTwitchAccessToken}\"')
        elif not utils.isValidStr(moderatorUserId):
            raise TypeError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise TypeError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if not user.areSoundAlertsEnabled:
            return False

        action = actions.get(bits, None)

        if not isinstance(action, SoundAlertCheerAction) or not action.isEnabled:
            return False
        elif not await self.__checkStreamStatusRequirement(action):
            self.__timber.log('SoundAlertCheerActionHelper', f'Received a sound alert CheerAction but the streamer does not have the required stream status ({action=}) ({bits=}) ({cheerUserId=}) ({cheerUserName=}) ({user=})')
            return False

        self.__backgroundTaskHelper.createTask(self.__playSoundAlert(
            action = action,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            user = user,
        ))

        return True

    async def __playSoundAlert(
        self,
        action: SoundAlertCheerAction,
        cheerUserId: str,
        cheerUserName: str,
        user: UserInterface,
    ):
        soundAlertPath = await self.__soundPlayerRandomizerHelper.chooseRandomFromDirectorySoundAlert(
            directoryPath = action.directory,
        )

        if not utils.isValidStr(soundAlertPath):
            return

        self.__timber.log('SoundAlertCheerActionHelper', f'Playing sound alert CheerAction ({soundAlertPath=}) ({action=}) ({cheerUserId=}) ({cheerUserName=}) ({user=})')

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
        await soundPlayerManager.playSoundFile(soundAlertPath)
