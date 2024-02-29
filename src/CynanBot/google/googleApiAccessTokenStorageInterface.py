from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.google.googleAccessToken import GoogleAccessToken


class GoogleApiAccessTokenStorageInterface(ABC):

    @abstractmethod
    async def getAccessToken(self) -> Optional[GoogleAccessToken]:
        pass

    @abstractmethod
    async def setAccessToken(self, accessToken: Optional[GoogleAccessToken]):
        pass
