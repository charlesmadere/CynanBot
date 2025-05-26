import pytest

from src.decTalk.mapper.decTalkVoiceMapper import DecTalkVoiceMapper
from src.decTalk.mapper.decTalkVoiceMapperInterface import DecTalkVoiceMapperInterface
from src.decTalk.models.decTalkVoice import DecTalkVoice


class TestDecTalkVoiceMapper:

    mapper: DecTalkVoiceMapperInterface = DecTalkVoiceMapper()

    @pytest.mark.asyncio
    async def test_parseVoice_withBetty(self):
        result = await self.mapper.parseVoice('betty')
        assert result is DecTalkVoice.BETTY

        result = await self.mapper.parseVoice('nb')
        assert result is DecTalkVoice.BETTY

        result = await self.mapper.parseVoice('[:nb]')
        assert result is DecTalkVoice.BETTY

    @pytest.mark.asyncio
    async def test_parseVoice_withDennis(self):
        result = await self.mapper.parseVoice('dennis')
        assert result is DecTalkVoice.DENNIS

        result = await self.mapper.parseVoice('nd')
        assert result is DecTalkVoice.DENNIS

        result = await self.mapper.parseVoice('[:nd]')
        assert result is DecTalkVoice.DENNIS

    @pytest.mark.asyncio
    async def test_parseVoice_withEmptyString(self):
        result = await self.mapper.parseVoice('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoice_withFrank(self):
        result = await self.mapper.parseVoice('frank')
        assert result is DecTalkVoice.FRANK

        result = await self.mapper.parseVoice('nf')
        assert result is DecTalkVoice.FRANK

        result = await self.mapper.parseVoice('[:nf]')
        assert result is DecTalkVoice.FRANK

    @pytest.mark.asyncio
    async def test_parseVoice_withHarry(self):
        result = await self.mapper.parseVoice('harry')
        assert result is DecTalkVoice.HARRY

        result = await self.mapper.parseVoice('nh')
        assert result is DecTalkVoice.HARRY

        result = await self.mapper.parseVoice('[:nh]')
        assert result is DecTalkVoice.HARRY

    @pytest.mark.asyncio
    async def test_parseVoice_withKit(self):
        result = await self.mapper.parseVoice('kit')
        assert result is DecTalkVoice.KIT

        result = await self.mapper.parseVoice('nk')
        assert result is DecTalkVoice.KIT

        result = await self.mapper.parseVoice('[:nk]')
        assert result is DecTalkVoice.KIT

    @pytest.mark.asyncio
    async def test_parseVoice_withNone(self):
        result = await self.mapper.parseVoice(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoice_withPaul(self):
        result = await self.mapper.parseVoice('paul')
        assert result is DecTalkVoice.PAUL

        result = await self.mapper.parseVoice('np')
        assert result is DecTalkVoice.PAUL

        result = await self.mapper.parseVoice('[:np]')
        assert result is DecTalkVoice.PAUL

    @pytest.mark.asyncio
    async def test_parseVoice_withRita(self):
        result = await self.mapper.parseVoice('rita')
        assert result is DecTalkVoice.RITA

        result = await self.mapper.parseVoice('nr')
        assert result is DecTalkVoice.RITA

        result = await self.mapper.parseVoice('[:nr]')
        assert result is DecTalkVoice.RITA

    @pytest.mark.asyncio
    async def test_parseVoice_withUrsula(self):
        result = await self.mapper.parseVoice('ursula')
        assert result is DecTalkVoice.URSULA

        result = await self.mapper.parseVoice('nu')
        assert result is DecTalkVoice.URSULA

        result = await self.mapper.parseVoice('[:nu]')
        assert result is DecTalkVoice.URSULA

    @pytest.mark.asyncio
    async def test_parseVoice_withWendy(self):
        result = await self.mapper.parseVoice('wendy')
        assert result is DecTalkVoice.WENDY

        result = await self.mapper.parseVoice('whispering wendy')
        assert result is DecTalkVoice.WENDY

        result = await self.mapper.parseVoice('nw')
        assert result is DecTalkVoice.WENDY

        result = await self.mapper.parseVoice('[:nw]')
        assert result is DecTalkVoice.WENDY

    @pytest.mark.asyncio
    async def test_parseVoice_withWhitespaceString(self):
        result = await self.mapper.parseVoice(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_requireVoice_withBetty(self):
        result = await self.mapper.requireVoice('betty')
        assert result is DecTalkVoice.BETTY

        result = await self.mapper.requireVoice('nb')
        assert result is DecTalkVoice.BETTY

        result = await self.mapper.requireVoice('[:nb]')
        assert result is DecTalkVoice.BETTY

    @pytest.mark.asyncio
    async def test_requireVoice_withDennis(self):
        result = await self.mapper.requireVoice('dennis')
        assert result is DecTalkVoice.DENNIS

        result = await self.mapper.requireVoice('nd')
        assert result is DecTalkVoice.DENNIS

        result = await self.mapper.requireVoice('[:nd]')
        assert result is DecTalkVoice.DENNIS

    @pytest.mark.asyncio
    async def test_requireVoice_withEmptyString(self):
        result: DecTalkVoice | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireVoice('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireVoice_withFrank(self):
        result = await self.mapper.requireVoice('frank')
        assert result is DecTalkVoice.FRANK

        result = await self.mapper.requireVoice('nf')
        assert result is DecTalkVoice.FRANK

        result = await self.mapper.requireVoice('[:nf]')
        assert result is DecTalkVoice.FRANK

    @pytest.mark.asyncio
    async def test_requireVoice_withHarry(self):
        result = await self.mapper.requireVoice('harry')
        assert result is DecTalkVoice.HARRY

        result = await self.mapper.requireVoice('nh')
        assert result is DecTalkVoice.HARRY

        result = await self.mapper.requireVoice('[:nh]')
        assert result is DecTalkVoice.HARRY

    @pytest.mark.asyncio
    async def test_requireVoice_withKit(self):
        result = await self.mapper.requireVoice('kit')
        assert result is DecTalkVoice.KIT

        result = await self.mapper.requireVoice('nk')
        assert result is DecTalkVoice.KIT

        result = await self.mapper.requireVoice('[:nk]')
        assert result is DecTalkVoice.KIT

    @pytest.mark.asyncio
    async def test_requireVoice_withNone(self):
        result: DecTalkVoice | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireVoice(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireVoice_withPaul(self):
        result = await self.mapper.requireVoice('paul')
        assert result is DecTalkVoice.PAUL

        result = await self.mapper.requireVoice('perfect paul')
        assert result is DecTalkVoice.PAUL

        result = await self.mapper.requireVoice('np')
        assert result is DecTalkVoice.PAUL

        result = await self.mapper.requireVoice('[:np]')
        assert result is DecTalkVoice.PAUL

    @pytest.mark.asyncio
    async def test_requireVoice_withRita(self):
        result = await self.mapper.requireVoice('rita')
        assert result is DecTalkVoice.RITA

        result = await self.mapper.requireVoice('nr')
        assert result is DecTalkVoice.RITA

        result = await self.mapper.requireVoice('[:nr]')
        assert result is DecTalkVoice.RITA

    @pytest.mark.asyncio
    async def test_requireVoice_withUrsula(self):
        result = await self.mapper.requireVoice('ursula')
        assert result is DecTalkVoice.URSULA

        result = await self.mapper.requireVoice('nu')
        assert result is DecTalkVoice.URSULA

        result = await self.mapper.requireVoice('[:nu]')
        assert result is DecTalkVoice.URSULA

    @pytest.mark.asyncio
    async def test_requireVoice_withWendy(self):
        result = await self.mapper.requireVoice('wendy')
        assert result is DecTalkVoice.WENDY

        result = await self.mapper.requireVoice('nw')
        assert result is DecTalkVoice.WENDY

        result = await self.mapper.requireVoice('[:nw]')
        assert result is DecTalkVoice.WENDY

    @pytest.mark.asyncio
    async def test_requireVoice_withWhitespaceString(self):
        result: DecTalkVoice | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireVoice(' ')

        assert result is None

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, DecTalkVoiceMapper)
        assert isinstance(self.mapper, DecTalkVoiceMapperInterface)

    @pytest.mark.asyncio
    async def test_serializeVoice_withBetty(self):
        result = await self.mapper.serializeVoice(DecTalkVoice.BETTY)
        assert result == 'betty'

    @pytest.mark.asyncio
    async def test_serializeVoice_withDennis(self):
        result = await self.mapper.serializeVoice(DecTalkVoice.DENNIS)
        assert result == 'dennis'

    @pytest.mark.asyncio
    async def test_serializeVoice_withFrank(self):
        result = await self.mapper.serializeVoice(DecTalkVoice.FRANK)
        assert result == 'frank'

    @pytest.mark.asyncio
    async def test_serializeVoice_withHarry(self):
        result = await self.mapper.serializeVoice(DecTalkVoice.HARRY)
        assert result == 'harry'

    @pytest.mark.asyncio
    async def test_serializeVoice_withKit(self):
        result = await self.mapper.serializeVoice(DecTalkVoice.KIT)
        assert result == 'kit'

    @pytest.mark.asyncio
    async def test_serializeVoice_withPaul(self):
        result = await self.mapper.serializeVoice(DecTalkVoice.PAUL)
        assert result == 'paul'

    @pytest.mark.asyncio
    async def test_serializeVoice_withRita(self):
        result = await self.mapper.serializeVoice(DecTalkVoice.RITA)
        assert result == 'rita'

    @pytest.mark.asyncio
    async def test_serializeVoice_withUrsula(self):
        result = await self.mapper.serializeVoice(DecTalkVoice.URSULA)
        assert result == 'ursula'

    @pytest.mark.asyncio
    async def test_serializeVoice_withWendy(self):
        result = await self.mapper.serializeVoice(DecTalkVoice.WENDY)
        assert result == 'wendy'
