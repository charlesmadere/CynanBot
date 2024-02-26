from abc import ABC, abstractmethod


class GoogleCloudProjectCredentialsProviderInterface(ABC):

    @abstractmethod
    async def getGoogleCloudApiKey(self) -> str:
        pass

    @abstractmethod
    async def getGoogleCloudProjectId(self) -> str:
        pass
