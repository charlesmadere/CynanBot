from typing import Any, Dict, Optional

from CynanBot.twitch.api.websocket.twitchWebsocketEvent import \
    TwitchWebsocketEvent
from CynanBot.twitch.api.websocket.twitchWebsocketSession import \
    TwitchWebsocketSession
from CynanBot.twitch.api.websocket.twitchWebsocketSubscription import \
    TwitchWebsocketSubscription


class TwitchWebsocketPayload():

    def __init__(
        self,
        event: Optional[TwitchWebsocketEvent] = None,
        session: Optional[TwitchWebsocketSession] = None,
        subscription: Optional[TwitchWebsocketSubscription] = None
    ):
        assert event is None or isinstance(event, TwitchWebsocketEvent), f"malformed {event=}"
        assert session is None or isinstance(session, TwitchWebsocketSession), f"malformed {session=}"
        assert subscription is None or isinstance(subscription, TwitchWebsocketSubscription), f"malformed {subscription=}"

        self.__event: Optional[TwitchWebsocketEvent] = event
        self.__session: Optional[TwitchWebsocketSession] = session
        self.__subscription: Optional[TwitchWebsocketSubscription] = subscription

    def getEvent(self) -> Optional[TwitchWebsocketEvent]:
        return self.__event

    def getSession(self) -> Optional[TwitchWebsocketSession]:
        return self.__session

    def getSubscription(self) -> Optional[TwitchWebsocketSubscription]:
        return self.__subscription

    def isEmpty(self) -> bool:
        return self.__event is None and self.__session is None and self.__subscription is None

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def requireSubscription(self) -> TwitchWebsocketSubscription:
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
