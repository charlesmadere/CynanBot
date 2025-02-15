import pytest

from src.decTalk.decTalkVoiceMapper import DecTalkVoiceMapper
from src.decTalk.decTalkVoiceMapperInterface import DecTalkVoiceMapperInterface
from src.decTalk.models.decTalkVoice import DecTalkVoice


class TestDecTalkVoiceMapper:

    decTalkVoiceMapper: DecTalkVoiceMapperInterface = DecTalkVoiceMapper()

    @pytest.mark.asyncio
    async def test_fromString_withBetty(self):
        result = await self.decTalkVoiceMapper.fromString('betty')
        assert result is DecTalkVoice.BETTY

    @pytest.mark.asyncio
    async def test_fromString_withDennis(self):
        result = await self.decTalkVoiceMapper.fromString('dennis')
        assert result is DecTalkVoice.DENNIS

    @pytest.mark.asyncio
    async def test_fromString_withFrank(self):
        result = await self.decTalkVoiceMapper.fromString('frank')
        assert result is DecTalkVoice.FRANK

    @pytest.mark.asyncio
    async def test_fromString_withHarry(self):
        result = await self.decTalkVoiceMapper.fromString('harry')
        assert result is DecTalkVoice.HARRY

    @pytest.mark.asyncio
    async def test_fromString_withKit(self):
        result = await self.decTalkVoiceMapper.fromString('kit')
        assert result is DecTalkVoice.KIT

    @pytest.mark.asyncio
    async def test_fromString_withPaul(self):
        result = await self.decTalkVoiceMapper.fromString('paul')
        assert result is DecTalkVoice.PAUL

    @pytest.mark.asyncio
    async def test_fromString_withRita(self):
        result = await self.decTalkVoiceMapper.fromString('rita')
        assert result is DecTalkVoice.RITA

    @pytest.mark.asyncio
    async def test_fromString_withUrsula(self):
        result = await self.decTalkVoiceMapper.fromString('ursula')
        assert result is DecTalkVoice.URSULA

    @pytest.mark.asyncio
    async def test_fromString_withWendy(self):
        result = await self.decTalkVoiceMapper.fromString('wendy')
        assert result is DecTalkVoice.WENDY

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
