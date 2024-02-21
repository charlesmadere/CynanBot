import math
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.builder.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from CynanBot.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from CynanBot.tts.ttsDonation import TtsDonation
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsProvider import TtsProvider
from CynanBot.tts.ttsSubscriptionDonation import TtsSubscriptionDonation
from CynanBot.tts.ttsSubscriptionDonationGiftType import \
    TtsSubscriptionDonationGiftType
from CynanBot.twitch.absTwitchSubscriptionHandler import \
    AbsTwitchSubscriptionHandler
from CynanBot.twitch.api.twitchCommunitySubGift import TwitchCommunitySubGift
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier
from CynanBot.twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType
from CynanBot.twitch.configuration.twitchChannelProvider import \
    TwitchChannelProvider
from CynanBot.twitch.twitchTokensUtilsInterface import \
    TwitchTokensUtilsInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.userInterface import UserInterface


class TwitchSubscriptionHandler(AbsTwitchSubscriptionHandler):

    def __init__(
        self,
        streamAlertsManager: Optional[StreamAlertsManagerInterface],
        timber: TimberInterface,
        triviaGameBuilder: Optional[TriviaGameBuilderInterface],
        triviaGameMachine: Optional[TriviaGameMachineInterface],
        twitchChannelProvider: TwitchChannelProvider,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        assert streamAlertsManager is None or isinstance(streamAlertsManager, StreamAlertsManagerInterface), f"malformed {streamAlertsManager=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert triviaGameBuilder is None or isinstance(triviaGameBuilder, TriviaGameBuilderInterface), f"malformed {triviaGameBuilder=}"
        assert triviaGameMachine is None or isinstance(triviaGameMachine, TriviaGameMachineInterface), f"malformed {triviaGameMachine=}"
        assert isinstance(twitchChannelProvider, TwitchChannelProvider), f"malformed {twitchChannelProvider=}"
        assert isinstance(twitchTokensUtils, TwitchTokensUtilsInterface), f"malformed {twitchTokensUtils=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"

        self.__streamAlertsManager: Optional[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__triviaGameBuilder: Optional[TriviaGameBuilderInterface] = triviaGameBuilder
        self.__triviaGameMachine: Optional[TriviaGameMachineInterface] = triviaGameMachine
        self.__twitchChannelProvider: TwitchChannelProvider = twitchChannelProvider
        self.__twitchTokensUtils: TwitchTokensUtilsInterface = twitchTokensUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

    async def onNewSubscription(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        assert isinstance(user, UserInterface), f"malformed {user=}"
        assert isinstance(dataBundle, TwitchWebsocketDataBundle), f"malformed {dataBundle=}"

        payload = dataBundle.requirePayload()
        event = payload.getEvent()
        subscription = payload.getSubscription()

        if event is None or subscription is None:
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that has no event: (channel=\"{user.getHandle()}\") ({dataBundle=})')
            return

        subscriptionType = subscription.getSubscriptionType()
        isAnonymous = event.isAnonymous()
        isGift = event.isGift()
        communitySubGift = event.getCommunitySubGift()
        message = event.getMessage()
        eventUserId = event.getUserId()
        eventUserInput = event.getUserInput()
        eventUserLogin = event.getUserLogin()
        eventUserName = event.getUserName()
        tier = event.getTier()

        if tier is None:
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({subscriptionType}) ({isAnonymous=}) ({isGift=}) ({communitySubGift=}) ({message=}) ({eventUserId=}) ({eventUserInput=}) ({eventUserLogin=}) ({eventUserName=}) ({tier=})')
            return

        self.__timber.log('TwitchSubscriptionHandler', f'Received a subscription event: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({subscriptionType}) ({isAnonymous=}) ({isGift=}) ({communitySubGift=}) ({message=}) ({eventUserId=}) ({eventUserInput=}) ({eventUserLogin=}) ({eventUserName=}) ({tier=})')

        if user.isSuperTriviaGameEnabled():
            await self.__processSuperTriviaEvent(
                tier = tier,
                user = user,
                communitySubGift = communitySubGift,
                subscriptionType = subscriptionType
            )

        if user.isTtsEnabled():
            await self.__processTtsEvent(
                isAnonymous = isAnonymous,
                isGift = isGift,
                message = message,
                userId = eventUserId,
                userInput = eventUserInput,
                userLogin = eventUserLogin,
                userName = eventUserName,
                communitySubGift = communitySubGift,
                tier = tier,
                subscriptionType = subscriptionType,
                user = user
            )

    async def __processSuperTriviaEvent(
        self,
        tier: TwitchSubscriberTier,
        user: UserInterface,
        communitySubGift: Optional[TwitchCommunitySubGift],
        subscriptionType: TwitchWebsocketSubscriptionType
    ):
        assert isinstance(tier, TwitchSubscriberTier), f"malformed {tier=}"
        assert isinstance(user, UserInterface), f"malformed {user=}"
        assert communitySubGift is None or isinstance(communitySubGift, TwitchCommunitySubGift), f"malformed {communitySubGift=}"
        assert isinstance(subscriptionType, TwitchWebsocketSubscriptionType), f"malformed {subscriptionType=}"

        if self.__triviaGameBuilder is None or self.__triviaGameMachine is None:
            return
        elif not user.isSuperTriviaGameEnabled():
            return
        elif subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIBE:
            return

        superTriviaSubscribeTriggerAmount = user.getSuperTriviaSubscribeTriggerAmount()
        if not utils.isValidNum(superTriviaSubscribeTriggerAmount) or superTriviaSubscribeTriggerAmount <= 0:
            return

        numberOfSubs = 1
        if communitySubGift is not None:
            numberOfSubs = communitySubGift.getTotal()

        numberOfGames = math.floor(numberOfSubs / superTriviaSubscribeTriggerAmount)
        if numberOfGames < 1:
            return

        action = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.getHandle(),
            numberOfGames = numberOfGames
        )

        if action is not None:
            self.__triviaGameMachine.submitAction(action)

    async def __processTtsEvent(
        self,
        isAnonymous: Optional[bool],
        isGift: Optional[bool],
        message: Optional[str],
        userId: Optional[str],
        userInput: Optional[str],
        userLogin: Optional[str],
        userName: Optional[str],
        communitySubGift: Optional[TwitchCommunitySubGift],
        tier: TwitchSubscriberTier,
        subscriptionType: TwitchWebsocketSubscriptionType,
        user: UserInterface,
    ):
        if isAnonymous is not None and not utils.isValidBool(isAnonymous):
            raise TypeError(f'isAnonymous argument is malformed: \"{isAnonymous}\"')
        if isGift is not None and not utils.isValidBool(isGift):
            raise TypeError(f'isGift argument is malformed: \"{isGift}\"')
        assert message is None or isinstance(message, str), f"malformed {message=}"
        if userId is not None and not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        assert userInput is None or isinstance(userInput, str), f"malformed {userInput=}"
        if userLogin is not None and not utils.isValidStr(userLogin):
            raise TypeError(f'userLogin argument is malformed: \"{userLogin}\"')
        if userName is not None and not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')
        assert communitySubGift is None or isinstance(communitySubGift, TwitchCommunitySubGift), f"malformed {communitySubGift=}"
        assert isinstance(tier, TwitchSubscriberTier), f"malformed {tier=}"
        assert isinstance(subscriptionType, TwitchWebsocketSubscriptionType), f"malformed {subscriptionType=}"
        assert isinstance(user, UserInterface), f"malformed {user=}"

        if self.__streamAlertsManager is None:
            return
        elif not user.isTtsEnabled():
            return
        elif isGift is None:
            if subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIBE or \
                subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT:
                # prevents an annoying situation where some subscription events end up causing
                # two distinct events to come from Twitch, where each are subtly different but
                # both inform of the same new subscriber
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
                twitchAccessToken = await self.__twitchTokensUtils.requireAccessTokenOrFallback(
                    twitchChannel = user.getHandle()
                )

                actualUserId = await self.__userIdsRepository.requireAnonymousUserId(
                    twitchAccessToken = twitchAccessToken
                )

                actualUserName = await self.__userIdsRepository.requireAnonymousUserName(
                    twitchAccessToken = twitchAccessToken
                )
            else:
                self.__timber.log('TwitchSubscriptionHandler', f'Attempted to process subscription event into a TTS message, but data is weird? ({isAnonymous=}) ({isGift=}) ({userId=}) ({userName=})')
                return

        giftType: Optional[TtsSubscriptionDonationGiftType] = None

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
            userId = actualUserId,
            userName = actualUserName,
            donation = donation,
            provider = TtsProvider.DEC_TALK,
            raidInfo = None
        )

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.SUBSCRIBE,
            twitchChannel = user.getHandle(),
            ttsEvent = ttsEvent
        ))
