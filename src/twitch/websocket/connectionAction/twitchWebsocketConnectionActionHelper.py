from typing import Final

from .twitchWebsocketConnectionAction import TwitchWebsocketConnectionAction
from .twitchWebsocketConnectionActionHelperInterface import TwitchWebsocketConnectionActionHelperInterface
from ..endpointHelper.twitchWebsocketEndpointHelperInterface import TwitchWebsocketEndpointHelperInterface
from ..sessionIdHelper.twitchWebsocketSessionIdHelperInterface import TwitchWebsocketSessionIdHelperInterface
from ...api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ...api.models.twitchWebsocketMessageType import TwitchWebsocketMessageType
from ...websocket.twitchWebsocketUser import TwitchWebsocketUser
from ....misc import utils as utils
from ....timber.timberInterface import TimberInterface


class TwitchWebsocketConnectionActionHelper(TwitchWebsocketConnectionActionHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        twitchWebsocketEndpointHelper: TwitchWebsocketEndpointHelperInterface,
        twitchWebsocketSessionIdHelper: TwitchWebsocketSessionIdHelperInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchWebsocketEndpointHelper, TwitchWebsocketEndpointHelperInterface):
            raise TypeError(f'twitchWebsocketEndpointHelper argument is malformed: \"{twitchWebsocketEndpointHelper}\"')
        elif not isinstance(twitchWebsocketSessionIdHelper, TwitchWebsocketSessionIdHelperInterface):
            raise TypeError(f'twitchWebsocketSessionIdHelper argument is malformed: \"{twitchWebsocketSessionIdHelper}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__twitchWebsocketEndpointHelper: Final[TwitchWebsocketEndpointHelperInterface] = twitchWebsocketEndpointHelper
        self.__twitchWebsocketSessionIdHelper: Final[TwitchWebsocketSessionIdHelperInterface] = twitchWebsocketSessionIdHelper

    async def handleConnectionRelatedActions(
        self,
        dataBundle: TwitchWebsocketDataBundle,
        user: TwitchWebsocketUser,
    ) -> TwitchWebsocketConnectionAction:
        if not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')
        elif not isinstance(user, TwitchWebsocketUser):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        await self.__updateConnectionStates(
            dataBundle = dataBundle,
            user = user,
        )

        match dataBundle.metadata.messageType:
            case TwitchWebsocketMessageType.KEEP_ALIVE:
                return TwitchWebsocketConnectionAction.OK

            case TwitchWebsocketMessageType.NOTIFICATION:
                return TwitchWebsocketConnectionAction.OK

            case TwitchWebsocketMessageType.RECONNECT:
                return TwitchWebsocketConnectionAction.RECONNECT

            case TwitchWebsocketMessageType.REVOCATION:
                return TwitchWebsocketConnectionAction.DISCONNECT

            case TwitchWebsocketMessageType.WELCOME:
                return TwitchWebsocketConnectionAction.CREATE_EVENT_SUB_SUBSCRIPTION

            case _:
                raise ValueError(f'Encountered unexpected TwitchWebsocketMessageType ({dataBundle.metadata.messageType=}) ({dataBundle=}) ({user=})')

    async def __updateConnectionStates(
        self,
        dataBundle: TwitchWebsocketDataBundle,
        user: TwitchWebsocketUser,
    ):
        payload = dataBundle.payload
        if payload is None:
            return

        session = payload.session
        if session is None:
            return

        oldTwitchWebsocketUrl = self.__twitchWebsocketEndpointHelper[user]
        newTwitchWebsocketUrl = session.reconnectUrl
        oldTwitchSessionId = self.__twitchWebsocketSessionIdHelper[user]
        newTwitchSessionId = session.sessionId

        anyUpdatedConnectionStates = False

        if utils.isValidUrl(newTwitchWebsocketUrl) and oldTwitchWebsocketUrl != newTwitchWebsocketUrl:
            self.__twitchWebsocketEndpointHelper[user] = newTwitchWebsocketUrl
            anyUpdatedConnectionStates = True

        if utils.isValidStr(newTwitchSessionId) and oldTwitchSessionId != newTwitchSessionId:
            self.__twitchWebsocketSessionIdHelper[user] = newTwitchSessionId
            anyUpdatedConnectionStates = True

        if anyUpdatedConnectionStates:
            self.__timber.log('TwitchWebsocketConnectionActionHelper', f'Twitch connection states have changed ({dataBundle=}) ({user=})')
