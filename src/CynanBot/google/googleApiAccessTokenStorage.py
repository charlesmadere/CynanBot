from datetime import datetime, timedelta, timezone, tzinfo

from CynanBot.google.googleAccessToken import GoogleAccessToken
from CynanBot.google.googleApiAccessTokenStorageInterface import \
    GoogleApiAccessTokenStorageInterface
from CynanBot.timber.timberInterface import TimberInterface


class GoogleApiAccessTokenStorage(GoogleApiAccessTokenStorageInterface):

    def __init__(
        self,
        timber: TimberInterface,
        expireTimeBuffer: timedelta = timedelta(minutes = 3),
        timeZone: tzinfo = timezone.utc
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(expireTimeBuffer, timedelta):
            raise TypeError(f'expireTimeBuffer argument is malformed: \"{expireTimeBuffer}\"')
        elif not isinstance(timeZone, timezone):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__timber: TimberInterface = timber
        self.__expireTimeBuffer: timedelta = expireTimeBuffer
        self.__timeZone: tzinfo = timeZone

        self.__accessToken: GoogleAccessToken | None = None

    async def getAccessToken(self) -> GoogleAccessToken | None:
        accessToken = self.__accessToken

        if accessToken is None:
            return None

        now = datetime.now(self.__timeZone)
        expireTime = accessToken.expireTime

        if (now + self.__expireTimeBuffer) < expireTime:
            return accessToken

        self.__timber.log('GoogleApiAccessTokenStorage', f'Erasing persisted access token, as it is now too old to use')
        self.__accessToken = None
        return None

    async def setAccessToken(self, accessToken: GoogleAccessToken | None):
        if accessToken is not None and not isinstance(accessToken, GoogleAccessToken):
            raise TypeError(f'accessToken argument is malformed: \"{accessToken}\"')

        oldAccessToken = self.__accessToken
        self.__accessToken = accessToken
        self.__timber.log('GoogleApiAccessTokenStorage', f'Updating access token (old={oldAccessToken}) (new={accessToken})')
