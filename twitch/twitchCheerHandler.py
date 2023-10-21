import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from CynanBotCommon.users.userInterface import UserInterface
from twitch.twitchChannelProvider import TwitchChannelProvider


class TwitchCheerHandler():

    def __init__(
        self,
        timber: TimberInterface,
        twitchChannelProvider: TwitchChannelProvider
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise ValueError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')

        self.__timber: TimberInterface = timber
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

        twitchChannel = await self.__twitchChannelProvider.getTwitchChannel(user.getHandle())

        self.__timber.log('TwitchCheerHandler', f'Received a cheer event: (event=\"{event}\") (channel=\"{user.getHandle()}\") (bits={bits}) (message=\"{message}\") (redemptionUserId=\"{redemptionUserId}\") (redemptionUserLogin=\"{redemptionUserLogin}\") (redemptionUserName=\"{redemptionUserName}\")')

        # TODO
        pass
