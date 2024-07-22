from .twitchChannelPointsMessage import TwitchChannelPointsMessage
from .twitchChannelProvider import TwitchChannelProvider
from ..absTwitchChannelPointRedemptionHandler import AbsTwitchChannelPointRedemptionHandler
from ..api.websocket.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ...channelPointRedemptions.absChannelPointRedemption import AbsChannelPointRedemption
from ...channelPointRedemptions.casualGamePollPointRedemption import CasualGamePollPointRedemption
from ...channelPointRedemptions.cutenessPointRedemption import CutenessPointRedemption
from ...channelPointRedemptions.pkmnBattlePointRedemption import PkmnBattlePointRedemption
from ...channelPointRedemptions.pkmnCatchPointRedemption import PkmnCatchPointRedemption
from ...channelPointRedemptions.pkmnEvolvePointRedemption import PkmnEvolvePointRedemption
from ...channelPointRedemptions.pkmnShinyPointRedemption import PkmnShinyPointRedemption
from ...channelPointRedemptions.shizaPointRedemption import ShizaPointRedemption
from ...channelPointRedemptions.soundAlertPointRedemption import SoundAlertPointRedemption
from ...channelPointRedemptions.stubChannelPointRedemption import StubPointRedemption
from ...channelPointRedemptions.superTriviaGamePointRedemption import SuperTriviaGamePointRedemption
from ...channelPointRedemptions.triviaGamePointRedemption import TriviaGamePointRedemption
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class TwitchChannelPointRedemptionHandler(AbsTwitchChannelPointRedemptionHandler):

    def __init__(
        self,
        casualGamePollPointRedemption: AbsChannelPointRedemption,
        cutenessPointRedemption: AbsChannelPointRedemption,
        pkmnBattlePointRedemption: AbsChannelPointRedemption,
        pkmnCatchPointRedemption: AbsChannelPointRedemption,
        pkmnEvolvePointRedemption: AbsChannelPointRedemption,
        pkmnShinyPointRedemption: AbsChannelPointRedemption,
        shizaPointRedemption: AbsChannelPointRedemption,
        soundAlertPointRedemption: AbsChannelPointRedemption,
        superTriviaGamePointRedemption: AbsChannelPointRedemption,
        triviaGamePointRedemption: AbsChannelPointRedemption,
        timber: TimberInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(casualGamePollPointRedemption, CasualGamePollPointRedemption) and not isinstance(casualGamePollPointRedemption, StubPointRedemption):
            raise TypeError(f'casualGamePollPointRedemption argument is malformed: \"{casualGamePollPointRedemption}\"')
        elif not isinstance(cutenessPointRedemption, CutenessPointRedemption) and not isinstance(cutenessPointRedemption, StubPointRedemption):
            raise TypeError(f'cutenessPointRedemption argument is malformed: \"{cutenessPointRedemption}\"')
        elif not isinstance(pkmnBattlePointRedemption, PkmnBattlePointRedemption) and not isinstance(pkmnBattlePointRedemption, StubPointRedemption):
            raise TypeError(f'pkmnBattlePointRedemption argument is malformed: \"{pkmnBattlePointRedemption}\"')
        elif not isinstance(pkmnCatchPointRedemption, PkmnCatchPointRedemption) and not isinstance(pkmnCatchPointRedemption, StubPointRedemption):
            raise TypeError(f'pkmnCatchPointRedemption argument is malformed: \"{pkmnCatchPointRedemption}\"')
        elif not isinstance(pkmnEvolvePointRedemption, PkmnEvolvePointRedemption) and not isinstance(pkmnEvolvePointRedemption, StubPointRedemption):
            raise TypeError(f'pkmnEvolvePointRedemption argument is malformed: \"{pkmnEvolvePointRedemption}\"')
        elif not isinstance(pkmnShinyPointRedemption, PkmnShinyPointRedemption) and not isinstance(pkmnShinyPointRedemption, StubPointRedemption):
            raise TypeError(f'pkmnShinyPointRedemption argument is malformed: \"{pkmnShinyPointRedemption}\"')
        elif not isinstance(shizaPointRedemption, ShizaPointRedemption) and not isinstance(shizaPointRedemption, StubPointRedemption):
            raise TypeError(f'shizaPointRedemption argument is malformed: \"{shizaPointRedemption}\"')
        elif not isinstance(soundAlertPointRedemption, SoundAlertPointRedemption) and not isinstance(soundAlertPointRedemption, StubPointRedemption):
            raise TypeError(f'soundAlertPointRedemption argument is malformed: \"{soundAlertPointRedemption}\"')
        elif not isinstance(superTriviaGamePointRedemption, SuperTriviaGamePointRedemption) and not isinstance(superTriviaGamePointRedemption, StubPointRedemption):
            raise TypeError(f'superTriviaGamePointRedemption argument is malformed: \"{superTriviaGamePointRedemption}\"')
        elif not isinstance(triviaGamePointRedemption, TriviaGamePointRedemption) and not isinstance(triviaGamePointRedemption, StubPointRedemption):
            raise TypeError(f'triviaGamePointRedemption argument is malformed: \"{triviaGamePointRedemption}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__casualGamePollPointRedemption: AbsChannelPointRedemption = casualGamePollPointRedemption
        self.__cutenessPointRedemption: AbsChannelPointRedemption = cutenessPointRedemption
        self.__pkmnBattlePointRedemption: AbsChannelPointRedemption = pkmnBattlePointRedemption
        self.__pkmnCatchPointRedemption: AbsChannelPointRedemption = pkmnCatchPointRedemption
        self.__pkmnEvolvePointRedemption: AbsChannelPointRedemption = pkmnEvolvePointRedemption
        self.__pkmnShinyPointRedemption: AbsChannelPointRedemption = pkmnShinyPointRedemption
        self.__shizaPointRedemption: AbsChannelPointRedemption = shizaPointRedemption
        self.__soundAlertPointRedemption: AbsChannelPointRedemption = soundAlertPointRedemption
        self.__superTriviaGamePointRedemption: AbsChannelPointRedemption = superTriviaGamePointRedemption
        self.__triviaGamePointRedemption: AbsChannelPointRedemption = triviaGamePointRedemption
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
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that has no event (channel=\"{user.getHandle()}\") ({dataBundle=})')
            return

        eventId = dataBundle.metadata.messageId
        reward = event.reward
        redemptionUserId = event.userId
        redemptionUserInput = event.userInput
        redemptionUserLogin = event.userLogin

        if not utils.isValidStr(eventId) or reward is None or not utils.isValidStr(redemptionUserId) or not utils.isValidStr(redemptionUserLogin):
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that is missing crucial data: ({eventId=}) ({reward=}) ({redemptionUserId=}) ({redemptionUserInput=}) ({redemptionUserLogin=})')
            return

        self.__timber.log('TwitchChannelPointRedemptionHandler', f'Channel point reward ({reward}) redeemed by {redemptionUserLogin}:{redemptionUserId} in {user.getHandle()}:{userId} ({redemptionUserInput=})')

        await self.__userIdsRepository.setUser(
            userId = redemptionUserId,
            userName = redemptionUserLogin
        )

        channelPointsMessage = TwitchChannelPointsMessage(
            eventId = eventId,
            redemptionMessage = redemptionUserInput,
            rewardId = reward.rewardId,
            twitchUser = user,
            userId = redemptionUserId,
            userName = redemptionUserLogin
        )

        twitchChannelProvider = self.__twitchChannelProvider

        if twitchChannelProvider is None:
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Abandoning handling of this channel point redemption as no TwitchChannelProvider has been set: \"{twitchChannelProvider}\"')
            return

        twitchChannel = await twitchChannelProvider.getTwitchChannel(user.getHandle())

        if user.isCasualGamePollEnabled() and channelPointsMessage.getRewardId() == user.getCasualGamePollRewardId():
            if await self.__casualGamePollPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.isCutenessEnabled() and user.hasCutenessBoosterPacks():
            if await self.__cutenessPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.isPkmnEnabled():
            if channelPointsMessage.getRewardId() == user.getPkmnBattleRewardId():
                if await self.__pkmnBattlePointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

            if user.hasPkmnCatchBoosterPacks():
                if await self.__pkmnCatchPointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

            if channelPointsMessage.getRewardId() == user.getPkmnEvolveRewardId():
                if await self.__pkmnEvolvePointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

            if channelPointsMessage.getRewardId() == user.getPkmnShinyRewardId():
                if await self.__pkmnShinyPointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

        if user.isShizaMessageEnabled and channelPointsMessage.getRewardId() == user.shizaMessageRewardId:
            if await self.__shizaPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.isTriviaGameEnabled() and channelPointsMessage.getRewardId() == user.getTriviaGameRewardId():
            if await self.__triviaGamePointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.isSuperTriviaGameEnabled() and channelPointsMessage.getRewardId() == user.getSuperTriviaGameRewardId():
            if await self.__superTriviaGamePointRedemption.handlePointRedemption(
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

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
