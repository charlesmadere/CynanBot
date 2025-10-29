from datetime import timedelta

from .cheerActionType import CheerActionType
from .cheerActionsWizardInterface import CheerActionsWizardInterface
from .wizards.absWizard import AbsWizard
from .wizards.airStrike.airStrikeWizard import AirStrikeWizard
from .wizards.beanChance.beanChanceWizard import BeanChanceWizard
from .wizards.crowdControl.crowdControlWizard import CrowdControlWizard
from .wizards.gameShuffle.gameShuffleWizard import GameShuffleWizard
from .wizards.itemUse.itemUseWizard import ItemUseWizard
from .wizards.soundAlert.soundAlertWizard import SoundAlertWizard
from .wizards.timeout.timeoutWizard import TimeoutWizard
from .wizards.voicemail.voicemailWizard import VoicemailWizard
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..timber.timberInterface import TimberInterface


class CheerActionsWizard(CheerActionsWizardInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timePerStep: timedelta = timedelta(minutes = 1),
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
        twitchChannelId: str,
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
            case CheerActionType.ADGE:
                raise RuntimeError('Not implemented')

            case CheerActionType.AIR_STRIKE:
                return await self.__startNewAirStrikeWizard(
                    twitchChannel = twitchChannel,
                    twitchChannelId = twitchChannelId,
                )

            case CheerActionType.BEAN_CHANCE:
                return await self.__startNewBeanChanceWizard(
                    twitchChannel = twitchChannel,
                    twitchChannelId = twitchChannelId,
                )

            case CheerActionType.CROWD_CONTROL:
                return await self.__startNewCrowdControlWizard(
                    twitchChannel = twitchChannel,
                    twitchChannelId = twitchChannelId,
                )

            case CheerActionType.GAME_SHUFFLE:
                return await self.__startNewGameShuffleWizard(
                    twitchChannel = twitchChannel,
                    twitchChannelId = twitchChannelId,
                )

            case CheerActionType.ITEM_USE:
                return await self.__startNewItemUseWizard(
                    twitchChannel = twitchChannel,
                    twitchChannelId = twitchChannelId,
                )

            case CheerActionType.SOUND_ALERT:
                return await self.__startNewSoundAlertWizard(
                    twitchChannel = twitchChannel,
                    twitchChannelId = twitchChannelId,
                )

            case CheerActionType.TIMEOUT:
                return await self.__startNewTimeoutWizard(
                    twitchChannel = twitchChannel,
                    twitchChannelId = twitchChannelId,
                )

            case CheerActionType.VOICEMAIL:
                return await self.__startNewVoicemailWizard(
                    twitchChannel = twitchChannel,
                    twitchChannelId = twitchChannelId,
                )

            case _:
                raise RuntimeError(f'unknown CheerActionType: \"{cheerActionType}\"')

    async def __startNewAirStrikeWizard(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> AirStrikeWizard:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        wizard = AirStrikeWizard(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        self.__wizards[twitchChannelId] = wizard
        self.__timber.log('CheerActionsWizard', f'Started new Air Strike wizard for {twitchChannel}:{twitchChannelId}')

        return wizard

    async def __startNewBeanChanceWizard(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> BeanChanceWizard:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        wizard = BeanChanceWizard(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        self.__wizards[twitchChannelId] = wizard
        self.__timber.log('CheerActionsWizard', f'Started new Bean Chance wizard for {twitchChannel}:{twitchChannelId}')

        return wizard

    async def __startNewCrowdControlWizard(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> CrowdControlWizard:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        wizard = CrowdControlWizard(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        self.__wizards[twitchChannelId] = wizard
        self.__timber.log('CheerActionsWizard', f'Started new Crowd Control wizard for {twitchChannel}:{twitchChannelId}')

        return wizard

    async def __startNewGameShuffleWizard(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> GameShuffleWizard:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        wizard = GameShuffleWizard(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        self.__wizards[twitchChannelId] = wizard
        self.__timber.log('CheerActionsWizard', f'Started new Game Shuffle wizard for {twitchChannel}:{twitchChannelId}')

        return wizard

    async def __startNewItemUseWizard(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> ItemUseWizard:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        wizard = ItemUseWizard(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        self.__wizards[twitchChannelId] = wizard
        self.__timber.log('CheerActionsWizard', f'Started new Item Use wizard for {twitchChannel}:{twitchChannelId}')

        return wizard

    async def __startNewSoundAlertWizard(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> SoundAlertWizard:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        wizard = SoundAlertWizard(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        self.__wizards[twitchChannelId] = wizard
        self.__timber.log('CheerActionsWizard', f'Started new Sound Alert wizard for {twitchChannel}:{twitchChannelId}')

        return wizard

    async def __startNewTimeoutWizard(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> TimeoutWizard:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        wizard = TimeoutWizard(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        self.__wizards[twitchChannelId] = wizard
        self.__timber.log('CheerActionsWizard', f'Started new Timeout wizard for {twitchChannel}:{twitchChannelId}')

        return wizard

    async def __startNewVoicemailWizard(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> VoicemailWizard:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        wizard = VoicemailWizard(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        self.__wizards[twitchChannelId] = wizard
        self.__timber.log('CheerActionsWizard', f'Started new Voicemail wizard for {twitchChannel}:{twitchChannelId}')

        return wizard
