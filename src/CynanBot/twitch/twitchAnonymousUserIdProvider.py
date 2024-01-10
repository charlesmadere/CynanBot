import CynanBot.misc.utils as utils
from CynanBot.twitch.twitchAnonymousUserIdProviderInterface import \
    TwitchAnonymousUserIdProviderInterface


class TwitchAnonymousUserIdProvider(TwitchAnonymousUserIdProviderInterface):

    def __init__(
        self,
        twitchAnonymousUserId: str = '274598607' # This is hardcoded to the ID of the
                                                 # "AnAnonymousGifter" account on Twitch.
    ):
        if not utils.isValidStr(twitchAnonymousUserId):
            raise ValueError(f'twitchAnonymousUserId argument is malformed: \"{twitchAnonymousUserId}\"')

        self.__twitchAnonymousUserId: str = twitchAnonymousUserId

    async def getTwitchAnonymousUserId(self) -> str:
        return self.__twitchAnonymousUserId
