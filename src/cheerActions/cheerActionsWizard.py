from datetime import timedelta

from .cheerActionType import CheerActionType
from .cheerActionsWizardInterface import CheerActionsWizardInterface
from .wizards.absWizard import AbsWizard
from .wizards.soundAlertWizard import SoundAlertWizard
from .wizards.timeoutWizard import TimeoutWizard
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..timber.timberInterface import TimberInterface


class CheerActionsWizard(CheerActionsWizardInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timePerStep: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timePerStep, timedelta):
            raise TypeError(f'timePerStep argument is malformed: \"{timePerStep}\"')

        self.__timber: TimberInterface = timber
        self.__wizards: TimedDict[AbsWizard] = TimedDict(timePerStep)

    async def complete(self, twitchChannelId: str):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        del self.__wizards[twitchChannelId]

    async def get(self, twitchChannelId: str) -> AbsWizard | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        return self.__wizards[twitchChannelId]

    async def start(
        self,
        cheerActionType: CheerActionType,
        twitchChannel: str,
        twitchChannelId: str
    ) -> AbsWizard:
        if not isinstance(cheerActionType, CheerActionType):
            raise TypeError(f'cheerActionType argument is malformed: \"{cheerActionType}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        existingWizard = self.__wizards[twitchChannelId]

        if existingWizard is not None:
            self.__timber.log('CheerActionsWizard', f'Starting a new \"{cheerActionType}\" wizard for {twitchChannel}:{twitchChannelId}, which will clobber an existing wizard: \"{existingWizard}\"')

        match cheerActionType:
            case CheerActionType.SOUND_ALERT:
                return await self.__startNewSoundAlertWizard(
                    twitchChannel = twitchChannel,
                    twitchChannelId = twitchChannelId
                )

            case CheerActionType.TIMEOUT:
                return await self.__startNewTimeoutWizard(
                    twitchChannel = twitchChannel,
                    twitchChannelId = twitchChannelId
                )

            case _:
                raise RuntimeError(f'unknown CheerActionType: \"{cheerActionType}\"')

    async def __startNewSoundAlertWizard(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> SoundAlertWizard:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        wizard = SoundAlertWizard(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__wizards[twitchChannelId] = wizard
        self.__timber.log('CheerActionsWizard', f'Started new Sound Alert wizard for {twitchChannel}:{twitchChannelId}')

        return wizard

    async def __startNewTimeoutWizard(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TimeoutWizard:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        wizard = TimeoutWizard(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__wizards[twitchChannelId] = wizard
        self.__timber.log('CheerActionsWizard', f'Started new Timeout wizard for {twitchChannel}:{twitchChannelId}')

        return wizard
