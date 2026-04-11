import asyncio
import queue
import traceback
from queue import SimpleQueue
from typing import Any, Collection, Final

from frozenlist import FrozenList

from ..absTwitchChannelPointRedemptionHandler import AbsTwitchChannelPointRedemptionHandler
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ...channelPointRedemptions.absChannelPointsRedemption2 import AbsChannelPointRedemption2
from ...channelPointRedemptions.pointsRedemptionResult import PointsRedemptionResult
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class TwitchChannelPointRedemptionHandler(AbsTwitchChannelPointRedemptionHandler):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        pointRedemptions: Collection[AbsChannelPointRedemption2 | Any | None] | None,
        queueSleepTimeSeconds: float = 1,
        queueTimeoutSeconds: float = 3,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif pointRedemptions is not None and not isinstance(pointRedemptions, Collection):
            raise TypeError(f'pointRedemptions argument is malformed: \"{pointRedemptions}\"')
        elif not utils.isValidNum(queueSleepTimeSeconds):
            raise TypeError(f'queueSleepTimeSeconds argument is malformed: \"{queueSleepTimeSeconds}\"')
        elif queueSleepTimeSeconds < 1 or queueSleepTimeSeconds > 15:
            raise ValueError(f'queueSleepTimeSeconds argument is out of bounds: {queueSleepTimeSeconds}')
        elif not utils.isValidNum(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__timber: Final[TimberInterface] = timber
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__queueSleepTimeSeconds: Final[float] = queueSleepTimeSeconds
        self.__queueTimeoutSeconds: Final[float] = queueTimeoutSeconds
        self.__pointRedemptions: Final[Collection[AbsChannelPointRedemption2]] = self.__buildPointRedemptionsCollection(pointRedemptions)

        self.__isStarted: bool = False
        self.__channelPointsRedemptionsQueue: Final[SimpleQueue[TwitchChannelPointsRedemption]] = SimpleQueue()

    def __buildPointRedemptionsCollection(
        self,
        pointRedemptions: Collection[AbsChannelPointRedemption2 | Any | None] | None,
    ) -> Collection[AbsChannelPointRedemption2]:
        if pointRedemptions is None:
            emptyPointRedemptions: FrozenList[AbsChannelPointRedemption2] = FrozenList()
            emptyPointRedemptions.freeze()
            return emptyPointRedemptions

        frozenPointRedemptions: FrozenList[AbsChannelPointRedemption2 | Any | None] = FrozenList(pointRedemptions)
        frozenPointRedemptions.freeze()

        validPointRedemptions: FrozenList[AbsChannelPointRedemption2] = FrozenList()

        for index, pointRedemption in enumerate(frozenPointRedemptions):
            if pointRedemption is None:
                continue
            elif isinstance(pointRedemption, AbsChannelPointRedemption2):
                validPointRedemptions.append(pointRedemption)
            else:
                exception = TypeError(f'Encountered an invalid AbsChannelPointRedemption2 instance ({index=}) ({pointRedemption=}) ({frozenPointRedemptions=})')
                self.__timber.log('TwitchChannelPointRedemptionHandler', f'Encountered an invalid AbsChannelPointRedemption2 instance ({index=}) ({pointRedemption=}) ({frozenPointRedemptions=})', exception, traceback.format_exc())
                raise exception

        validPointRedemptions.freeze()
        return validPointRedemptions

    async def __handleChannelPointsRedemption(self, channelPointsRedemption: TwitchChannelPointsRedemption):
        if not isinstance(channelPointsRedemption, TwitchChannelPointsRedemption):
            raise TypeError(f'channelPointsRedemption argument is malformed: \"{channelPointsRedemption}\"')

        for index, pointRedemption in enumerate(self.__pointRedemptions):
            try:
                relevantRewardIds = pointRedemption.relevantRewardIds(
                    twitchUser = channelPointsRedemption.twitchUser,
                )

                if channelPointsRedemption.rewardId not in relevantRewardIds:
                    continue

                result = await pointRedemption.handlePointsRedemption(
                    pointsRedemption = channelPointsRedemption,
                )

                match result:
                    case PointsRedemptionResult.CONSUMED: return
                    case PointsRedemptionResult.HANDLED: continue
                    case PointsRedemptionResult.IGNORED: pass
            except Exception as e:
                self.__timber.log('TwitchChannelPointRedemptionHandler', f'Encountered an unexpected error while handling a point redemption ({index=}) ({pointRedemption=}) ({channelPointsRedemption=})', e, traceback.format_exc())

    async def onNewChannelPointsRedemption(self, channelPointsRedemption: TwitchChannelPointsRedemption):
        if not isinstance(channelPointsRedemption, TwitchChannelPointsRedemption):
            raise TypeError(f'channelPointsRedemption argument is malformed: \"{channelPointsRedemption}\"')

        self.__submitChannelPointsRedemption(
            channelPointsRedemption = channelPointsRedemption,
        )

    async def onNewChannelPointRedemptionDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.requirePayload().event

        if event is None:
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that has no event: ({user=}) ({twitchChannelId=}) ({dataBundle=})')
            return

        eventId = dataBundle.metadata.messageId
        redemptionUserId = event.userId
        redemptionUserInput = event.userInput
        redemptionUserLogin = event.userLogin
        reward = event.reward

        if not utils.isValidStr(eventId) or reward is None or not utils.isValidStr(redemptionUserId) or not utils.isValidStr(redemptionUserLogin):
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({twitchChannelId=}) ({dataBundle=}) ({eventId=}) ({redemptionUserId=}) ({redemptionUserInput=}) ({redemptionUserLogin=}) ({reward=})')
            return

        self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a channel point redemption event: ({user=}) ({twitchChannelId=}) ({eventId=}) ({redemptionUserId=}) ({redemptionUserInput=}) ({redemptionUserLogin=}) ({reward=})')

        await self.__userIdsRepository.setUser(
            userId = redemptionUserId,
            userName = redemptionUserLogin,
        )

        channelPointsRedemption = TwitchChannelPointsRedemption(
            rewardCost = reward.cost,
            eventId = eventId,
            redemptionMessage = redemptionUserInput,
            redemptionUserId = redemptionUserId,
            redemptionUserLogin = redemptionUserLogin,
            redemptionUserName = redemptionUserLogin,
            rewardId = reward.rewardId,
            twitchChannelId = twitchChannelId,
            twitchUser = user,
        )

        await self.onNewChannelPointsRedemption(
            channelPointsRedemption = channelPointsRedemption,
        )

    def start(self):
        if self.__isStarted:
            self.__timber.log('TwitchChannelPointRedemptionHandler', 'Not starting TwitchChannelPointRedemptionHandler as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('TwitchWebsocketClient', 'Starting TwitchWebsocketClient...')
        self.__backgroundTaskHelper.createTask(self.__startChannelPointsMessageLoop())

    async def __startChannelPointsMessageLoop(self):
        while True:
            channelPointsRedemptions: FrozenList[TwitchChannelPointsRedemption] = FrozenList()

            try:
                while not self.__channelPointsRedemptionsQueue.empty():
                    channelPointsRedemptions.append(self.__channelPointsRedemptionsQueue.get_nowait())
            except queue.Empty as e:
                self.__timber.log('TwitchChannelPointRedemptionHandler', f'Encountered queue.Empty when building up channelPointsMessages list (queue size: {self.__channelPointsRedemptionsQueue.qsize()}) (channelPointsMessages size: {len(channelPointsRedemptions)})', e, traceback.format_exc())

            channelPointsRedemptions.freeze()

            for channelPointsRedemption in channelPointsRedemptions:
                try:
                    await self.__handleChannelPointsRedemption(channelPointsRedemption)
                except Exception as e:
                    self.__timber.log('TwitchChannelPointRedemptionHandler', f'Encountered unknown Exception when looping through channelPointsMessages (queue size: {self.__channelPointsRedemptionsQueue.qsize()}) ({channelPointsRedemption=})', e, traceback.format_exc())

            await asyncio.sleep(self.__queueSleepTimeSeconds)

    def __submitChannelPointsRedemption(self, channelPointsRedemption: TwitchChannelPointsRedemption):
        if not isinstance(channelPointsRedemption, TwitchChannelPointsRedemption):
            raise TypeError(f'channelPointsRedemption argument is malformed: \"{channelPointsRedemption}\"')

        try:
            self.__channelPointsRedemptionsQueue.put(channelPointsRedemption, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Encountered queue.Full when submitting a new points redemption ({channelPointsRedemption}) into the redemption queue (queue size: {self.__channelPointsRedemptionsQueue.qsize()})', e, traceback.format_exc())
