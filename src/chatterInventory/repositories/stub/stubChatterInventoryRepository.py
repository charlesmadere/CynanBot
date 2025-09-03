from frozendict import frozendict

from ..chatterInventoryRepositoryInterface import ChatterInventoryRepositoryInterface
from ...models.chatterInventoryData import ChatterInventoryData
from ...models.chatterItemType import ChatterItemType


class StubChatterInventoryRepository(ChatterInventoryRepositoryInterface):

    async def __createStubInventory(self) -> frozendict[ChatterItemType, int]:
        inventory: dict[ChatterItemType, int] = dict()

        for itemType in ChatterItemType:
            inventory[itemType] = 0

        return frozendict(inventory)

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterInventoryData:
        inventory = await self.__createStubInventory()

        return ChatterInventoryData(
            inventory = inventory,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

    async def update(
        self,
        itemType: ChatterItemType,
        changeAmount: int,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterInventoryData:
        return await self.get(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )
