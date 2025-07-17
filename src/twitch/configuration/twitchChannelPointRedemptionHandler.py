import asyncio
import queue
import traceback
from queue import SimpleQueue
from typing import Final

from frozenlist import FrozenList

from .twitchChannelPointsMessage import TwitchChannelPointsMessage
from .twitchChannelProvider import TwitchChannelProvider
from ..absTwitchChannelPointRedemptionHandler import AbsTwitchChannelPointRedemptionHandler
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ...channelPointRedemptions.absChannelPointRedemption import AbsChannelPointRedemption
from ...channelPointRedemptions.casualGamePollPointRedemption import CasualGamePollPointRedemption
from ...channelPointRedemptions.chatterPreferredTtsPointRedemption import ChatterPreferredTtsPointRedemption
from ...channelPointRedemptions.cutenessPointRedemption import CutenessPointRedemption
from ...channelPointRedemptions.decTalkSongPointRedemption import DecTalkSongPointRedemption
from ...channelPointRedemptions.pkmnBattlePointRedemption import PkmnBattlePointRedemption
from ...channelPointRedemptions.pkmnCatchPointRedemption import PkmnCatchPointRedemption
from ...channelPointRedemptions.pkmnEvolvePointRedemption import PkmnEvolvePointRedemption
from ...channelPointRedemptions.pkmnShinyPointRedemption import PkmnShinyPointRedemption
from ...channelPointRedemptions.redemptionCounterPointRedemption import RedemptionCounterPointRedemption
from ...channelPointRedemptions.soundAlertPointRedemption import SoundAlertPointRedemption
from ...channelPointRedemptions.stub.stubChannelPointRedemption import StubPointRedemption
from ...channelPointRedemptions.superTriviaGamePointRedemption import SuperTriviaGamePointRedemption
from ...channelPointRedemptions.timeoutPointRedemption import TimeoutPointRedemption
from ...channelPointRedemptions.triviaGamePointRedemption import TriviaGamePointRedemption
from ...channelPointRedemptions.ttsChatterPointRedemption import TtsChatterPointRedemption
from ...channelPointRedemptions.voicemailPointRedemption import VoicemailPointRedemption
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class TwitchChannelPointRedemptionHandler(AbsTwitchChannelPointRedemptionHandler):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        casualGamePollPointRedemption: CasualGamePollPointRedemption | None,
        chatterPreferredTtsPointRedemption: ChatterPreferredTtsPointRedemption | None,
        cutenessPointRedemption: CutenessPointRedemption | None,
        decTalkSongPointRedemption: DecTalkSongPointRedemption | None,
        pkmnBattlePointRedemption: PkmnBattlePointRedemption | None,
        pkmnCatchPointRedemption: PkmnCatchPointRedemption | None,
        pkmnEvolvePointRedemption: PkmnEvolvePointRedemption | None,
        pkmnShinyPointRedemption: PkmnShinyPointRedemption | None,
        redemptionCounterPointRedemption: RedemptionCounterPointRedemption | None,
        soundAlertPointRedemption: SoundAlertPointRedemption | None,
        superTriviaGamePointRedemption: SuperTriviaGamePointRedemption | None,
        timeoutPointRedemption: TimeoutPointRedemption | None,
        triviaGamePointRedemption: TriviaGamePointRedemption | None,
        ttsChatterPointRedemption: TtsChatterPointRedemption | None,
        timber: TimberInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        voicemailPointRedemption: VoicemailPointRedemption | None,
        queueSleepTimeSeconds: float = 1,
        queueTimeoutSeconds: float = 3,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif casualGamePollPointRedemption is not None and not isinstance(casualGamePollPointRedemption, CasualGamePollPointRedemption):
            raise TypeError(f'casualGamePollPointRedemption argument is malformed: \"{casualGamePollPointRedemption}\"')
        elif chatterPreferredTtsPointRedemption is not None and not isinstance(chatterPreferredTtsPointRedemption, ChatterPreferredTtsPointRedemption):
            raise TypeError(f'chatterPreferredTtsPointRedemption argument is malformed: \"{chatterPreferredTtsPointRedemption}\"')
        elif cutenessPointRedemption is not None and not isinstance(cutenessPointRedemption, CutenessPointRedemption):
            raise TypeError(f'cutenessPointRedemption argument is malformed: \"{cutenessPointRedemption}\"')
        elif decTalkSongPointRedemption is not None and not isinstance(decTalkSongPointRedemption, DecTalkSongPointRedemption):
            raise TypeError(f'decTalkSongPointRedemption argument is malformed: \"{decTalkSongPointRedemption}\"')
        elif pkmnBattlePointRedemption is not None and not isinstance(pkmnBattlePointRedemption, PkmnBattlePointRedemption):
            raise TypeError(f'pkmnBattlePointRedemption argument is malformed: \"{pkmnBattlePointRedemption}\"')
        elif pkmnCatchPointRedemption is not None and not isinstance(pkmnCatchPointRedemption, PkmnCatchPointRedemption):
            raise TypeError(f'pkmnCatchPointRedemption argument is malformed: \"{pkmnCatchPointRedemption}\"')
        elif pkmnEvolvePointRedemption is not None and not isinstance(pkmnEvolvePointRedemption, PkmnEvolvePointRedemption):
            raise TypeError(f'pkmnEvolvePointRedemption argument is malformed: \"{pkmnEvolvePointRedemption}\"')
        elif pkmnShinyPointRedemption is not None and not isinstance(pkmnShinyPointRedemption, PkmnShinyPointRedemption):
            raise TypeError(f'pkmnShinyPointRedemption argument is malformed: \"{pkmnShinyPointRedemption}\"')
        elif redemptionCounterPointRedemption is not None and not isinstance(redemptionCounterPointRedemption, RedemptionCounterPointRedemption):
            raise TypeError(f'redemptionCounterPointRedemption argument is malformed: \"{redemptionCounterPointRedemption}\"')
        elif soundAlertPointRedemption is not None and not isinstance(soundAlertPointRedemption, SoundAlertPointRedemption):
            raise TypeError(f'soundAlertPointRedemption argument is malformed: \"{soundAlertPointRedemption}\"')
        elif superTriviaGamePointRedemption is not None and not isinstance(superTriviaGamePointRedemption, SuperTriviaGamePointRedemption):
            raise TypeError(f'superTriviaGamePointRedemption argument is malformed: \"{superTriviaGamePointRedemption}\"')
        elif timeoutPointRedemption is not None and not isinstance(timeoutPointRedemption, TimeoutPointRedemption):
            raise TypeError(f'timeoutPointRedemption argument is malformed: \"{timeoutPointRedemption}\"')
        elif triviaGamePointRedemption is not None and not isinstance(triviaGamePointRedemption, TriviaGamePointRedemption):
            raise TypeError(f'triviaGamePointRedemption argument is malformed: \"{triviaGamePointRedemption}\"')
        elif ttsChatterPointRedemption is not None and not isinstance(ttsChatterPointRedemption, TtsChatterPointRedemption):
            raise TypeError(f'ttsChatterPointRedemption argument is malformed: \"{ttsChatterPointRedemption}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif voicemailPointRedemption is not None and not isinstance(voicemailPointRedemption, VoicemailPointRedemption):
            raise TypeError(f'voicemailPointRedemption argument is malformed: \"{voicemailPointRedemption}\"')
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

        self.__isStarted: bool = False
        self.__channelPointsMessagesQueue: Final[SimpleQueue[TwitchChannelPointsMessage]] = SimpleQueue()
        self.__twitchChannelProvider: TwitchChannelProvider | None = None

        if casualGamePollPointRedemption is None:
            self.__casualGamePollPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__casualGamePollPointRedemption: AbsChannelPointRedemption = casualGamePollPointRedemption

        if chatterPreferredTtsPointRedemption is None:
            self.__chatterPreferredTtsPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__chatterPreferredTtsPointRedemption: AbsChannelPointRedemption = chatterPreferredTtsPointRedemption

        if cutenessPointRedemption is None:
            self.__cutenessPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__cutenessPointRedemption: AbsChannelPointRedemption = cutenessPointRedemption

        if decTalkSongPointRedemption is None:
            self.__decTalkSongPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__decTalkSongPointRedemption: AbsChannelPointRedemption = decTalkSongPointRedemption

        if pkmnBattlePointRedemption is None:
            self.__pkmnBattlePointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__pkmnBattlePointRedemption: AbsChannelPointRedemption = pkmnBattlePointRedemption

        if pkmnCatchPointRedemption is None:
            self.__pkmnCatchPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__pkmnCatchPointRedemption: AbsChannelPointRedemption = pkmnCatchPointRedemption

        if pkmnEvolvePointRedemption is None:
            self.__pkmnEvolvePointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__pkmnEvolvePointRedemption: AbsChannelPointRedemption = pkmnEvolvePointRedemption

        if pkmnShinyPointRedemption is None:
            self.__pkmnShinyPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__pkmnShinyPointRedemption: AbsChannelPointRedemption = pkmnShinyPointRedemption

        if redemptionCounterPointRedemption is None:
            self.__redemptionCounterPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__redemptionCounterPointRedemption: AbsChannelPointRedemption = redemptionCounterPointRedemption

        if soundAlertPointRedemption is None:
            self.__soundAlertPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__soundAlertPointRedemption: AbsChannelPointRedemption = soundAlertPointRedemption

        if superTriviaGamePointRedemption is None:
            self.__superTriviaGamePointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__superTriviaGamePointRedemption: AbsChannelPointRedemption = superTriviaGamePointRedemption

        if timeoutPointRedemption is None:
            self.__timeoutPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__timeoutPointRedemption: AbsChannelPointRedemption = timeoutPointRedemption

        if triviaGamePointRedemption is None:
            self.__triviaGamePointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__triviaGamePointRedemption: AbsChannelPointRedemption = triviaGamePointRedemption

        if ttsChatterPointRedemption is None:
            self.__ttsChatterPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__ttsChatterPointRedemption: AbsChannelPointRedemption = ttsChatterPointRedemption

        if voicemailPointRedemption is None:
            self.__voicemailPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__voicemailPointRedemption: AbsChannelPointRedemption = voicemailPointRedemption

    async def __handleChannelPointsMessage(self, channelPointsMessage: TwitchChannelPointsMessage):
        if not isinstance(channelPointsMessage, TwitchChannelPointsMessage):
            raise TypeError(f'channelPointsMessage argument is malformed: \"{channelPointsMessage}\"')

        user = channelPointsMessage.twitchUser
        twitchChannelProvider = self.__twitchChannelProvider

        if twitchChannelProvider is None:
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Abandoning handling of this channel point redemption as no TwitchChannelProvider has been set: \"{twitchChannelProvider}\"')
            return

        twitchChannel = await twitchChannelProvider.getTwitchChannel(user.handle)

        if user.areRedemptionCountersEnabled:
            await self.__redemptionCounterPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage,
            )

        if user.isCasualGamePollEnabled and channelPointsMessage.rewardId == user.casualGamePollRewardId:
            if await self.__casualGamePollPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage,
            ):
                return

        if user.isChatterPreferredTtsEnabled and channelPointsMessage.rewardId == user.setChatterPreferredTtsRewardId:
            if await self.__chatterPreferredTtsPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage,
            ):
                return

        if user.isCutenessEnabled:
            if await self.__cutenessPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage,
            ):
                return

        if user.isDecTalkSongsEnabled:
            if await self.__decTalkSongPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage,
            ):
                return

        if user.isPkmnEnabled:
            if channelPointsMessage.rewardId == user.pkmnBattleRewardId:
                if await self.__pkmnBattlePointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage,
                ):
                    return

            if await self.__pkmnCatchPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage,
            ):
                return

            if channelPointsMessage.rewardId == user.pkmnEvolveRewardId:
                if await self.__pkmnEvolvePointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage,
                ):
                    return

            if channelPointsMessage.rewardId == user.pkmnShinyRewardId:
                if await self.__pkmnShinyPointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage,
                ):
                    return

        if user.areSoundAlertsEnabled:
            if await self.__soundAlertPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage,
            ):
                return

        if user.isSuperTriviaGameEnabled and channelPointsMessage.rewardId == user.superTriviaGameRewardId:
            if await self.__superTriviaGamePointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage,
            ):
                return

        if await self.__timeoutPointRedemption.handlePointRedemption(
            twitchChannel = twitchChannel,
            twitchChannelPointsMessage = channelPointsMessage,
        ):
            return

        if user.isTriviaGameEnabled and channelPointsMessage.rewardId == user.triviaGameRewardId:
            if await self.__triviaGamePointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage,
            ):
                return

        if user.areTtsChattersEnabled and channelPointsMessage.rewardId == user.ttsChatterRewardId:
            if await self.__ttsChatterPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage,
            ):
                return

        if user.isVoicemailEnabled and channelPointsMessage.rewardId == user.voicemailRewardId:
            if await self.__voicemailPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage,
            ):
                return

    async def onNewChannelPointRedemption(self, channelPointsMessage: TwitchChannelPointsMessage):
        if not isinstance(channelPointsMessage, TwitchChannelPointsMessage):
            raise TypeError(f'channelPointsMessage argument is malformed: \"{channelPointsMessage}\"')

        self.__submitChannelPointsMessage(
            channelPointsMessage = channelPointsMessage,
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

        channelPointsMessage = TwitchChannelPointsMessage(
            rewardCost = reward.cost,
            eventId = eventId,
            redemptionMessage = redemptionUserInput,
            rewardId = reward.rewardId,
            twitchChannelId = twitchChannelId,
            userId = redemptionUserId,
            userName = redemptionUserLogin,
            twitchUser = user,
        )

        await self.onNewChannelPointRedemption(
            channelPointsMessage = channelPointsMessage,
        )

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider

    def start(self):
        if self.__isStarted:
            self.__timber.log('TwitchChannelPointRedemptionHandler', 'Not starting TwitchChannelPointRedemptionHandler as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('TwitchWebsocketClient', 'Starting TwitchWebsocketClient...')
        self.__backgroundTaskHelper.createTask(self.__startChannelPointsMessageLoop())

    async def __startChannelPointsMessageLoop(self):
        while True:
            channelPointsMessages: FrozenList[TwitchChannelPointsMessage] = FrozenList()

            try:
                while not self.__channelPointsMessagesQueue.empty():
                    channelPointsMessages.append(self.__channelPointsMessagesQueue.get_nowait())
            except queue.Empty as e:
                self.__timber.log('TwitchChannelPointRedemptionHandler', f'Encountered queue.Empty when building up channelPointsMessages list (queue size: {self.__channelPointsMessagesQueue.qsize()}) (channelPointsMessages size: {len(channelPointsMessages)}): {e}', e, traceback.format_exc())

            channelPointsMessages.freeze()

            for channelPointsMessage in channelPointsMessages:
                try:
                    await self.__handleChannelPointsMessage(channelPointsMessage)
                except Exception as e:
                    self.__timber.log('TwitchChannelPointRedemptionHandler', f'Encountered unknown Exception when looping through channelPointsMessages (queue size: {self.__channelPointsMessagesQueue.qsize()}) ({channelPointsMessage=}): {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__queueSleepTimeSeconds)

    def __submitChannelPointsMessage(self, channelPointsMessage: TwitchChannelPointsMessage):
        if not isinstance(channelPointsMessage, TwitchChannelPointsMessage):
            raise TypeError(f'channelPointsMessage argument is malformed: \"{channelPointsMessage}\"')

        try:
            self.__channelPointsMessagesQueue.put(channelPointsMessage, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Encountered queue.Full when submitting a new action ({channelPointsMessage}) into the action queue (queue size: {self.__channelPointsMessagesQueue.qsize()}): {e}', e, traceback.format_exc())
