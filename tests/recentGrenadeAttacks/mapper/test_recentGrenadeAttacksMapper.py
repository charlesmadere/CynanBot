from datetime import datetime

import pytest

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.recentGrenadeAttacks.mapper.recentGrenadeAttacksMapper import RecentGrenadeAttacksMapper
from src.recentGrenadeAttacks.mapper.recentGrenadeAttacksMapperInterface import RecentGrenadeAttacksMapperInterface
from src.recentGrenadeAttacks.models.grenadeAttack import GrenadeAttack


class TestRecentGrenadeAttacksMapper:

    mapper: RecentGrenadeAttacksMapperInterface = RecentGrenadeAttacksMapper()

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    @pytest.mark.asyncio
    async def test_parseGrenadeAttack(self):
        dateTime = datetime.now(self.timeZoneRepository.getDefault())
        attackedUserId = 'abc123'

        result = await self.mapper.parseGrenadeAttack({
            'dateTime': dateTime.isoformat(),
            'userId': attackedUserId,
        })

        assert isinstance(result, GrenadeAttack)
        assert result.attackedDateTime == dateTime
        assert result.attackedUserId == attackedUserId

    @pytest.mark.asyncio
    async def test_parseGrenadeAttack_withEmptyDictionary(self):
        result: GrenadeAttack | None = None

        with pytest.raises(TypeError):
            result = await self.mapper.parseGrenadeAttack(dict())

        assert result is None

    @pytest.mark.asyncio
    async def test_parseGrenadeAttack_withNone(self):
        result: GrenadeAttack | None = None

        with pytest.raises(TypeError):
            result = await self.mapper.parseGrenadeAttack(None)

        assert result is None

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, RecentGrenadeAttacksMapper)
        assert isinstance(self.mapper, RecentGrenadeAttacksMapperInterface)

    @pytest.mark.asyncio
    async def test_serializeGrenadeAttack(self):
        attackedDateTime = datetime.now(self.timeZoneRepository.getDefault())
        attackedUserId = 'xyz456'

        result = await self.mapper.serializeGrenadeAttack(GrenadeAttack(
            attackedDateTime = attackedDateTime,
            attackedUserId = attackedUserId
        ))

        assert isinstance(result, dict)
        assert len(result) == 2
        assert result['dateTime'] == attackedDateTime.isoformat()
        assert result['userId'] == attackedUserId
