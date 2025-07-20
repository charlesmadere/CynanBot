from collections import defaultdict
from typing import Final

from .twitchWebsocketSessionIdHelperInterface import TwitchWebsocketSessionIdHelperInterface
from ..twitchWebsocketUser import TwitchWebsocketUser
from ....timber.timberInterface import TimberInterface


class TwitchWebsocketSessionIdHelper(TwitchWebsocketSessionIdHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        defaultTwitchWebsocketSessionId: str = '',
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(defaultTwitchWebsocketSessionId, str):
            raise TypeError(f'defaultTwitchWebsocketSessionId argument is malformed: \"{defaultTwitchWebsocketSessionId}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__defaultTwitchWebsocketSessionId: Final[str] = defaultTwitchWebsocketSessionId

        self.__twitchSessionIds: Final[dict[TwitchWebsocketUser, str]] = defaultdict(lambda: defaultTwitchWebsocketSessionId)

    def __getitem__(self, key: TwitchWebsocketUser) -> str:
        if not isinstance(key, TwitchWebsocketUser):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        return self.__twitchSessionIds[key]

    def resetToDefault(self, key: TwitchWebsocketUser) -> str:
        if not isinstance(key, TwitchWebsocketUser):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        oldTwitchSessionId = self[key]
        self.__twitchSessionIds[key] = self.__defaultTwitchWebsocketSessionId
        self.__timber.log('TwitchWebsocketSessionidHelper', f'Session ID has been reset to the default ({key=}) ({self.__defaultTwitchWebsocketSessionId=}) ({oldTwitchSessionId=})')

        return self.__defaultTwitchWebsocketSessionId

    def __setitem__(self, key: TwitchWebsocketUser, value: str):
        if not isinstance(key, TwitchWebsocketUser):
            raise TypeError(f'key argument is malformed: \"{key}\"')
        elif not isinstance(value, str):
            raise TypeError(f'value argument is malformed: \"{value}\"')

        oldTwitchSessionId = self[key]
        self.__twitchSessionIds[key] = value
        self.__timber.log('TwitchWebsocketSessionIdHelper', f'Session ID has been changed ({key=}) ({value=}) ({oldTwitchSessionId=})')
