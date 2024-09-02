from abc import ABC, abstractmethod

from .chatterBeanStats import ChatterBeanStats


class BeanStatsPresenterInterface(ABC):

    @abstractmethod
    async def toString(self, beanStats: ChatterBeanStats) -> str:
        pass
