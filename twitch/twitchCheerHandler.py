from typing import Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.tts.ttsCheerDonation import TtsCheerDonation
from CynanBotCommon.tts.ttsDonation import TtsDonation
from CynanBotCommon.tts.ttsEvent import TtsEvent
from CynanBotCommon.tts.ttsManagerInterface import TtsManagerInterface
from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.users.userInterface import UserInterface
from twitch.absTwitchCheerHandler import AbsTwitchCheerHandler
from twitch.twitchChannelProvider import TwitchChannelProvider


class TwitchCheerHandler(AbsTwitchCheerHandler):

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

    async def onNewCheer(
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
            self.__timber.log('TwitchCheerHandler', f'Received a data bundle that has no event: \"{dataBundle}\"')
            return

        bits = event.getBits()
        message = event.getMessage()
        redemptionUserId = event.getUserId()
        redemptionUserLogin = event.getUserLogin()
        redemptionUserName = event.getUserName()

        if not utils.isValidInt(bits) or bits < 1 or not utils.isValidStr(redemptionUserId) or not utils.isValidStr(redemptionUserLogin) or not utils.isValidStr(redemptionUserName):
            self.__timber.log('TwitchCheerHandler', f'Received a data bundle that is missing crucial data: (bits={bits}) (userId=\"{redemptionUserId}\") (userLogin=\"{redemptionUserLogin}\") (userName=\"{redemptionUserName}\")')
            return

        self.__timber.log('TwitchCheerHandler', f'Received a cheer event: (event=\"{event}\") (channel=\"{user.getHandle()}\") (bits={bits}) (message=\"{message}\") (redemptionUserId=\"{redemptionUserId}\") (redemptionUserLogin=\"{redemptionUserLogin}\") (redemptionUserName=\"{redemptionUserName}\")')

        if user.isTtsEnabled():
            await self.__processTtsEvent(
                bits = bits,
                message = message,
                redemptionUserId = redemptionUserId,
                redemptionUserLogin = redemptionUserLogin,
                redemptionUserName = redemptionUserName,
                user = user
            )

    async def __processTtsEvent(
        self,
        bits: int,
        message: Optional[str],
        redemptionUserId: str,
        redemptionUserLogin: str,
        redemptionUserName: str,
        user: UserInterface
    ):
        if not utils.isValidInt(bits):
            raise ValueError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif message is not None and not isinstance(message, str):
            raise ValueError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(redemptionUserId):
            raise ValueError(f'redemptionUserId argument is malformed: \"{redemptionUserId}\"')
        elif not utils.isValidStr(redemptionUserLogin):
            raise ValueError(f'redemptionUserLogin argument is malformed: \"{redemptionUserLogin}\"')
        elif not utils.isValidStr(redemptionUserName):
            raise ValueError(f'redemptionUserName argument is malformed: \"{redemptionUserName}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        donation: TtsDonation = TtsCheerDonation(bits = bits)

        self.__ttsManager.submitTtsEvent(TtsEvent(
            message = message,
            twitchChannel = user.getHandle(),
            userId = redemptionUserId,
            userName = redemptionUserName,
            donation = donation
        ))
