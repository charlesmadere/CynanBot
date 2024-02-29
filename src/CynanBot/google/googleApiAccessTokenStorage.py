from typing import Optional

from CynanBot.google.googleAccessToken import GoogleAccessToken
from CynanBot.google.googleApiAccessTokenStorageInterface import \
    GoogleApiAccessTokenStorageInterface
from CynanBot.timber.timberInterface import TimberInterface


class GoogleApiAccessTokenStorage(GoogleApiAccessTokenStorageInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

        self.__accessToken: Optional[GoogleAccessToken] = None

    async def getAccessToken(self) -> Optional[GoogleAccessToken]:
        return self.__accessToken

    async def setAccessToken(self, accessToken: Optional[GoogleAccessToken]):
        if accessToken is not None and not isinstance(accessToken, GoogleAccessToken):
            raise TypeError(f'accessToken argument is malformed: \"{accessToken}\"')

        oldAccessToken = self.__accessToken
        self.__accessToken = accessToken
        self.__timber.log('GoogleApiAccessTokenStorage', f'Updated access token (old={oldAccessToken}) (new={accessToken})')
