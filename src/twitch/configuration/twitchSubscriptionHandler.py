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
from ...tts.ttsDonation import TtsDonation
from ...tts.ttsEvent import TtsEvent
from ...tts.ttsProvider import TtsProvider
from ...tts.ttsSubscriptionDonation import TtsSubscriptionDonation
from ...tts.ttsSubscriptionDonationGiftType import TtsSubscriptionDonationGiftType
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class TwitchSubscriptionHandler(AbsTwitchSubscriptionHandler):

    def __init__(
        self,
        streamAlertsManager: StreamAlertsManagerInterface | None,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface | None,
        triviaGameMachine: TriviaGameMachineInterface | None,
        twitchEmotesHelper: TwitchEmotesHelperInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if streamAlertsManager is not None and not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
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

        self.__streamAlertsManager: StreamAlertsManagerInterface | None = streamAlertsManager
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
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that has no event (channel=\"{user.getHandle()}\") ({dataBundle=})')
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
        eventUserId = event.userId
        eventUserInput = event.userInput
        eventUserLogin = event.userLogin
        eventUserName = event.userName
        tier = event.tier

        if not utils.isValidStr(broadcasterUserId) or tier is None:
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({subscriptionType=}) ({isAnonymous=}) ({isGift=}) ({communitySubGift=}) ({resub=}) ({subGift=}) ({message=}) ({broadcasterUserId=}) ({eventId=}) ({eventUserId=}) ({eventUserInput=}) ({eventUserLogin=}) ({eventUserName=}) ({tier=})')
            return

        self.__timber.log('TwitchSubscriptionHandler', f'Received a subscription event: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({subscriptionType=}) ({isAnonymous=}) ({isGift=}) ({communitySubGift=}) ({resub=}) ({subGift=}) ({message=}) ({broadcasterUserId=}) ({eventId=}) ({eventUserId=}) ({eventUserInput=}) ({eventUserLogin=}) ({eventUserName=}) ({tier=})')

        if user.isSubGiftThankingEnabled and subGift is not None:
            await self.__processCynanBotAsGiftRecipient(
                broadcasterUserId = broadcasterUserId,
                subGift = subGift,
                user = user
            )

        if user.isSuperTriviaGameEnabled():
            await self.__processSuperTriviaEvent(
                broadcasterUserId = broadcasterUserId,
                communitySubGift = communitySubGift,
                tier = tier,
                subscriptionType = subscriptionType,
                user = user
            )

        if user.isTtsEnabled():
            await self.__processTtsEvent(
                isAnonymous = isAnonymous,
                isGift = isGift,
                broadcasterUserId = broadcasterUserId,
                message = message,
                userId = eventUserId,
                userInput = eventUserInput,
                userLogin = eventUserLogin,
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
        subGift: TwitchSubGift,
        user: UserInterface
    ):
        if not user.isSubGiftThankingEnabled:
            return

        twitchChannelProvider = self.__twitchChannelProvider
        if twitchChannelProvider is None:
            return

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchId = await self.__userIdsRepository.fetchUserId(twitchHandle)

        if not utils.isValidStr(twitchId) or twitchId != subGift.recipientUserId:
            return

        allViableEmotes: set[str] = { 'KomodoHype' }

        try:
            channelSpecificViableEmotes = await self.__twitchEmotesHelper.fetchViableSubscriptionEmoteNames(
                twitchChannelId = broadcasterUserId
            )
            allViableEmotes.update(channelSpecificViableEmotes)
        except GenericNetworkException as e:
            self.__timber.log('TwitchSubscriptionHandler', f'Failed to fetch viable Twitch emote names ({broadcasterUserId=}) ({subGift=}) ({user=}): {e}', e, traceback.format_exc())

        viableEmotesList: list[str] = list(allViableEmotes)
        emoji1 = random.choice(viableEmotesList)
        emoji2 = random.choice(viableEmotesList)

        twitchChannel = await twitchChannelProvider.getTwitchChannel(user.getHandle())
        await self.__twitchUtils.safeSend(twitchChannel, f'{emoji1} thanks for the sub @{subGift.recipientUserLogin} {emoji2}')
        self.__timber.log('TwitchSubscriptionHandler', f'Thanked {subGift.recipientUserId}:{subGift.recipientUserLogin} in {user.getHandle()} for a gifted sub!')

    async def __processSuperTriviaEvent(
        self,
        broadcasterUserId: str,
        communitySubGift: TwitchCommunitySubGift | None,
        tier: TwitchSubscriberTier,
        subscriptionType: TwitchWebsocketSubscriptionType,
        user: UserInterface
    ):
        if not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif communitySubGift is not None and not isinstance(communitySubGift, TwitchCommunitySubGift):
            raise TypeError(f'communitySubGift argument is malformed: \"{communitySubGift}\"')
        elif not isinstance(tier, TwitchSubscriberTier):
            raise TypeError(f'tier argument is malformed: \"{tier}\"')
        elif not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        triviaGameBuilder = self.__triviaGameBuilder
        triviaGameMachine = self.__triviaGameMachine

        if triviaGameBuilder is None or triviaGameMachine is None:
            return
        elif not user.isSuperTriviaGameEnabled():
            return
        elif subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIBE:
            return

        superTriviaSubscribeTriggerAmount = user.getSuperTriviaSubscribeTriggerAmount()
        superTriviaSubscribeTriggerMaximum = user.getSuperTriviaSubscribeTriggerMaximum()

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
            twitchChannel = user.getHandle(),
            twitchChannelId = broadcasterUserId,
            numberOfGames = numberOfGames
        )

        if action is not None:
            triviaGameMachine.submitAction(action)

    async def __processTtsEvent(
        self,
        isAnonymous: bool | None,
        isGift: bool | None,
        broadcasterUserId: str,
        message: str | None,
        userId: str | None,
        userInput: str | None,
        userLogin: str | None,
        userName: str | None,
        communitySubGift: TwitchCommunitySubGift | None,
        resub: TwitchResub | None,
        subGift: TwitchSubGift | None,
        tier: TwitchSubscriberTier,
        subscriptionType: TwitchWebsocketSubscriptionType,
        user: UserInterface,
    ):
        if isAnonymous is not None and not utils.isValidBool(isAnonymous):
            raise TypeError(f'isAnonymous argument is malformed: \"{isAnonymous}\"')
        elif isGift is not None and not utils.isValidBool(isGift):
            raise TypeError(f'isGift argument is malformed: \"{isGift}\"')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif userId is not None and not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif userInput is not None and not isinstance(userInput, str):
            raise TypeError(f'userInput argument is malformed: \"{userInput}\"')
        elif userLogin is not None and not utils.isValidStr(userLogin):
            raise TypeError(f'userLogin argument is malformed: \"{userLogin}\"')
        elif userName is not None and not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')
        elif communitySubGift is not None and not isinstance(communitySubGift, TwitchCommunitySubGift):
            raise TypeError(f'communitySubGift argument is malformed: \"{communitySubGift}\"')
        elif resub is not None and not isinstance(resub, TwitchResub):
            raise TypeError(f'resub argument is malformed: \"{resub}\"')
        elif subGift is not None and not isinstance(subGift, TwitchSubGift):
            raise TypeError(f'subGift argument is malformed: \"{subGift}\"')
        elif not isinstance(tier, TwitchSubscriberTier):
            raise TypeError(f'tier argument is malformed: \"{tier}\"')
        elif not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        streamAlertsManager = self.__streamAlertsManager

        if streamAlertsManager is None:
            return
        elif not user.isTtsEnabled():
            return
        elif await self.__isRedundantSubscriptionAlert(
            isGift = isGift,
            subscriptionType = subscriptionType
        ):
            self.__timber.log('TwitchSubscriptionHandler', f'Encountered redundant subscription alert event ({isGift=}) ({communitySubGift=}) ({resub=}) ({subGift=}) ({subscriptionType=}) ({user=})')
            return

        actualMessage = message
        if not utils.isValidStr(actualMessage):
            actualMessage = userInput

        if isAnonymous is None:
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

        giftType: TtsSubscriptionDonationGiftType | None = None

        if isGift is True:
            giftType = TtsSubscriptionDonationGiftType.RECEIVER
        elif subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT:
            giftType = TtsSubscriptionDonationGiftType.GIVER

        donation: TtsDonation = TtsSubscriptionDonation(
            isAnonymous = isAnonymous,
            giftType = giftType,
            tier = tier
        )

        ttsEvent = TtsEvent(
            message = actualMessage,
            twitchChannel = user.getHandle(),
            twitchChannelId = broadcasterUserId,
            userId = actualUserId,
            userName = actualUserName,
            donation = donation,
            provider = TtsProvider.DEC_TALK,
            raidInfo = None
        )

        streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.SUBSCRIBE,
            twitchChannel = user.getHandle(),
            twitchChannelId = broadcasterUserId,
            ttsEvent = ttsEvent
        ))

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
