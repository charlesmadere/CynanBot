import math
import random
from typing import Final

from .twitchChannelProvider import TwitchChannelProvider
from ..absTwitchSubscriptionHandler import AbsTwitchSubscriptionHandler
from ..api.models.twitchCommunitySubGift import TwitchCommunitySubGift
from ..api.models.twitchResub import TwitchResub
from ..api.models.twitchSubGift import TwitchSubGift
from ..api.models.twitchSubscriberTier import TwitchSubscriberTier
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ..emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from ..officialAccounts.officialTwitchAccountUserIdProviderInterface import OfficialTwitchAccountUserIdProviderInterface
from ..tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitchUtilsInterface import TwitchUtilsInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundAlert import SoundAlert
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from ...trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ...tts.models.ttsEvent import TtsEvent
from ...tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ...tts.models.ttsSubscriptionDonation import TtsSubscriptionDonation
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class TwitchSubscriptionHandler(AbsTwitchSubscriptionHandler):

    def __init__(
        self,
        officialTwitchAccountUserIdProvider: OfficialTwitchAccountUserIdProviderInterface,
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
        if not isinstance(officialTwitchAccountUserIdProvider, OfficialTwitchAccountUserIdProviderInterface):
            raise TypeError(f'officialTwitchAccountUserIdProvider argument is malformed: \"{officialTwitchAccountUserIdProvider}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
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

        self.__officialTwitchAccountUserIdProvider: Final[OfficialTwitchAccountUserIdProviderInterface] = officialTwitchAccountUserIdProvider
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameBuilder: Final[TriviaGameBuilderInterface | None] = triviaGameBuilder
        self.__triviaGameMachine: Final[TriviaGameMachineInterface | None] = triviaGameMachine
        self.__twitchEmotesHelper: Final[TwitchEmotesHelperInterface] = twitchEmotesHelper
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __handleSubscription(
        self,
        isAnonymous: bool | None,
        isGift: bool | None,
        total: int | None,
        broadcasterUserId: str,
        chatMessage: str | None,
        eventUserId: str,
        eventUserLogin: str,
        eventUserName: str,
        userInput: str | None,
        communitySubGift: TwitchCommunitySubGift | None,
        resub: TwitchResub | None,
        subGift: TwitchSubGift | None,
        tier: TwitchSubscriberTier,
        subscriptionType: TwitchWebsocketSubscriptionType,
        user: UserInterface
    ):
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
                chatMessage = chatMessage,
                eventUserId = eventUserId,
                eventUserName = eventUserLogin,
                userInput = userInput,
                communitySubGift = communitySubGift,
                resub = resub,
                subGift = subGift,
                tier = tier,
                subscriptionType = subscriptionType,
                user = user
            )

    async def onNewSubscriptionDataBundle(
        self,
        broadcasterUserId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        if not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        payload = dataBundle.requirePayload()
        event = payload.event
        subscription = payload.subscription

        if event is None or subscription is None:
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that has no event ({user=}) ({dataBundle=})')
            return

        subscriptionType = subscription.subscriptionType
        isAnonymous = event.isAnonymous
        isGift = event.isGift
        total = event.total
        communitySubGift = event.communitySubGift
        chatMessage = event.message
        eventId = event.eventId
        resub = event.resub
        subGift = event.subGift
        eventUserId = event.userId
        eventUserLogin = event.userLogin
        eventUserName = event.userName
        userInput = event.userInput
        tier = event.tier

        if not utils.isValidStr(eventUserId) or not utils.isValidStr(eventUserLogin) or not utils.isValidStr(eventUserName) or tier is None:
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({dataBundle=}) ({subscriptionType=}) ({isAnonymous=}) ({isGift=}) ({communitySubGift=}) ({resub=}) ({subGift=}) ({total=}) ({chatMessage=}) ({broadcasterUserId=}) ({eventId=}) ({eventUserId=}) ({eventUserLogin=}) ({eventUserName=}) ({userInput=}) ({tier=})')
            return

        await self.__handleSubscription(
            isAnonymous = isAnonymous,
            isGift = isGift,
            total = total,
            broadcasterUserId = broadcasterUserId,
            chatMessage = chatMessage,
            eventUserId = eventUserId,
            eventUserLogin = eventUserLogin,
            eventUserName = eventUserName,
            userInput = userInput,
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

        await self.__twitchUtils.waitThenSend(
            messageable = twitchChannel,
            delaySeconds = 3,
            message = f'{emoji1} thanks for the sub!!! {emoji2}'
        )

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
        chatMessage: str | None,
        eventUserId: str | None,
        eventUserName: str | None,
        userInput: str | None,
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

        actualMessage = chatMessage
        if not utils.isValidStr(actualMessage):
            actualMessage = userInput

        if isAnonymous is None:
            if resub is not None and resub.gifterIsAnonymous is True:
                isAnonymous = True
            else:
                isAnonymous = False

        actualUserId = eventUserId
        actualUserName = eventUserName

        if not utils.isValidStr(actualUserId) or not utils.isValidStr(actualUserName):
            if isAnonymous:
                twitchAccessToken = await self.__twitchTokensUtils.requireAccessTokenByIdOrFallback(
                    twitchChannelId = broadcasterUserId
                )

                actualUserId = await self.__officialTwitchAccountUserIdProvider.getTwitchAnonymousGifterUserId()

                actualUserName = await self.__userIdsRepository.requireUserName(
                    userId = actualUserId,
                    twitchAccessToken = twitchAccessToken
                )
            else:
                self.__timber.log('TwitchSubscriptionHandler', f'Attempted to process subscription event into a TTS message, but data is weird? ({isAnonymous=}) ({isGift=}) ({eventUserId=}) ({eventUserName=}) ({communitySubGift=}) ({resub=}) ({subscriptionType=})')
                return

        if total is None and communitySubGift is not None:
            total = communitySubGift.total

        cumulativeMonths: int | None = None
        durationMonths: int | None = None

        if resub is not None:
            cumulativeMonths = resub.cumulativeMonths
            durationMonths = resub.durationMonths

        providerOverridableStatus: TtsProviderOverridableStatus

        if user.isChatterPreferredTtsEnabled:
            providerOverridableStatus = TtsProviderOverridableStatus.CHATTER_OVERRIDABLE
        else:
            providerOverridableStatus = TtsProviderOverridableStatus.TWITCH_CHANNEL_DISABLED

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.SUBSCRIBE,
            twitchChannel = user.handle,
            twitchChannelId = broadcasterUserId,
            ttsEvent = TtsEvent(
                message = actualMessage,
                twitchChannel = user.handle,
                twitchChannelId = broadcasterUserId,
                userId = actualUserId,
                userName = actualUserName,
                donation = TtsSubscriptionDonation(
                    isAnonymous = isAnonymous,
                    cumulativeMonths = cumulativeMonths,
                    durationMonths = durationMonths,
                    numberOfGiftedSubs = total,
                    tier = tier
                ),
                provider = user.defaultTtsProvider,
                providerOverridableStatus = providerOverridableStatus,
                raidInfo = None
            )
        ))

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
