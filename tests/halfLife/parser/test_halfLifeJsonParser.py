import pytest

from src.halfLife.models.halfLifeVoice import HalfLifeVoice
from src.halfLife.parser.halfLifeJsonParser import HalfLifeJsonParser
from src.halfLife.parser.halfLifeJsonParserInterface import HalfLifeJsonParserInterface


class TesthalfLifeJsonParser:

    parser: HalfLifeJsonParserInterface = HalfLifeJsonParser()

    @pytest.mark.asyncio
    async def test_parseVoice_withAll(self):
        result = self.parser.parseVoice('all')
        assert result is HalfLifeVoice.ALL

    @pytest.mark.asyncio
    async def test_parseVoice_withBarney(self):
        result = self.parser.parseVoice('barney')
        assert result is HalfLifeVoice.BARNEY

    @pytest.mark.asyncio
    async def test_parseVoice_withFemale(self):
        result = self.parser.parseVoice('female')
        assert result is HalfLifeVoice.FEMALE

    async def test_parseVoice_withMale(self):
        result = self.parser.parseVoice('male')
        assert result is HalfLifeVoice.MALE

    @pytest.mark.asyncio
    async def test_parseVoice_withPolice(self):
        result = self.parser.parseVoice('police')
        assert result is HalfLifeVoice.POLICE

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
        result = self.parser.requireVoice('male')
        assert result is HalfLifeVoice.MALE

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
    async def test_serializeVoice_withFemale(self):
        result = self.parser.serializeVoice(HalfLifeVoice.FEMALE)
        assert result == 'female'

    @pytest.mark.asyncio
    async def test_serializeVoice_withMale(self):
        result = self.parser.serializeVoice(HalfLifeVoice.MALE)
        assert result == 'male'

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
