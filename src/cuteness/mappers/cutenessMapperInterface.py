from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class CutenessMapperInterface(ABC):

    @abstractmethod
    async def parseUtcYearAndMonthString(
        self,
        utcYearAndMonthString: str | Any | None,
    ) -> datetime | None:
        pass

    @abstractmethod
    async def requireUtcYearAndMonthString(
        self,
        utcYearAndMonthString: str | Any | None,
    ) -> datetime:
        pass

    @abstractmethod
    async def serializeToUtcYearAndMonth(
        self,
        dateTime: datetime,
    ) -> str:
        pass
