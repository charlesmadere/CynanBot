from abc import ABC, abstractmethod

from CynanBot.google.googleAccessToken import GoogleAccessToken


class GoogleApiAccessTokenStorageInterface(ABC):

    @abstractmethod
    async def getAccessToken(self) -> GoogleAccessToken | None:
        pass

    @abstractmethod
    async def setAccessToken(self, accessToken: GoogleAccessToken | None):
        pass
