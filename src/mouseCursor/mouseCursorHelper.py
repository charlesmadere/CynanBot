from datetime import timedelta
from typing import Any, Final

from .mouseCursorHelperInterface import MouseCursorHelperInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..users.userInterface import UserInterface
from ..websocketConnection.websocketConnectionServerInterface import WebsocketConnectionServerInterface
from ..websocketConnection.websocketEventType import WebsocketEventType


class MouseCursorHelper(MouseCursorHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        websocketConnectionServer: WebsocketConnectionServerInterface,
        visibilityDuration: timedelta = timedelta(seconds = 20),
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(websocketConnectionServer, WebsocketConnectionServerInterface):
            raise TypeError(f'websocketConnectionServer argument is malformed: \"{websocketConnectionServer}\"')
        elif not isinstance(visibilityDuration, timedelta):
            raise TypeError(f'visibilityDuration argument is malformed: \"{visibilityDuration}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__websocketConnectionServer: Final[WebsocketConnectionServerInterface] = websocketConnectionServer
        self.__visibilityDuration: Final[timedelta] = visibilityDuration

    async def applyMouseCursor(
        self,
        twitchChannelId: str,
        twitchUser: UserInterface,
    ) -> bool:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(twitchUser, UserInterface):
            raise TypeError(f'twitchUser argument is malformed: \"{twitchUser}\"')

        if not twitchUser.isMouseCursorEnabled:
            return False

        eventData: dict[str, Any] = {
            'visibilityDurationSeconds': self.__visibilityDuration.total_seconds(),
        }

        self.__websocketConnectionServer.submitEvent(
            twitchChannel = twitchUser.handle,
            twitchChannelId = twitchChannelId,
            eventType = WebsocketEventType.MOUSE_CURSOR,
            eventData = eventData,
        )

        return True
