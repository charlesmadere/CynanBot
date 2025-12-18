from collections import defaultdict
from typing import Final

from .twitchWebsocketEndpointHelperInterface import TwitchWebsocketEndpointHelperInterface
from ..twitchWebsocketUser import TwitchWebsocketUser
from ....misc import utils as utils
from ....timber.timberInterface import TimberInterface


class TwitchWebsocketEndpointHelper(TwitchWebsocketEndpointHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        defaultTwitchWebsocketEndpointUrl: str = 'wss://eventsub.wss.twitch.tv/ws',
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidUrl(defaultTwitchWebsocketEndpointUrl):
            raise TypeError(f'defaultTwitchWebsocketEndpointUrl argument is malformed: \"{defaultTwitchWebsocketEndpointUrl}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__defaultTwitchWebsocketEndpointUrl: Final[str] = defaultTwitchWebsocketEndpointUrl

        self.__twitchEndpointUrls: Final[dict[TwitchWebsocketUser, str]] = defaultdict(lambda: defaultTwitchWebsocketEndpointUrl)

    def __getitem__(self, key: TwitchWebsocketUser) -> str:
        if not isinstance(key, TwitchWebsocketUser):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        return self.__twitchEndpointUrls[key]

    def resetToDefault(self, key: TwitchWebsocketUser) -> str:
        if not isinstance(key, TwitchWebsocketUser):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        oldTwitchEndpointUrl = self[key]
        self.__twitchEndpointUrls[key] = self.__defaultTwitchWebsocketEndpointUrl
        self.__timber.log('TwitchWebsocketEndpointHelper', f'Endpoint has been reset to the default ({key=}) ({self.__defaultTwitchWebsocketEndpointUrl=}) ({oldTwitchEndpointUrl=})')

        return self.__defaultTwitchWebsocketEndpointUrl

    def __setitem__(self, key: TwitchWebsocketUser, value: str):
        if not isinstance(key, TwitchWebsocketUser):
            raise TypeError(f'key argument is malformed: \"{key}\"')
        elif not utils.isValidUrl(value):
            raise TypeError(f'value argument is malformed: \"{value}\"')

        oldTwitchEndpointUrl = self[key]
        self.__twitchEndpointUrls[key] = value
        self.__timber.log('TwitchWebsocketEndpointHelper', f'Endpoint has been changed ({key=}) ({value=}) ({oldTwitchEndpointUrl=})')
