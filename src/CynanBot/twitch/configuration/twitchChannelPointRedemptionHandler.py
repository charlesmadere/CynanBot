import CynanBot.misc.utils as utils
from CynanBot.channelPointRedemptions.absChannelPointRedemption import \
    AbsChannelPointRedemption
from CynanBot.channelPointRedemptions.casualGamePollPointRedemption import \
    CasualGamePollPointRedemption
from CynanBot.channelPointRedemptions.cutenessPointRedemption import \
    CutenessPointRedemption
from CynanBot.channelPointRedemptions.pkmnBattlePointRedemption import \
    PkmnBattlePointRedemption
from CynanBot.channelPointRedemptions.pkmnCatchPointRedemption import \
    PkmnCatchPointRedemption
from CynanBot.channelPointRedemptions.pkmnEvolvePointRedemption import \
    PkmnEvolvePointRedemption
from CynanBot.channelPointRedemptions.pkmnShinyPointRedemption import \
    PkmnShinyPointRedemption
from CynanBot.channelPointRedemptions.soundAlertPointRedemption import \
    SoundAlertPointRedemption
from CynanBot.channelPointRedemptions.stubChannelPointRedemption import \
    StubPointRedemption
from CynanBot.channelPointRedemptions.superTriviaGamePointRedemption import \
    SuperTriviaGamePointRedemption
from CynanBot.channelPointRedemptions.triviaGamePointRedemption import \
    TriviaGamePointRedemption
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.absTwitchChannelPointRedemptionHandler import \
    AbsTwitchChannelPointRedemptionHandler
from CynanBot.twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from CynanBot.twitch.configuration.twitchChannelPointsMessage import \
    TwitchChannelPointsMessage
from CynanBot.twitch.configuration.twitchChannelProvider import \
    TwitchChannelProvider
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.userInterface import UserInterface


class TwitchChannelPointRedemptionHandler(AbsTwitchChannelPointRedemptionHandler):

    def __init__(
        self,
        casualGamePollPointRedemption: AbsChannelPointRedemption,
        cutenessPointRedemption: AbsChannelPointRedemption,
        pkmnBattlePointRedemption: AbsChannelPointRedemption,
        pkmnCatchPointRedemption: AbsChannelPointRedemption,
        pkmnEvolvePointRedemption: AbsChannelPointRedemption,
        pkmnShinyPointRedemption: AbsChannelPointRedemption,
        soundAlertPointRedemption: AbsChannelPointRedemption,
        superTriviaGamePointRedemption: AbsChannelPointRedemption,
        triviaGamePointRedemption: AbsChannelPointRedemption,
        timber: TimberInterface,
        twitchChannelProvider: TwitchChannelProvider,
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
        elif not isinstance(soundAlertPointRedemption, SoundAlertPointRedemption) and not isinstance(soundAlertPointRedemption, StubPointRedemption):
            raise TypeError(f'soundAlertPointRedemption argument is malformed: \"{soundAlertPointRedemption}\"')
        elif not isinstance(superTriviaGamePointRedemption, SuperTriviaGamePointRedemption) and not isinstance(superTriviaGamePointRedemption, StubPointRedemption):
            raise TypeError(f'superTriviaGamePointRedemption argument is malformed: \"{superTriviaGamePointRedemption}\"')
        elif not isinstance(triviaGamePointRedemption, TriviaGamePointRedemption) and not isinstance(triviaGamePointRedemption, StubPointRedemption):
            raise TypeError(f'triviaGamePointRedemption argument is malformed: \"{triviaGamePointRedemption}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise TypeError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__casualGamePollPointRedemption: AbsChannelPointRedemption = casualGamePollPointRedemption
        self.__cutenessPointRedemption: AbsChannelPointRedemption = cutenessPointRedemption
        self.__pkmnBattlePointRedemption: AbsChannelPointRedemption = pkmnBattlePointRedemption
        self.__pkmnCatchPointRedemption: AbsChannelPointRedemption = pkmnCatchPointRedemption
        self.__pkmnEvolvePointRedemption: AbsChannelPointRedemption = pkmnEvolvePointRedemption
        self.__pkmnShinyPointRedemption: AbsChannelPointRedemption = pkmnShinyPointRedemption
        self.__soundAlertPointRedemption: AbsChannelPointRedemption = soundAlertPointRedemption
        self.__superTriviaGamePointRedemption: AbsChannelPointRedemption = superTriviaGamePointRedemption
        self.__triviaGamePointRedemption: AbsChannelPointRedemption = triviaGamePointRedemption
        self.__timber: TimberInterface = timber
        self.__twitchChannelProvider: TwitchChannelProvider = twitchChannelProvider
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

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
        reward = event.getReward()
        redemptionUserId = event.getUserId()
        redemptionUserInput = event.getUserInput()
        redemptionUserLogin = event.getUserLogin()

        if not utils.isValidStr(eventId) or reward is None or not utils.isValidStr(redemptionUserId) or not utils.isValidStr(redemptionUserLogin):
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that is missing crucial data: ({eventId=}) ({reward=}) ({redemptionUserId=}) ({redemptionUserInput=}) ({redemptionUserLogin=})')
            return

        self.__timber.log('TwitchChannelPointRedemptionHandler', f'Channel point reward ({reward}) redeemed by {redemptionUserLogin}:{redemptionUserId} in {user.getHandle()}:{userId} ({redemptionUserInput=})')

        await self.__userIdsRepository.setUser(
            userId = redemptionUserId,
            userName = redemptionUserLogin
        )

        twitchChannel = await self.__twitchChannelProvider.getTwitchChannel(user.getHandle())

        channelPointsMessage = TwitchChannelPointsMessage(
            eventId = eventId,
            redemptionMessage = redemptionUserInput,
            rewardId = reward.rewardId,
            twitchUser = user,
            userId = redemptionUserId,
            userName = redemptionUserLogin
        )

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

        if user.areSoundAlertsEnabled() and channelPointsMessage.getRewardId() == user.getSoundAlertRewardId():
            if await self.__soundAlertPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return
