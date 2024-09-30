import pytest

from src.decTalk.decTalkVoice import DecTalkVoice
from src.decTalk.decTalkVoiceMapper import DecTalkVoiceMapper
from src.decTalk.decTalkVoiceMapperInterface import DecTalkVoiceMapperInterface


class TestDecTalkVoiceMapper:

    decTalkVoiceMapper: DecTalkVoiceMapperInterface = DecTalkVoiceMapper()

    @pytest.mark.asyncio
    async def test_toString_withBetty(self):
        result = await self.decTalkVoiceMapper.toString(DecTalkVoice.BETTY)
        assert result == '[:nb]'

    @pytest.mark.asyncio
    async def test_toString_withDennis(self):
        result = await self.decTalkVoiceMapper.toString(DecTalkVoice.DENNIS)
        assert result == '[:nd]'

    @pytest.mark.asyncio
    async def test_toString_withFrank(self):
        result = await self.decTalkVoiceMapper.toString(DecTalkVoice.FRANK)
        assert result == '[:nf]'

    @pytest.mark.asyncio
    async def test_toString_withHarry(self):
        result = await self.decTalkVoiceMapper.toString(DecTalkVoice.HARRY)
        assert result == '[:nh]'

    @pytest.mark.asyncio
    async def test_toString_withKit(self):
        result = await self.decTalkVoiceMapper.toString(DecTalkVoice.KIT)
        assert result == '[:nk]'

    @pytest.mark.asyncio
    async def test_toString_withPaul(self):
        result = await self.decTalkVoiceMapper.toString(DecTalkVoice.PAUL)
        assert result == '[:np]'

    @pytest.mark.asyncio
    async def test_toString_withRita(self):
        result = await self.decTalkVoiceMapper.toString(DecTalkVoice.RITA)
        assert result == '[:nr]'

    @pytest.mark.asyncio
    async def test_toString_withUrsula(self):
        result = await self.decTalkVoiceMapper.toString(DecTalkVoice.URSULA)
        assert result == '[:nu]'

    @pytest.mark.asyncio
    async def test_toString_withWendy(self):
        result = await self.decTalkVoiceMapper.toString(DecTalkVoice.WENDY)
        assert result == '[:nw]'
