from abc import ABC, abstractmethod


class Clearable(ABC):

    @abstractmethod
    async def clearCaches(self):
        pass
