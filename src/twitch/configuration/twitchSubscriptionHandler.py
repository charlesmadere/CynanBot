import math
import random
from typing import Final

from ..absTwitchSubscriptionHandler import AbsTwitchSubscriptionHandler
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ..chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from ..handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..officialAccounts.officialTwitchAccountUserIdProviderInterface import OfficialTwitchAccountUserIdProviderInterface
from ..tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
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
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchEmotesHelper: TwitchEmotesHelperInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
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
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchEmotesHelper, TwitchEmotesHelperInterface):
            raise TypeError(f'twitchEmotesHelper argument is malformed: \"{twitchEmotesHelper}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__officialTwitchAccountUserIdProvider: Final[OfficialTwitchAccountUserIdProviderInterface] = officialTwitchAccountUserIdProvider
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameBuilder: Final[TriviaGameBuilderInterface | None] = triviaGameBuilder
        self.__triviaGameMachine: Final[TriviaGameMachineInterface | None] = triviaGameMachine
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchEmotesHelper: Final[TwitchEmotesHelperInterface] = twitchEmotesHelper
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

    async def onNewSubscription(self, subscriptionData: AbsTwitchSubscriptionHandler.SubscriptionData):
        if not isinstance(subscriptionData, AbsTwitchSubscriptionHandler.SubscriptionData):
            raise TypeError(f'subscriptionData argument is malformed: \"{subscriptionData}\"')

        user = subscriptionData.user

        if user.isSubGiftThankingEnabled:
            await self.__processCynanBotAsGiftRecipient(subscriptionData)

        if user.isSuperTriviaGameEnabled:
            await self.__processSuperTriviaEvent(subscriptionData)

        if user.isTtsEnabled:
            await self.__processTtsEvent(subscriptionData)

    async def onNewSubscriptionDataBundle(
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
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that has no event ({user=}) ({twitchChannelId=}) ({dataBundle=})')
            return

        eventUserId = event.userId
        eventUserLogin = event.userLogin
        eventUserName = event.userName
        tier = event.tier
        subscriptionType = dataBundle.metadata.subscriptionType

        if not utils.isValidStr(eventUserId) or not utils.isValidStr(eventUserLogin) or not utils.isValidStr(eventUserName) or tier is None or subscriptionType is None:
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({twitchChannelId=}) ({dataBundle=}) ({eventUserId=}) ({eventUserLogin=}) ({eventUserName=}) ({tier=})')
            return

        subscriptionData = AbsTwitchSubscriptionHandler.SubscriptionData(
            isAnonymous = event.isAnonymous,
            isGift = event.isGift,
            total = event.total,
            chatMessage = event.message,
            eventUserId = eventUserId,
            eventUserLogin = eventUserLogin,
            eventUserName = eventUserName,
            twitchChannelId = twitchChannelId,
            communitySubGift = event.communitySubGift,
            resub = event.resub,
            resubscriptionMessage = event.resubscriptionMessage,
            subGift = event.subGift,
            tier = tier,
            subscriptionType = subscriptionType,
            user = user,
        )

        await self.onNewSubscription(
            subscriptionData = subscriptionData,
        )

    async def __processCynanBotAsGiftRecipient(self, subscriptionData: AbsTwitchSubscriptionHandler.SubscriptionData):
        user = subscriptionData.user

        if not user.isSubGiftThankingEnabled:
            return

        recipientUserId: str

        if subscriptionData.subGift is None:
            recipientUserId = subscriptionData.eventUserId
        else:
            recipientUserId = subscriptionData.subGift.recipientUserId

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchId = await self.__userIdsRepository.fetchUserId(twitchHandle)

        if not utils.isValidStr(twitchId) or twitchId != recipientUserId:
            return

        viableEmoteNames = await self.__twitchEmotesHelper.fetchViableSubscriptionEmoteNames(
            twitchChannelId = subscriptionData.twitchChannelId,
        )

        allViableEmotes: set[str] = { 'KomodoHype' }
        allViableEmotes.update(viableEmoteNames)

        viableEmotesList: list[str] = list(allViableEmotes)
        emoji1 = random.choice(viableEmotesList)
        emoji2 = random.choice(viableEmotesList)

        self.__twitchChatMessenger.send(
            text = f'{emoji1} thanks for the sub!!! {emoji2}',
            twitchChannelId = subscriptionData.twitchChannelId,
            delaySeconds = 3,
        )

        self.__timber.log('TwitchSubscriptionHandler', f'Received and thanked in {user.handle} for a gifted sub! ({subscriptionData=})')

    async def __processSuperTriviaEvent(self, subscriptionData: AbsTwitchSubscriptionHandler.SubscriptionData):
        user = subscriptionData.user

        if self.__triviaGameBuilder is None or self.__triviaGameMachine is None:
            return
        elif not user.isSuperTriviaGameEnabled:
            return
        elif subscriptionData.subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIBE:
            return

        superTriviaSubscribeTriggerAmount = user.superTriviaSubscribeTriggerAmount
        superTriviaSubscribeTriggerMaximum = user.superTriviaSubscribeTriggerMaximum

        if superTriviaSubscribeTriggerAmount is None or superTriviaSubscribeTriggerAmount <= 0:
            return

        numberOfSubs = 1
        if subscriptionData.communitySubGift is not None:
            numberOfSubs = subscriptionData.communitySubGift.total

        numberOfGames = int(math.floor(numberOfSubs / superTriviaSubscribeTriggerAmount))

        if numberOfGames < 1:
            return
        elif superTriviaSubscribeTriggerMaximum is not None:
            numberOfGames = min(numberOfGames, superTriviaSubscribeTriggerMaximum)

        action = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.handle,
            twitchChannelId = subscriptionData.twitchChannelId,
            numberOfGames = numberOfGames,
        )

        if action is not None:
            self.__triviaGameMachine.submitAction(action)

    async def __processTtsEvent(self, subscriptionData: AbsTwitchSubscriptionHandler.SubscriptionData):
        user = subscriptionData.user

        if not user.isTtsEnabled:
            return
        elif subscriptionData.isGift is not None and subscriptionData.isGift is True:
            # Community gift sub bombs will send out an event where this is true for every single
            # individual person who received a gifted sub. We don't want to do a TTS alert for all
            # users who received a gifted sub, so we're going to return here.
            return

        isAnonymous = subscriptionData.isAnonymous

        if isAnonymous is None:
            if subscriptionData.resub is not None and subscriptionData.resub.gifterIsAnonymous is True:
                isAnonymous = True
            else:
                isAnonymous = False

        actualUserId = subscriptionData.eventUserId
        actualUserName = subscriptionData.eventUserName

        if not utils.isValidStr(actualUserId) or not utils.isValidStr(actualUserName):
            if isAnonymous:
                twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                    twitchChannelId = subscriptionData.twitchChannelId,
                )

                actualUserId = await self.__officialTwitchAccountUserIdProvider.getTwitchAnonymousGifterUserId()

                actualUserName = await self.__userIdsRepository.requireUserName(
                    userId = actualUserId,
                    twitchAccessToken = twitchAccessToken,
                )
            else:
                self.__timber.log('TwitchSubscriptionHandler', f'Attempted to process subscription event into a TTS message, but data is weird? ({isAnonymous=}) ({subscriptionData=})')
                return

        total = subscriptionData.total

        if total is None and subscriptionData.communitySubGift is not None:
            total = subscriptionData.communitySubGift.total

        cumulativeMonths: int | None = None
        durationMonths: int | None = None

        if subscriptionData.resub is not None:
            cumulativeMonths = subscriptionData.resub.cumulativeMonths
            durationMonths = subscriptionData.resub.durationMonths

        providerOverridableStatus: TtsProviderOverridableStatus

        if user.isChatterPreferredTtsEnabled:
            providerOverridableStatus = TtsProviderOverridableStatus.CHATTER_OVERRIDABLE
        else:
            providerOverridableStatus = TtsProviderOverridableStatus.TWITCH_CHANNEL_DISABLED

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.SUBSCRIBE,
            twitchChannel = user.handle,
            twitchChannelId = subscriptionData.twitchChannelId,
            ttsEvent = TtsEvent(
                message = subscriptionData.chatMessage,
                twitchChannel = user.handle,
                twitchChannelId = subscriptionData.twitchChannelId,
                userId = actualUserId,
                userName = actualUserName,
                donation = TtsSubscriptionDonation(
                    isAnonymous = isAnonymous,
                    cumulativeMonths = cumulativeMonths,
                    durationMonths = durationMonths,
                    numberOfGiftedSubs = total,
                    tier = subscriptionData.tier,
                ),
                provider = user.defaultTtsProvider,
                providerOverridableStatus = providerOverridableStatus,
                raidInfo = None,
            ),
        ))
