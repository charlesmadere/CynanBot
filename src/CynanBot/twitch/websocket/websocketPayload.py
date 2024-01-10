from typing import Any, Dict, Optional

from CynanBot.twitch.websocket.websocketEvent import WebsocketEvent
from CynanBot.twitch.websocket.websocketSession import WebsocketSession
from CynanBot.twitch.websocket.websocketSubscription import \
    WebsocketSubscription


class WebsocketPayload():

    def __init__(
        self,
        event: Optional[WebsocketEvent] = None,
        session: Optional[WebsocketSession] = None,
        subscription: Optional[WebsocketSubscription] = None
    ):
        if event is not None and not isinstance(event, WebsocketEvent):
            raise ValueError(f'event argument is malformed: \"{event}\"')
        elif session is not None and not isinstance(session, WebsocketSession):
            raise ValueError(f'session argument is malformed: \"{session}\"')
        elif subscription is not None and not isinstance(subscription, WebsocketSubscription):
            raise ValueError(f'subscription argument is malformed: \"{subscription}\"')

        self.__event: Optional[WebsocketEvent] = event
        self.__session: Optional[WebsocketSession] = session
        self.__subscription: Optional[WebsocketSubscription] = subscription

    def getEvent(self) -> Optional[WebsocketEvent]:
        return self.__event

    def getSession(self) -> Optional[WebsocketSession]:
        return self.__session

    def getSubscription(self) -> Optional[WebsocketSubscription]:
        return self.__subscription

    def isEmpty(self) -> bool:
        return self.__event is None and self.__session is None and self.__subscription is None

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def requireSubscription(self) -> WebsocketSubscription:
        subscription = self.__subscription

        if subscription is None:
            raise RuntimeError(f'this WebsocketPayload has no subscription ({self})')

        return subscription

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'event': self.__event,
            'session': self.__session,
            'subscription': self.__subscription
        }
