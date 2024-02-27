from abc import ABC, abstractmethod
from typing import Optional


class GoogleCloudProjectCredentialsProviderInterface(ABC):

    @abstractmethod
    async def getGoogleCloudApiKey(self) -> Optional[str]:
        pass

    @abstractmethod
    async def getGoogleCloudProjectId(self) -> Optional[str]:
        pass
