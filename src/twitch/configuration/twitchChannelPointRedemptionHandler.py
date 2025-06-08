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
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class TwitchChannelPointRedemptionHandler(AbsTwitchChannelPointRedemptionHandler):

    def __init__(
        self,
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
    ):
        if casualGamePollPointRedemption is not None and not isinstance(casualGamePollPointRedemption, CasualGamePollPointRedemption):
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

        self.__timber: TimberInterface = timber
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def onNewChannelPointRedemption(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.requirePayload().event

        if event is None:
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that has no event: ({user=}) ({userId=}) ({dataBundle=})')
            return

        broadcasterUserId = event.broadcasterUserId
        eventId = dataBundle.metadata.messageId
        reward = event.reward
        redemptionUserId = event.userId
        redemptionUserInput = event.userInput
        redemptionUserLogin = event.userLogin

        if not utils.isValidStr(broadcasterUserId) or not utils.isValidStr(eventId) or reward is None or not utils.isValidStr(redemptionUserId) or not utils.isValidStr(redemptionUserLogin):
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({broadcasterUserId=}) ({eventId=}) ({redemptionUserId=}) ({redemptionUserInput=}) ({redemptionUserLogin=}) ({reward=})')
            return

        self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received an event: ({user=}) ({broadcasterUserId=}) ({eventId=}) ({redemptionUserId=}) ({redemptionUserInput=}) ({redemptionUserLogin=}) ({reward=})')

        await self.__userIdsRepository.setUser(
            userId = redemptionUserId,
            userName = redemptionUserLogin
        )

        channelPointsMessage = TwitchChannelPointsMessage(
            rewardCost = reward.cost,
            eventId = eventId,
            redemptionMessage = redemptionUserInput,
            rewardId = reward.rewardId,
            twitchChannelId = broadcasterUserId,
            userId = redemptionUserId,
            userName = redemptionUserLogin,
            twitchUser = user
        )

        twitchChannelProvider = self.__twitchChannelProvider

        if twitchChannelProvider is None:
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Abandoning handling of this channel point redemption as no TwitchChannelProvider has been set: \"{twitchChannelProvider}\"')
            return

        twitchChannel = await twitchChannelProvider.getTwitchChannel(user.handle)

        if user.areRedemptionCountersEnabled:
            if await self.__redemptionCounterPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.isCasualGamePollEnabled and channelPointsMessage.rewardId == user.casualGamePollRewardId:
            if await self.__casualGamePollPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.isChatterPreferredTtsEnabled and channelPointsMessage.rewardId == user.setChatterPreferredTtsRewardId:
            if await self.__chatterPreferredTtsPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.isCutenessEnabled:
            if await self.__cutenessPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.isDecTalkSongsEnabled:
            if await self.__decTalkSongPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.isPkmnEnabled:
            if channelPointsMessage.rewardId == user.pkmnBattleRewardId:
                if await self.__pkmnBattlePointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

            if await self.__pkmnCatchPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

            if channelPointsMessage.rewardId == user.pkmnEvolveRewardId:
                if await self.__pkmnEvolvePointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

            if channelPointsMessage.rewardId == user.pkmnShinyRewardId:
                if await self.__pkmnShinyPointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

        if user.areSoundAlertsEnabled:
            if await self.__soundAlertPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.isSuperTriviaGameEnabled and channelPointsMessage.rewardId == user.superTriviaGameRewardId:
            if await self.__superTriviaGamePointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if await self.__timeoutPointRedemption.handlePointRedemption(
            twitchChannel = twitchChannel,
            twitchChannelPointsMessage = channelPointsMessage
        ):
            return

        if user.isTriviaGameEnabled and channelPointsMessage.rewardId == user.triviaGameRewardId:
            if await self.__triviaGamePointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.areTtsChattersEnabled and channelPointsMessage.rewardId == user.ttsChatterRewardId:
            if await self.__ttsChatterPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.isVoicemailEnabled and channelPointsMessage.rewardId == user.voicemailRewardId:
            if await self.__voicemailPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
