from abc import ABC, abstractmethod
from typing import Any

from ..models.grenadeAttack import GrenadeAttack


class RecentGrenadeAttacksMapperInterface(ABC):

    @abstractmethod
    async def parseGrenadeAttack(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> GrenadeAttack:
        pass

    @abstractmethod
    async def serializeGrenadeAttack(
        self,
        grenadeAttack: GrenadeAttack
    ) -> dict[str, Any]:
        pass
