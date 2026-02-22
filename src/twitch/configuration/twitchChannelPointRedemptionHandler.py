import asyncio
import queue
import traceback
from queue import SimpleQueue
from typing import Final

from frozenlist import FrozenList

from ..absTwitchChannelPointRedemptionHandler import AbsTwitchChannelPointRedemptionHandler
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ...channelPointRedemptions.absChannelPointRedemption import AbsChannelPointRedemption
from ...channelPointRedemptions.casualGamePollPointRedemption import CasualGamePollPointRedemption
from ...channelPointRedemptions.chatterPreferredNamePointRedemption import ChatterPreferredNamePointRedemption
from ...channelPointRedemptions.chatterPreferredTtsPointRedemption import ChatterPreferredTtsPointRedemption
from ...channelPointRedemptions.cutenessPointRedemption import CutenessPointRedemption
from ...channelPointRedemptions.decTalkSongPointRedemption import DecTalkSongPointRedemption
from ...channelPointRedemptions.mouseCursorPointRedemption import MouseCursorPointRedemption
from ...channelPointRedemptions.pkmnBattlePointRedemption import PkmnBattlePointRedemption
from ...channelPointRedemptions.pkmnCatchPointRedemption import PkmnCatchPointRedemption
from ...channelPointRedemptions.pkmnEvolvePointRedemption import PkmnEvolvePointRedemption
from ...channelPointRedemptions.pkmnShinyPointRedemption import PkmnShinyPointRedemption
from ...channelPointRedemptions.redemptionCounterPointRedemption import RedemptionCounterPointRedemption
from ...channelPointRedemptions.soundAlertPointRedemption import SoundAlertPointRedemption
from ...channelPointRedemptions.stub.stubChannelPointRedemption import StubChannelPointRedemption
from ...channelPointRedemptions.superTriviaGamePointRedemption import SuperTriviaGamePointRedemption
from ...channelPointRedemptions.superTriviaLotrGamePointRedemption import SuperTriviaLotrGamePointRedemption
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
        chatterPreferredNamePointRedemption: ChatterPreferredNamePointRedemption | None,
        chatterPreferredTtsPointRedemption: ChatterPreferredTtsPointRedemption | None,
        cutenessPointRedemption: CutenessPointRedemption | None,
        decTalkSongPointRedemption: DecTalkSongPointRedemption | None,
        mouseCursorPointRedemption: MouseCursorPointRedemption | None,
        pkmnBattlePointRedemption: PkmnBattlePointRedemption | None,
        pkmnCatchPointRedemption: PkmnCatchPointRedemption | None,
        pkmnEvolvePointRedemption: PkmnEvolvePointRedemption | None,
        pkmnShinyPointRedemption: PkmnShinyPointRedemption | None,
        redemptionCounterPointRedemption: RedemptionCounterPointRedemption | None,
        soundAlertPointRedemption: SoundAlertPointRedemption | None,
        superTriviaGamePointRedemption: SuperTriviaGamePointRedemption | None,
        superTriviaLotrGamePointRedemption: SuperTriviaLotrGamePointRedemption | None,
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
        elif chatterPreferredNamePointRedemption is not None and not isinstance(chatterPreferredNamePointRedemption, ChatterPreferredNamePointRedemption):
            raise TypeError(f'chatterPreferredNamePointRedemption argument is malformed: \"{chatterPreferredNamePointRedemption}\"')
        elif chatterPreferredTtsPointRedemption is not None and not isinstance(chatterPreferredTtsPointRedemption, ChatterPreferredTtsPointRedemption):
            raise TypeError(f'chatterPreferredTtsPointRedemption argument is malformed: \"{chatterPreferredTtsPointRedemption}\"')
        elif cutenessPointRedemption is not None and not isinstance(cutenessPointRedemption, CutenessPointRedemption):
            raise TypeError(f'cutenessPointRedemption argument is malformed: \"{cutenessPointRedemption}\"')
        elif decTalkSongPointRedemption is not None and not isinstance(decTalkSongPointRedemption, DecTalkSongPointRedemption):
            raise TypeError(f'decTalkSongPointRedemption argument is malformed: \"{decTalkSongPointRedemption}\"')
        elif mouseCursorPointRedemption is not None and not isinstance(mouseCursorPointRedemption, MouseCursorPointRedemption):
            raise TypeError(f'mouseCursorPointRedemption argument is malformed: \"{mouseCursorPointRedemption}\"')
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
        elif superTriviaLotrGamePointRedemption is not None and not isinstance(superTriviaLotrGamePointRedemption, SuperTriviaLotrGamePointRedemption):
            raise TypeError(f'superTriviaLotrGamePointRedemption argument is malformed: \"{superTriviaLotrGamePointRedemption}\"')
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
        self.__channelPointsRedemptionsQueue: Final[SimpleQueue[TwitchChannelPointsRedemption]] = SimpleQueue()

        if casualGamePollPointRedemption is None:
            self.__casualGamePollPointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__casualGamePollPointRedemption: AbsChannelPointRedemption = casualGamePollPointRedemption

        if chatterPreferredNamePointRedemption is None:
            self.__chatterPreferredNamePointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__chatterPreferredNamePointRedemption: AbsChannelPointRedemption = chatterPreferredNamePointRedemption

        if chatterPreferredTtsPointRedemption is None:
            self.__chatterPreferredTtsPointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__chatterPreferredTtsPointRedemption: AbsChannelPointRedemption = chatterPreferredTtsPointRedemption

        if cutenessPointRedemption is None:
            self.__cutenessPointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__cutenessPointRedemption: AbsChannelPointRedemption = cutenessPointRedemption

        if decTalkSongPointRedemption is None:
            self.__decTalkSongPointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__decTalkSongPointRedemption: AbsChannelPointRedemption = decTalkSongPointRedemption

        if mouseCursorPointRedemption is None:
            self.__mouseCursorPointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__mouseCursorPointRedemption: AbsChannelPointRedemption = mouseCursorPointRedemption

        if pkmnBattlePointRedemption is None:
            self.__pkmnBattlePointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__pkmnBattlePointRedemption: AbsChannelPointRedemption = pkmnBattlePointRedemption

        if pkmnCatchPointRedemption is None:
            self.__pkmnCatchPointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__pkmnCatchPointRedemption: AbsChannelPointRedemption = pkmnCatchPointRedemption

        if pkmnEvolvePointRedemption is None:
            self.__pkmnEvolvePointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__pkmnEvolvePointRedemption: AbsChannelPointRedemption = pkmnEvolvePointRedemption

        if pkmnShinyPointRedemption is None:
            self.__pkmnShinyPointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__pkmnShinyPointRedemption: AbsChannelPointRedemption = pkmnShinyPointRedemption

        if redemptionCounterPointRedemption is None:
            self.__redemptionCounterPointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__redemptionCounterPointRedemption: AbsChannelPointRedemption = redemptionCounterPointRedemption

        if soundAlertPointRedemption is None:
            self.__soundAlertPointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__soundAlertPointRedemption: AbsChannelPointRedemption = soundAlertPointRedemption

        if superTriviaGamePointRedemption is None:
            self.__superTriviaGamePointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__superTriviaGamePointRedemption: AbsChannelPointRedemption = superTriviaGamePointRedemption

        if superTriviaLotrGamePointRedemption is None:
            self.__superTriviaLotrGamePointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__superTriviaLotrGamePointRedemption: AbsChannelPointRedemption = superTriviaLotrGamePointRedemption

        if triviaGamePointRedemption is None:
            self.__triviaGamePointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__triviaGamePointRedemption: AbsChannelPointRedemption = triviaGamePointRedemption

        if ttsChatterPointRedemption is None:
            self.__ttsChatterPointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__ttsChatterPointRedemption: AbsChannelPointRedemption = ttsChatterPointRedemption

        if voicemailPointRedemption is None:
            self.__voicemailPointRedemption: AbsChannelPointRedemption = StubChannelPointRedemption()
        else:
            self.__voicemailPointRedemption: AbsChannelPointRedemption = voicemailPointRedemption

    async def __handleChannelPointsRedemption(self, channelPointsRedemption: TwitchChannelPointsRedemption):
        if not isinstance(channelPointsRedemption, TwitchChannelPointsRedemption):
            raise TypeError(f'channelPointsRedemption argument is malformed: \"{channelPointsRedemption}\"')

        user = channelPointsRedemption.twitchUser

        if user.areRedemptionCountersEnabled:
            await self.__redemptionCounterPointRedemption.handlePointRedemption(
                channelPointsRedemption = channelPointsRedemption,
            )

        if user.isCasualGamePollEnabled and channelPointsRedemption.rewardId == user.casualGamePollRewardId:
            if await self.__casualGamePollPointRedemption.handlePointRedemption(
                channelPointsRedemption = channelPointsRedemption,
            ):
                return

        if channelPointsRedemption.rewardId == user.chatterPreferredNameRewardId:
            if await self.__chatterPreferredNamePointRedemption.handlePointRedemption(
                channelPointsRedemption = channelPointsRedemption,
            ):
                return

        if user.isChatterPreferredTtsEnabled and channelPointsRedemption.rewardId == user.setChatterPreferredTtsRewardId:
            if await self.__chatterPreferredTtsPointRedemption.handlePointRedemption(
                channelPointsRedemption = channelPointsRedemption,
            ):
                return

        if user.isCutenessEnabled:
            if await self.__cutenessPointRedemption.handlePointRedemption(
                channelPointsRedemption = channelPointsRedemption,
            ):
                return

        if user.isDecTalkSongsEnabled:
            if await self.__decTalkSongPointRedemption.handlePointRedemption(
                channelPointsRedemption = channelPointsRedemption,
            ):
                return

        if user.isMouseCursorEnabled and channelPointsRedemption.rewardId == user.mouseCursorRewardId:
            if await self.__mouseCursorPointRedemption.handlePointRedemption(
                channelPointsRedemption = channelPointsRedemption,
            ):
                return

        if user.isPkmnEnabled:
            if channelPointsRedemption.rewardId == user.pkmnBattleRewardId:
                if await self.__pkmnBattlePointRedemption.handlePointRedemption(
                    channelPointsRedemption = channelPointsRedemption,
                ):
                    return

            if await self.__pkmnCatchPointRedemption.handlePointRedemption(
                channelPointsRedemption = channelPointsRedemption,
            ):
                return

            if channelPointsRedemption.rewardId == user.pkmnEvolveRewardId:
                if await self.__pkmnEvolvePointRedemption.handlePointRedemption(
                    channelPointsRedemption = channelPointsRedemption,
                ):
                    return

            if channelPointsRedemption.rewardId == user.pkmnShinyRewardId:
                if await self.__pkmnShinyPointRedemption.handlePointRedemption(
                    channelPointsRedemption = channelPointsRedemption,
                ):
                    return

        if user.areSoundAlertsEnabled:
            if await self.__soundAlertPointRedemption.handlePointRedemption(
                channelPointsRedemption = channelPointsRedemption,
            ):
                return

        if user.isSuperTriviaGameEnabled:
            if channelPointsRedemption.rewardId == user.superTriviaGameRewardId:
                if await self.__superTriviaGamePointRedemption.handlePointRedemption(
                    channelPointsRedemption = channelPointsRedemption,
                ):
                    return

            if channelPointsRedemption.rewardId == user.superTriviaLotrGameRewardId:
                if await self.__superTriviaLotrGamePointRedemption.handlePointRedemption(
                    channelPointsRedemption = channelPointsRedemption,
                ):
                    return

        if user.isTriviaGameEnabled and channelPointsRedemption.rewardId == user.triviaGameRewardId:
            if await self.__triviaGamePointRedemption.handlePointRedemption(
                channelPointsRedemption = channelPointsRedemption,
            ):
                return

        if user.areTtsChattersEnabled and channelPointsRedemption.rewardId == user.ttsChatterRewardId:
            if await self.__ttsChatterPointRedemption.handlePointRedemption(
                channelPointsRedemption = channelPointsRedemption,
            ):
                return

        if user.isVoicemailEnabled and channelPointsRedemption.rewardId == user.voicemailRewardId:
            if await self.__voicemailPointRedemption.handlePointRedemption(
                channelPointsRedemption = channelPointsRedemption,
            ):
                return

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
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Encountered queue.Full when submitting a new action ({channelPointsRedemption}) into the action queue (queue size: {self.__channelPointsRedemptionsQueue.qsize()})', e, traceback.format_exc())
