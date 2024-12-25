import math
import random
import traceback

from .twitchChannelProvider import TwitchChannelProvider
from ..absTwitchSubscriptionHandler import AbsTwitchSubscriptionHandler
from ..api.twitchCommunitySubGift import TwitchCommunitySubGift
from ..api.twitchResub import TwitchResub
from ..api.twitchSubGift import TwitchSubGift
from ..api.twitchSubscriberTier import TwitchSubscriberTier
from ..api.websocket.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.websocket.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ..emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from ..twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..twitchUtilsInterface import TwitchUtilsInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...soundPlayerManager.soundAlert import SoundAlert
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from ...trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ...tts.ttsEvent import TtsEvent
from ...tts.ttsSubscriptionDonation import TtsSubscriptionDonation
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class TwitchSubscriptionHandler(AbsTwitchSubscriptionHandler):

    def __init__(
        self,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface | None,
        triviaGameMachine: TriviaGameMachineInterface | None,
        twitchEmotesHelper: TwitchEmotesHelperInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif triviaGameBuilder is not None and not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise TypeError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif triviaGameMachine is not None and not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(twitchEmotesHelper, TwitchEmotesHelperInterface):
            raise TypeError(f'twitchEmotesHelper argument is malformed: \"{twitchEmotesHelper}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__triviaGameBuilder: TriviaGameBuilderInterface | None = triviaGameBuilder
        self.__triviaGameMachine: TriviaGameMachineInterface | None = triviaGameMachine
        self.__twitchEmotesHelper: TwitchEmotesHelperInterface = twitchEmotesHelper
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTokensUtils: TwitchTokensUtilsInterface = twitchTokensUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __isRedundantSubscriptionAlert(
        self,
        isGift: bool | None,
        subscriptionType: TwitchWebsocketSubscriptionType
    ) -> bool:
        # This method intends to prevent an annoying situation where some subscription events end
        # up causing two distinct subscription event alerts to come from Twitch, where both are
        # just subtly different yet each inform of the same new subscriber/subscription event.

        if isGift is False and subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIBE or \
                isGift is None and subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIBE or \
                isGift is None and subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT:
            return True

        return False

    async def onNewSubscription(
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

        payload = dataBundle.requirePayload()
        event = payload.event
        subscription = payload.subscription

        if event is None or subscription is None:
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that has no event (channel=\"{user.handle}\") ({dataBundle=})')
            return

        subscriptionType = subscription.subscriptionType
        isAnonymous = event.isAnonymous
        isGift = event.isGift
        communitySubGift = event.communitySubGift
        message = event.message
        broadcasterUserId = event.broadcasterUserId
        eventId = event.eventId
        resub = event.resub
        subGift = event.subGift
        total = event.total
        eventUserId = event.userId
        eventUserInput = event.userInput
        eventUserLogin = event.userLogin
        eventUserName = event.userName
        tier = event.tier

        if not utils.isValidStr(broadcasterUserId) or tier is None:
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.handle}\") ({dataBundle=}) ({subscriptionType=}) ({isAnonymous=}) ({isGift=}) ({communitySubGift=}) ({resub=}) ({subGift=}) ({total=}) ({message=}) ({broadcasterUserId=}) ({eventId=}) ({eventUserId=}) ({eventUserInput=}) ({eventUserLogin=}) ({eventUserName=}) ({tier=})')
            return

        self.__timber.log('TwitchSubscriptionHandler', f'Received a subscription event: (channel=\"{user.handle}\") ({dataBundle=}) ({subscriptionType=}) ({isAnonymous=}) ({isGift=}) ({communitySubGift=}) ({resub=}) ({subGift=}) ({total=}) ({message=}) ({broadcasterUserId=}) ({eventId=}) ({eventUserId=}) ({eventUserInput=}) ({eventUserLogin=}) ({eventUserName=}) ({tier=})')

        if user.isSubGiftThankingEnabled:
            await self.__processCynanBotAsGiftRecipient(
                broadcasterUserId = broadcasterUserId,
                eventUserId = eventUserId,
                subGift = subGift,
                subscriptionType = subscriptionType,
                user = user
            )

        if user.isSuperTriviaGameEnabled:
            await self.__processSuperTriviaEvent(
                broadcasterUserId = broadcasterUserId,
                communitySubGift = communitySubGift,
                subscriptionType = subscriptionType,
                user = user
            )

        if user.isTtsEnabled:
            await self.__processTtsEvent(
                isAnonymous = isAnonymous,
                isGift = isGift,
                total = total,
                broadcasterUserId = broadcasterUserId,
                message = message,
                userId = eventUserId,
                userInput = eventUserInput,
                userName = eventUserName,
                communitySubGift = communitySubGift,
                resub = resub,
                subGift = subGift,
                tier = tier,
                subscriptionType = subscriptionType,
                user = user
            )

    async def __processCynanBotAsGiftRecipient(
        self,
        broadcasterUserId: str,
        eventUserId: str,
        subGift: TwitchSubGift | None,
        subscriptionType: TwitchWebsocketSubscriptionType,
        user: UserInterface
    ):
        if not user.isSubGiftThankingEnabled:
            return

        twitchChannelProvider = self.__twitchChannelProvider
        if twitchChannelProvider is None:
            return

        recipientUserId: str

        if subGift is None:
            recipientUserId = eventUserId
        else:
            recipientUserId = subGift.recipientUserId

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchId = await self.__userIdsRepository.fetchUserId(twitchHandle)

        if not utils.isValidStr(twitchId) or twitchId != recipientUserId:
            return

        viableEmoteNames = await self.__twitchEmotesHelper.fetchViableSubscriptionEmoteNames(
            twitchChannelId = broadcasterUserId
        )

        allViableEmotes: set[str] = { 'KomodoHype' }
        allViableEmotes.update(viableEmoteNames)

        viableEmotesList: list[str] = list(allViableEmotes)
        emoji1 = random.choice(viableEmotesList)
        emoji2 = random.choice(viableEmotesList)

        twitchChannel = await twitchChannelProvider.getTwitchChannel(user.handle)
        await self.__twitchUtils.safeSend(twitchChannel, f'{emoji1} thanks for the sub!!! {emoji2}')
        self.__timber.log('TwitchSubscriptionHandler', f'Received and thanked in {user.handle} for a gifted sub! ({broadcasterUserId=}) ({eventUserId=}) ({subGift=}) ({subscriptionType=}) ({user=})')

    async def __processSuperTriviaEvent(
        self,
        broadcasterUserId: str,
        communitySubGift: TwitchCommunitySubGift | None,
        subscriptionType: TwitchWebsocketSubscriptionType,
        user: UserInterface
    ):
        triviaGameBuilder = self.__triviaGameBuilder
        triviaGameMachine = self.__triviaGameMachine

        if triviaGameBuilder is None or triviaGameMachine is None:
            return
        elif not user.isSuperTriviaGameEnabled:
            return
        elif subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIBE:
            return

        superTriviaSubscribeTriggerAmount = user.superTriviaSubscribeTriggerAmount
        superTriviaSubscribeTriggerMaximum = user.superTriviaSubscribeTriggerMaximum

        if not utils.isValidNum(superTriviaSubscribeTriggerAmount) or superTriviaSubscribeTriggerAmount <= 0:
            return

        numberOfSubs = 1
        if communitySubGift is not None:
            numberOfSubs = communitySubGift.total

        numberOfGames = int(math.floor(numberOfSubs / superTriviaSubscribeTriggerAmount))

        if numberOfGames < 1:
            return
        elif utils.isValidInt(superTriviaSubscribeTriggerMaximum) and numberOfGames > superTriviaSubscribeTriggerMaximum:
            numberOfGames = superTriviaSubscribeTriggerMaximum

        action = await triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.handle,
            twitchChannelId = broadcasterUserId,
            numberOfGames = numberOfGames
        )

        if action is not None:
            triviaGameMachine.submitAction(action)

    async def __processTtsEvent(
        self,
        isAnonymous: bool | None,
        isGift: bool | None,
        total: int | None,
        broadcasterUserId: str,
        message: str | None,
        userId: str | None,
        userInput: str | None,
        userName: str | None,
        communitySubGift: TwitchCommunitySubGift | None,
        resub: TwitchResub | None,
        subGift: TwitchSubGift | None,
        tier: TwitchSubscriberTier,
        subscriptionType: TwitchWebsocketSubscriptionType,
        user: UserInterface,
    ):
        if not user.isTtsEnabled:
            return
        elif isGift is True:
            # Community gift sub bombs will send out an event where this is true for every single
            # individual person who received a gifted sub. We don't want to do a TTS alert for all
            # users who received a gifted sub, so we're going to return here.
            return
        elif await self.__isRedundantSubscriptionAlert(
            isGift = isGift,
            subscriptionType = subscriptionType
        ):
            self.__timber.log('TwitchSubscriptionHandler', f'Encountered redundant subscription alert event ({isGift=}) ({total=}) ({communitySubGift=}) ({resub=}) ({subGift=}) ({subscriptionType=}) ({user=})')
            return

        actualMessage = message
        if not utils.isValidStr(actualMessage):
            actualMessage = userInput

        if isAnonymous is None:
            if resub is not None and resub.gifterIsAnonymous is True:
                isAnonymous = True
            else:
                isAnonymous = False

        actualUserId = userId
        actualUserName = userName

        if not utils.isValidStr(actualUserId) or not utils.isValidStr(actualUserName):
            if isAnonymous:
                twitchAccessToken = await self.__twitchTokensUtils.requireAccessTokenByIdOrFallback(
                    twitchChannelId = broadcasterUserId
                )

                actualUserId = await self.__userIdsRepository.requireAnonymousUserId()

                actualUserName = await self.__userIdsRepository.requireAnonymousUserName(
                    twitchAccessToken = twitchAccessToken
                )
            else:
                self.__timber.log('TwitchSubscriptionHandler', f'Attempted to process subscription event into a TTS message, but data is weird? ({isAnonymous=}) ({isGift=}) ({userId=}) ({userName=}) ({communitySubGift=}) ({subscriptionType=})')
                return

        if total is None and communitySubGift is not None:
            total = communitySubGift.total

        cumulativeMonths: int | None = None
        durationMonths: int | None = None

        if resub is not None:
            cumulativeMonths = resub.cumulativeMonths
            durationMonths = resub.durationMonths

        donation = TtsSubscriptionDonation(
            isAnonymous = isAnonymous,
            cumulativeMonths = cumulativeMonths,
            durationMonths = durationMonths,
            numberOfGiftedSubs = total,
            tier = tier
        )

        ttsEvent = TtsEvent(
            message = actualMessage,
            twitchChannel = user.handle,
            twitchChannelId = broadcasterUserId,
            userId = actualUserId,
            userName = actualUserName,
            donation = donation,
            provider = user.defaultTtsProvider,
            raidInfo = None
        )

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.SUBSCRIBE,
            twitchChannel = user.handle,
            twitchChannelId = broadcasterUserId,
            ttsEvent = ttsEvent
        ))

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
