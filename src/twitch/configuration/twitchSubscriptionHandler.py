import asyncio
import math
import queue
import random
import traceback
from collections import defaultdict
from dataclasses import dataclass
from queue import SimpleQueue

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
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...network.exceptions import GenericNetworkException
from ...soundPlayerManager.soundAlert import SoundAlert
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from ...trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ...tts.ttsEvent import TtsEvent
from ...tts.ttsSubscriptionDonation import TtsSubscriptionDonation
from ...tts.ttsSubscriptionDonationGiftType import TtsSubscriptionDonationGiftType
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class TwitchSubscriptionHandler(AbsTwitchSubscriptionHandler):

    @dataclass(frozen = True)
    class GiftSub:
        isAnonymous: bool
        receiverUserId: str
        receiverUserName: str
        subGiftGiverUserId: str
        subGiftGiverUserName: str
        twitchChannelId: str
        giftType: TtsSubscriptionDonationGiftType
        tier: TwitchSubscriberTier
        user: UserInterface

        @property
        def twitchChannel(self) -> str:
            return self.user.handle

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface | None,
        triviaGameMachine: TriviaGameMachineInterface | None,
        twitchEmotesHelper: TwitchEmotesHelperInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        sleepTimeSeconds: float = 3
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
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
        elif not utils.isValidNum(sleepTimeSeconds):
            raise TypeError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 1 or sleepTimeSeconds > 60:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__triviaGameBuilder: TriviaGameBuilderInterface | None = triviaGameBuilder
        self.__triviaGameMachine: TriviaGameMachineInterface | None = triviaGameMachine
        self.__twitchEmotesHelper: TwitchEmotesHelperInterface = twitchEmotesHelper
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTokensUtils: TwitchTokensUtilsInterface = twitchTokensUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__sleepTimeSeconds: float = sleepTimeSeconds

        self.__isStarted: bool = False
        self.__giftSubQueue: SimpleQueue[TwitchSubscriptionHandler.GiftSub] = SimpleQueue()
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
        eventUserId = event.userId
        eventUserInput = event.userInput
        eventUserLogin = event.userLogin
        eventUserName = event.userName
        tier = event.tier

        if not utils.isValidStr(broadcasterUserId) or tier is None:
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.handle}\") ({dataBundle=}) ({subscriptionType=}) ({isAnonymous=}) ({isGift=}) ({communitySubGift=}) ({resub=}) ({subGift=}) ({message=}) ({broadcasterUserId=}) ({eventId=}) ({eventUserId=}) ({eventUserInput=}) ({eventUserLogin=}) ({eventUserName=}) ({tier=})')
            return

        self.__timber.log('TwitchSubscriptionHandler', f'Received a subscription event: (channel=\"{user.handle}\") ({dataBundle=}) ({subscriptionType=}) ({isAnonymous=}) ({isGift=}) ({communitySubGift=}) ({resub=}) ({subGift=}) ({message=}) ({broadcasterUserId=}) ({eventId=}) ({eventUserId=}) ({eventUserInput=}) ({eventUserLogin=}) ({eventUserName=}) ({tier=})')

        if user.isSubGiftThankingEnabled and subGift is not None:
            await self.__processCynanBotAsGiftRecipient(
                broadcasterUserId = broadcasterUserId,
                subGift = subGift,
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

        twitchChannel = await twitchChannelProvider.getTwitchChannel(user.handle)
        await self.__twitchUtils.safeSend(twitchChannel, f'{emoji1} thanks for the sub @{subGift.recipientUserLogin} {emoji2}')
        self.__timber.log('TwitchSubscriptionHandler', f'Thanked {subGift.recipientUserId}:{subGift.recipientUserLogin} in {user.handle} for a gifted sub!')

    async def __processGiftSubBatches(self, giftSubBatches: list[GiftSub] | None):
        if giftSubBatches is None or len(giftSubBatches) == 0:
            return

        giftSubGroups: dict[str, dict[str, list[TwitchSubscriptionHandler.GiftSub]]] = defaultdict(lambda: defaultdict(lambda: list()))

        for giftSubBatch in giftSubBatches:
            giftSubGroups[giftSubBatch.twitchChannelId][giftSubBatch.subGiftGiverUserId].append(giftSubBatch)

        for giftSubGroup in giftSubGroups.values():
            for giftSubList in giftSubGroup.values():
                firstGiftSub = giftSubList[0]

                donation = TtsSubscriptionDonation(
                    isAnonymous = firstGiftSub.isAnonymous,
                    cumulativeMonths = None,
                    durationMonths = None,
                    numberOfGiftedSubs = len(giftSubList),
                    subGiftGiverDisplayName = firstGiftSub.subGiftGiverUserName,
                    giftType = firstGiftSub.giftType,
                    tier = firstGiftSub.tier
                )

                ttsEvent = TtsEvent(
                    message = None,
                    twitchChannel = firstGiftSub.twitchChannel,
                    twitchChannelId = firstGiftSub.twitchChannelId,
                    userId = firstGiftSub.receiverUserId,
                    userName = firstGiftSub.receiverUserName,
                    donation = donation,
                    provider = firstGiftSub.user.defaultTtsProvider,
                    raidInfo = None
                )

                self.__streamAlertsManager.submitAlert(StreamAlert(
                    soundAlert = SoundAlert.SUBSCRIBE,
                    twitchChannel = firstGiftSub.twitchChannel,
                    twitchChannelId = firstGiftSub.twitchChannelId,
                    ttsEvent = ttsEvent
                ))

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
        if not user.isTtsEnabled:
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

        giftType: TtsSubscriptionDonationGiftType | None = None

        if isGift == True:
            giftType = TtsSubscriptionDonationGiftType.RECEIVER
        elif subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT:
            giftType = TtsSubscriptionDonationGiftType.GIVER

        cumulativeMonths: int | None = None
        durationMonths: int | None = None
        subGiftGiverUserId: str | None = None
        subGiftGiverUserName: str | None = None

        if resub is not None:
            cumulativeMonths = resub.cumulativeMonths
            durationMonths = resub.durationMonths

            if giftType is TtsSubscriptionDonationGiftType.RECEIVER and not isAnonymous and utils.isValidStr(resub.gifterUserId) and utils.isValidStr(resub.gifterUserName) and actualUserId != resub.gifterUserId:
                subGiftGiverUserId = resub.gifterUserId
                subGiftGiverUserName = resub.gifterUserName

        if giftType is not None and utils.isValidStr(subGiftGiverUserId) and utils.isValidStr(subGiftGiverUserName):
            try:
                self.__giftSubQueue.put_nowait(TwitchSubscriptionHandler.GiftSub(
                    isAnonymous = isAnonymous,
                    receiverUserId = actualUserId,
                    receiverUserName = actualUserName,
                    subGiftGiverUserId = subGiftGiverUserId,
                    subGiftGiverUserName = subGiftGiverUserName,
                    twitchChannelId = broadcasterUserId,
                    giftType = giftType,
                    tier = tier,
                    user = user
                ))
            except queue.Full as e:
                self.__timber.log('TwitchSubscriptionHandler', f'Encountered queue.Full when submitting a new gift sub into the giftSub queue (queue size: {self.__giftSubQueue.qsize()}): {e}', e, traceback.format_exc())
        else:
            donation = TtsSubscriptionDonation(
                isAnonymous = isAnonymous,
                cumulativeMonths = cumulativeMonths,
                durationMonths = durationMonths,
                numberOfGiftedSubs = None,
                subGiftGiverDisplayName = subGiftGiverUserName,
                giftType = giftType,
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

    def start(self):
        if self.__isStarted:
            self.__timber.log('TwitchSubscriptionHandler', 'Not starting TwitchSubscriptionHandler as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('TwitchSubscriptionHandler', 'Starting TwitchSubscriptionHandler...')
        self.__backgroundTaskHelper.createTask(self.__startGiftSubBatchingLoop())

    async def __startGiftSubBatchingLoop(self):
        while True:
            giftSubs: list[TwitchSubscriptionHandler.GiftSub] = list()

            try:
                while not self.__giftSubQueue.empty():
                    giftSubs.append(self.__giftSubQueue.get_nowait())
            except queue.Empty as e:
                self.__timber.log('TwitchSubscriptionHandler', f'Encountered queue.Empty when building up giftSubs list (queue size: {self.__giftSubQueue.qsize()}) (giftSubs size: {len(giftSubs)}): {e}', e, traceback.format_exc())

            await self.__processGiftSubBatches(giftSubs)
            await asyncio.sleep(self.__sleepTimeSeconds)
