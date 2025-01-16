import pytest

from src.cheerActions.cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from src.cheerActions.timeout.timeoutCheerActionMapper import TimeoutCheerActionMapper
from src.timeout.timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement


class TestTimeoutCheerActionMapper:

    mapper: TimeoutCheerActionMapper = TimeoutCheerActionMapper()

    @pytest.mark.asyncio
    async def test_toTimeoutActionDataStreamStatusRequirement_withAny(self):
        result = await self.mapper.toTimeoutActionDataStreamStatusRequirement(CheerActionStreamStatusRequirement.ANY)
        assert result is TimeoutStreamStatusRequirement.ANY

    @pytest.mark.asyncio
    async def test_toTimeoutActionDataStreamStatusRequirement_withOffline(self):
        result = await self.mapper.toTimeoutActionDataStreamStatusRequirement(CheerActionStreamStatusRequirement.OFFLINE)
        assert result is TimeoutStreamStatusRequirement.OFFLINE

    @pytest.mark.asyncio
    async def test_toTimeoutActionDataStreamStatusRequirement_withOnline(self):
        result = await self.mapper.toTimeoutActionDataStreamStatusRequirement(CheerActionStreamStatusRequirement.ONLINE)
        assert result is TimeoutStreamStatusRequirement.ONLINE
