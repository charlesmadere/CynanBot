import pytest

from src.halfLife.models.halfLifeVoice import HalfLifeVoice
from src.halfLife.parser.halfLifeVoiceParser import HalfLifeVoiceParser
from src.halfLife.parser.halfLifeVoiceParserInterface import HalfLifeVoiceParserInterface


class TesthalfLifeJsonParser:

    parser: HalfLifeVoiceParserInterface = HalfLifeVoiceParser()

    @pytest.mark.asyncio
    async def test_parseVoice_withAll(self):
        result = self.parser.parseVoice('all')
        assert result is HalfLifeVoice.ALL

    @pytest.mark.asyncio
    async def test_parseVoice_withAllVoices(self):
        result = self.parser.parseVoice('all voices')
        assert result is HalfLifeVoice.ALL

        result = self.parser.parseVoice('all-voices')
        assert result is HalfLifeVoice.ALL

        result = self.parser.parseVoice('all_voices')
        assert result is HalfLifeVoice.ALL

        result = self.parser.parseVoice('allvoices')
        assert result is HalfLifeVoice.ALL

        result = self.parser.parseVoice('all voice')
        assert result is HalfLifeVoice.ALL

        result = self.parser.parseVoice('all-voice')
        assert result is HalfLifeVoice.ALL

        result = self.parser.parseVoice('all_voice')
        assert result is HalfLifeVoice.ALL

        result = self.parser.parseVoice('allvoice')
        assert result is HalfLifeVoice.ALL

    @pytest.mark.asyncio
    async def test_parseVoice_withBarney(self):
        result = self.parser.parseVoice('barney')
        assert result is HalfLifeVoice.BARNEY

    @pytest.mark.asyncio
    async def test_parseVoice_withHev(self):
        result = self.parser.parseVoice('hev')
        assert result is HalfLifeVoice.HEV

    @pytest.mark.asyncio
    async def test_parseVoice_withIntercom(self):
        result = self.parser.parseVoice('intercom')
        assert result is HalfLifeVoice.INTERCOM

    @pytest.mark.asyncio
    async def test_parseVoice_withPolice(self):
        result = self.parser.parseVoice('police')
        assert result is HalfLifeVoice.POLICE

    @pytest.mark.asyncio
    async def test_parseVoice_withScience(self):
        result = self.parser.parseVoice('science')
        assert result is HalfLifeVoice.SCIENTIST

    @pytest.mark.asyncio
    async def test_parseVoice_withScientist(self):
        result = self.parser.parseVoice('scientist')
        assert result is HalfLifeVoice.SCIENTIST

    @pytest.mark.asyncio
    async def test_parseVoice_withSoldier(self):
        result = self.parser.parseVoice('soldier')
        assert result is HalfLifeVoice.SOLDIER

    @pytest.mark.asyncio
    async def test_parseVoice_withEmptyString(self):
        result = self.parser.parseVoice('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoice_withNone(self):
        result = self.parser.parseVoice(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoice_withWhitespaceString(self):
        result = self.parser.parseVoice(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_requireVoice_withMale(self):
        result = self.parser.requireVoice('intercom')
        assert result is HalfLifeVoice.INTERCOM

    @pytest.mark.asyncio
    async def test_requireVoice_withPolice(self):
        result = self.parser.requireVoice('police')
        assert result is HalfLifeVoice.POLICE

    @pytest.mark.asyncio
    async def test_requireVoice_withEmptyString(self):
        result: HalfLifeVoice | None = None

        with pytest.raises(ValueError):
            result = self.parser.requireVoice('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireVoice_withNone(self):
        result: HalfLifeVoice | None = None

        with pytest.raises(ValueError):
            result = self.parser.requireVoice(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireVoice_withWhitespaceString(self):
        result: HalfLifeVoice | None = None

        with pytest.raises(ValueError):
            result = self.parser.requireVoice(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_serializeVoice_withAll(self):
        result = self.parser.serializeVoice(HalfLifeVoice.ALL)
        assert result == 'all'

    @pytest.mark.asyncio
    async def test_serializeVoice_withBarney(self):
        result = self.parser.serializeVoice(HalfLifeVoice.BARNEY)
        assert result == 'barney'

    @pytest.mark.asyncio
    async def test_serializeVoice_withHev(self):
        result = self.parser.serializeVoice(HalfLifeVoice.HEV)
        assert result == 'hev'

    @pytest.mark.asyncio
    async def test_serializeVoice_withIntercom(self):
        result = self.parser.serializeVoice(HalfLifeVoice.INTERCOM)
        assert result == 'intercom'

    @pytest.mark.asyncio
    async def test_serializeVoice_withPolice(self):
        result = self.parser.serializeVoice(HalfLifeVoice.POLICE)
        assert result == 'police'

    @pytest.mark.asyncio
    async def test_serializeVoice_withScientist(self):
        result = self.parser.serializeVoice(HalfLifeVoice.SCIENTIST)
        assert result == 'scientist'

    @pytest.mark.asyncio
    async def test_serializeVoice_withSoldier(self):
        result = self.parser.serializeVoice(HalfLifeVoice.SOLDIER)
        assert result == 'soldier'
