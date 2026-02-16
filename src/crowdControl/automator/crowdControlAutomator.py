import asyncio
from datetime import datetime, timedelta
from typing import Final

from .crowdControlAutomatorAddResult import CrowdControlAutomatorAddResult
from .crowdControlAutomatorData import CrowdControlAutomatorData
from .crowdControlAutomatorInterface import CrowdControlAutomatorInterface
from .crowdControlAutomatorRemovalResult import CrowdControlAutomatorRemovalResult
from ..actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from ..crowdControlMachineInterface import CrowdControlMachineInterface
from ..idGenerator.crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.usersRepositoryInterface import UsersRepositoryInterface


class CrowdControlAutomator(CrowdControlAutomatorInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        crowdControlIdGenerator: CrowdControlIdGeneratorInterface,
        crowdControlMachine: CrowdControlMachineInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        refreshSleepTimeSeconds: float = 5,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(crowdControlIdGenerator, CrowdControlIdGeneratorInterface):
            raise TypeError(f'crowdControlIdGenerator argument is malformed: \"{crowdControlIdGenerator}\"')
        elif not isinstance(crowdControlMachine, CrowdControlMachineInterface):
            raise TypeError(f'crowdControlMachine argument is malformed: \"{crowdControlMachine}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not utils.isValidNum(refreshSleepTimeSeconds):
            raise TypeError(f'refreshSleepTimeSeconds argument is malformed: \"{refreshSleepTimeSeconds}\"')
        elif refreshSleepTimeSeconds < 1 or refreshSleepTimeSeconds > 60:
            raise ValueError(f'refreshSleepTimeSeconds argument is malformed: \"{refreshSleepTimeSeconds}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__crowdControlIdGenerator: Final[CrowdControlIdGeneratorInterface] = crowdControlIdGenerator
        self.__crowdControlMachine: Final[CrowdControlMachineInterface] = crowdControlMachine
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository
        self.__refreshSleepTimeSeconds: Final[float] = refreshSleepTimeSeconds

        self.__isStarted: bool = False
        self.__automatorData: Final[dict[str, CrowdControlAutomatorData]] = dict()
        self.__lastGameShuffleTimes: Final[dict[str, datetime | None]] = dict()

    async def addGameShuffleAutomator(
        self,
        automatorData: CrowdControlAutomatorData,
    ) -> CrowdControlAutomatorAddResult:
        if not isinstance(automatorData, CrowdControlAutomatorData):
            raise TypeError(f'automatorData argument is malformed: \"{automatorData}\"')

        existingAutomatorData = self.__automatorData.get(automatorData.twitchChannelId, None)
        self.__automatorData[automatorData.twitchChannelId] = automatorData

        if existingAutomatorData is None:
            self.__timber.log('CrowdControlAutomator', f'Added game shuffle automator ({automatorData=})')
            return CrowdControlAutomatorAddResult.OK
        else:
            self.__timber.log('CrowdControlAutomator', f'Replaced game shuffle automator ({automatorData=}) ({existingAutomatorData=})')
            return CrowdControlAutomatorAddResult.REPLACED

    async def __refreshGameShuffleAutomators(self):
        if len(self.__automatorData) == 0:
            return

        now = self.__timeZoneRepository.getNow()
        twitchChannelIds: set[str] = set()

        for automatorData in self.__automatorData.values():
            lastGameShuffleTime = self.__lastGameShuffleTimes.get(automatorData.twitchChannelId, None)

            if lastGameShuffleTime is None:
                twitchChannelIds.add(automatorData.twitchChannelId)
                continue

            timeBetweenShuffles = now - lastGameShuffleTime
            reoccurSeconds = timedelta(seconds = automatorData.reoccurSeconds)

            if timeBetweenShuffles >= reoccurSeconds:
                twitchChannelIds.add(automatorData.twitchChannelId)

        if len(twitchChannelIds) == 0:
            return

        cynanBotUserName = await self.__twitchHandleProvider.getTwitchHandle()
        cynanBotUserId = await self.__userIdsRepository.requireUserId(cynanBotUserName)

        for twitchChannelId in twitchChannelIds:
            await self.__submitGameShuffleAction(
                now = now,
                cynanBotUserId = cynanBotUserId,
                cynanBotUserName = cynanBotUserName,
                twitchChannelId = twitchChannelId,
            )

    async def removeGameShuffleAutomator(
        self,
        twitchChannelId: str,
    ) -> CrowdControlAutomatorRemovalResult:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        existingAutomatorData = self.__automatorData.pop(twitchChannelId, None)
        self.__lastGameShuffleTimes.pop(twitchChannelId, None)

        if existingAutomatorData is None:
            self.__timber.log('CrowdControlAutomator', f'Attempted to remove non-existing game shuffle automator ({twitchChannelId=})')
            return CrowdControlAutomatorRemovalResult.DID_NOT_EXIST
        else:
            self.__timber.log('CrowdControlAutomator', f'Removed game shuffle automator ({existingAutomatorData=})')
            return CrowdControlAutomatorRemovalResult.OK

    def start(self):
        if self.__isStarted:
            self.__timber.log('CrowdControlAutomator', 'Not starting CrowdControlAutomator as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('CrowdControlAutomator', 'Starting CrowdControlAutomator...')
        self.__backgroundTaskHelper.createTask(self.__startRefreshLoop())

    async def __startRefreshLoop(self):
        while True:
            await self.__refreshGameShuffleAutomators()
            await asyncio.sleep(self.__refreshSleepTimeSeconds)

    async def __submitGameShuffleAction(
        self,
        now: datetime,
        cynanBotUserId: str,
        cynanBotUserName: str,
        twitchChannelId: str,
    ):
        userName = await self.__userIdsRepository.requireUserName(twitchChannelId)
        user = await self.__usersRepository.getUserAsync(userName)

        if not user.isCrowdControlEnabled:
            self.__timber.log('CrowdControlAutomator', f'Removing game shuffle automator for user that has crowd control disabled ({user=}) ({twitchChannelId=})')
            await self.removeGameShuffleAutomator(twitchChannelId)
            return

        self.__crowdControlMachine.submitAction(GameShuffleCrowdControlAction(
            entryWithinGigaShuffle = False,
            dateTime = now,
            startOfGigaShuffleSize = None,
            actionId = await self.__crowdControlIdGenerator.generateActionId(),
            chatterUserId = cynanBotUserId,
            chatterUserName = cynanBotUserName,
            twitchChannel = user.handle,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = None,
        ))

        self.__timber.log('CrowdControlAutomator', f'Submitted automated game shuffle ({user=}) ({twitchChannelId=})')
