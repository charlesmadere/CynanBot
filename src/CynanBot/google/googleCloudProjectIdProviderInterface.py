from abc import ABC, abstractmethod


class GoogleCloudProjectCredentialsProviderInterface(ABC):

    @abstractmethod
    async def getGoogleCloudApiKey(self) -> str | None:
        pass

    @abstractmethod
    async def getGoogleCloudProjectId(self) -> str | None:
        pass
