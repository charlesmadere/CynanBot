from .twitchAnonymousUserIdProviderInterface import TwitchAnonymousUserIdProviderInterface
from ..misc import utils as utils


class TwitchAnonymousUserIdProvider(TwitchAnonymousUserIdProviderInterface):

    def __init__(
        self,
        twitchAnonymousUserId: str = '274598607' # This is hardcoded to the ID of the
                                                 # "AnAnonymousGifter" account on Twitch.
    ):
        if not utils.isValidStr(twitchAnonymousUserId):
            raise TypeError(f'twitchAnonymousUserId argument is malformed: \"{twitchAnonymousUserId}\"')

        self.__twitchAnonymousUserId: str = twitchAnonymousUserId

    async def getTwitchAnonymousUserId(self) -> str:
        return self.__twitchAnonymousUserId
