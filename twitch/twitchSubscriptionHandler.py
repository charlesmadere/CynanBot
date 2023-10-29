from typing import Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.tts.ttsDonation import TtsDonation
from CynanBotCommon.tts.ttsEvent import TtsEvent
from CynanBotCommon.tts.ttsManagerInterface import TtsManagerInterface
from CynanBotCommon.tts.ttsSubscriptionDonation import TtsSubscriptionDonation
from CynanBotCommon.twitch.twitchSubscriberTier import TwitchSubscriberTier
from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.users.userInterface import UserInterface
from twitch.absTwitchSubscriptionHandler import AbsTwitchSubscriptionHandler
from twitch.twitchChannelProvider import TwitchChannelProvider


class TwitchSubscriptionHandler(AbsTwitchSubscriptionHandler):

    def __init__(
        self,
        timber: TimberInterface,
        ttsManager: TtsManagerInterface,
        twitchChannelProvider: TwitchChannelProvider
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsManager, TtsManagerInterface):
            raise ValueError(f'ttsManager argument is malformed: \"{ttsManager}\"')
        elif not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise ValueError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')

        self.__timber: TimberInterface = timber
        self.__ttsManager: TtsManagerInterface = ttsManager
        self.__twitchChannelProvider: TwitchChannelProvider = twitchChannelProvider

    async def onNewSubscription(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: WebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, WebsocketDataBundle):
            raise ValueError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.getPayload().getEvent()

        if event is None:
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that has no event: \"{dataBundle}\"')
            return

        isAnonymous = event.isAnonymous()
        isGift = event.isGift()
        message = event.getMessage()
        redemptionUserId = event.getUserId()
        redemptionUserLogin = event.getUserLogin()
        redemptionUserName = event.getUserName()
        userInput = event.getUserInput()
        tier = event.getTier()

        if not utils.isValidStr(redemptionUserId) or not utils.isValidStr(redemptionUserLogin) or not utils.isValidStr(redemptionUserName) or tier is None:
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that is missing crucial data: (isAnonymous={isAnonymous}) (isGift={isGift}) (userId=\"{redemptionUserId}\") (userLogin=\"{redemptionUserLogin}\") (userName=\"{redemptionUserName}\") (tier={tier})')
            return

        self.__timber.log('TwitchCheerHandler', f'Received a subscription event: (event=\"{event}\") (channel=\"{user.getHandle()}\") (isAnonymous={isAnonymous}) (isGift={isGift}) (message=\"{message}\") (redemptionUserId=\"{redemptionUserId}\") (redemptionUserLogin=\"{redemptionUserLogin}\") (redemptionUserName=\"{redemptionUserName}\") (userInput=\"{userInput}\") (tier=\"{tier}\")')

        if user.isTtsEnabled():
            await self.__processTtsEvent(
                isAnonymous = isAnonymous,
                isGift = isGift,
                message = message,
                redemptionUserId = redemptionUserId,
                redemptionUserLogin = redemptionUserLogin,
                redemptionUserName = redemptionUserName,
                userInput = userInput,
                tier = tier,
                user = user
            )

    async def __processTtsEvent(
        self,
        isAnonymous: Optional[bool],
        isGift: Optional[bool],
        message: Optional[str],
        redemptionUserId: str,
        redemptionUserLogin: str,
        redemptionUserName: str,
        userInput: Optional[str],
        tier: TwitchSubscriberTier,
        user: UserInterface
    ):
        if isAnonymous is not None and not utils.isValidBool(isAnonymous):
            raise ValueError(f'isAnonymous argument is malformed: \"{isAnonymous}\"')
        elif isGift is not None and not utils.isValidBool(isGift):
            raise ValueError(f'isGift argument is malformed: \"{isGift}\"')
        elif message is not None and not isinstance(message, str):
            raise ValueError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(redemptionUserId):
            raise ValueError(f'redemptionUserId argument is malformed: \"{redemptionUserId}\"')
        elif not utils.isValidStr(redemptionUserLogin):
            raise ValueError(f'redemptionUserLogin argument is malformed: \"{redemptionUserLogin}\"')
        elif not utils.isValidStr(redemptionUserName):
            raise ValueError(f'redemptionUserName argument is malformed: \"{redemptionUserName}\"')
        elif userInput is not None and not isinstance(userInput, str):
            raise ValueError(f'userInput argument is malformed: \"{userInput}\"')
        elif not isinstance(tier, TwitchSubscriberTier):
            raise ValueError(f'tier argument is malformed: \"{tier}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        actualMessage = message
        if not utils.isValidStr(actualMessage):
            actualMessage = userInput

        if isAnonymous is None:
            isAnonymous = False

        if isGift is None:
            isGift = False

        donation: TtsDonation = TtsSubscriptionDonation(
            isAnonymous = isAnonymous,
            isGift = isGift,
            tier = tier
        )

        self.__ttsManager.submitTtsEvent(TtsEvent(
            message = actualMessage,
            twitchChannel = user.getHandle(),
            userId = redemptionUserId,
            userName = redemptionUserName,
            donation = donation
        ))
