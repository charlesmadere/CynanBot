import pytest

from src.microsoft.models.microsoftTtsVoice import MicrosoftTtsVoice
from src.microsoft.parser.microsoftTtsJsonParser import MicrosoftTtsJsonParser
from src.microsoft.parser.microsoftTtsJsonParserInterface import MicrosoftTtsJsonParserInterface


class TestMicrosoftTtsJsonParser:

    parser: MicrosoftTtsJsonParserInterface = MicrosoftTtsJsonParser()

    @pytest.mark.asyncio
    async def test_parseVoice_withAna(self):
        result = await self.parser.parseVoice('ana')
        assert result is MicrosoftTtsVoice.ANA

    @pytest.mark.asyncio
    async def test_parseVoice_withAndrew(self):
        result = await self.parser.parseVoice('andrew')
        assert result is MicrosoftTtsVoice.ANDREW

    @pytest.mark.asyncio
    async def test_parseVoice_withAria(self):
        result = await self.parser.parseVoice('aria')
        assert result is MicrosoftTtsVoice.ARIA

    @pytest.mark.asyncio
    async def test_parseVoice_withAva(self):
        result = await self.parser.parseVoice('ava')
        assert result is MicrosoftTtsVoice.AVA

    @pytest.mark.asyncio
    async def test_parseVoice_withBrian(self):
        result = await self.parser.parseVoice('brian')
        assert result is MicrosoftTtsVoice.BRIAN

    @pytest.mark.asyncio
    async def test_parseVoice_withChristopher(self):
        result = await self.parser.parseVoice('christopher')
        assert result is MicrosoftTtsVoice.CHRISTOPHER

    @pytest.mark.asyncio
    async def test_parseVoice_withClara(self):
        result = await self.parser.parseVoice('clara')
        assert result is MicrosoftTtsVoice.CLARA

    @pytest.mark.asyncio
    async def test_parseVoice_withDavid(self):
        result = await self.parser.parseVoice('david')
        assert result is MicrosoftTtsVoice.DAVID

    @pytest.mark.asyncio
    async def test_parseVoice_withEmma(self):
        result = await self.parser.parseVoice('emma')
        assert result is MicrosoftTtsVoice.EMMA

    @pytest.mark.asyncio
    async def test_parseVoice_withEric(self):
        result = await self.parser.parseVoice('eric')
        assert result is MicrosoftTtsVoice.ERIC

    @pytest.mark.asyncio
    async def test_parseVoice_withGuy(self):
        result = await self.parser.parseVoice('guy')
        assert result is MicrosoftTtsVoice.GUY

    @pytest.mark.asyncio
    async def test_parseVoice_withHaruka(self):
        result = await self.parser.parseVoice('haruka')
        assert result is MicrosoftTtsVoice.HARUKA

    @pytest.mark.asyncio
    async def test_parseVoice_withHortense(self):
        result = await self.parser.parseVoice('hortense')
        assert result is MicrosoftTtsVoice.HORTENSE

    @pytest.mark.asyncio
    async def test_parseVoice_withJenny(self):
        result = await self.parser.parseVoice('jenny')
        assert result is MicrosoftTtsVoice.JENNY

    @pytest.mark.asyncio
    async def test_parseVoice_withKeita(self):
        result = await self.parser.parseVoice('keita')
        assert result is MicrosoftTtsVoice.KEITA

    @pytest.mark.asyncio
    async def test_parseVoice_withLiam(self):
        result = await self.parser.parseVoice('liam')
        assert result is MicrosoftTtsVoice.LIAM

    @pytest.mark.asyncio
    async def test_parseVoice_withMichelle(self):
        result = await self.parser.parseVoice('michelle')
        assert result is MicrosoftTtsVoice.MICHELLE

    @pytest.mark.asyncio
    async def test_parseVoice_withNanami(self):
        result = await self.parser.parseVoice('nanami')
        assert result is MicrosoftTtsVoice.NANAMI

    @pytest.mark.asyncio
    async def test_parseVoice_withRoger(self):
        result = await self.parser.parseVoice('roger')
        assert result is MicrosoftTtsVoice.ROGER

    @pytest.mark.asyncio
    async def test_parseVoice_withSteffan(self):
        result = await self.parser.parseVoice('steffan')
        assert result is MicrosoftTtsVoice.STEFFAN

    @pytest.mark.asyncio
    async def test_parseVoice_withZira(self):
        result = await self.parser.parseVoice('zira')
        assert result is MicrosoftTtsVoice.ZIRA

    @pytest.mark.asyncio
    async def test_parseVoice_withNone(self):
        result = await self.parser.parseVoice(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoice_withEmptyString(self):
        result = await self.parser.parseVoice(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoice_withWhitespaceString(self):
        result = await self.parser.parseVoice(' ')
        assert result is None

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, MicrosoftTtsJsonParser)
        assert isinstance(self.parser, MicrosoftTtsJsonParserInterface)

    @pytest.mark.asyncio
    async def test_serializeVoice_withAna(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.ANA)
        assert result == 'ana'

    @pytest.mark.asyncio
    async def test_serializeVoice_withAndrew(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.ANDREW)
        assert result == 'andrew'

    @pytest.mark.asyncio
    async def test_serializeVoice_withAria(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.ARIA)
        assert result == 'aria'

    @pytest.mark.asyncio
    async def test_serializeVoice_withAva(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.AVA)
        assert result == 'ava'

    @pytest.mark.asyncio
    async def test_serializeVoice_withBrian(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.BRIAN)
        assert result == 'brian'

    @pytest.mark.asyncio
    async def test_serializeVoice_withChristopher(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.CHRISTOPHER)
        assert result == 'christopher'

    @pytest.mark.asyncio
    async def test_serializeVoice_withClara(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.CLARA)
        assert result == 'clara'

    @pytest.mark.asyncio
    async def test_serializeVoice_withDavid(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.DAVID)
        assert result == 'david'

    @pytest.mark.asyncio
    async def test_serializeVoice_withEmma(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.EMMA)
        assert result == 'emma'

    @pytest.mark.asyncio
    async def test_serializeVoice_withEric(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.ERIC)
        assert result == 'eric'

    @pytest.mark.asyncio
    async def test_serializeVoice_withGuy(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.GUY)
        assert result == 'guy'

    @pytest.mark.asyncio
    async def test_serializeVoice_withHaruka(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.HARUKA)
        assert result == 'haruka'

    @pytest.mark.asyncio
    async def test_serializeVoice_withHortense(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.HORTENSE)
        assert result == 'hortense'

    @pytest.mark.asyncio
    async def test_serializeVoice_withJenny(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.JENNY)
        assert result == 'jenny'

    @pytest.mark.asyncio
    async def test_serializeVoice_withKeita(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.KEITA)
        assert result == 'keita'

    @pytest.mark.asyncio
    async def test_serializeVoice_withLiam(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.LIAM)
        assert result == 'liam'

    @pytest.mark.asyncio
    async def test_serializeVoice_withMichelle(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.MICHELLE)
        assert result == 'michelle'

    @pytest.mark.asyncio
    async def test_serializeVoice_withNanami(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.NANAMI)
        assert result == 'nanami'

    @pytest.mark.asyncio
    async def test_serializeVoice_withRoger(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.ROGER)
        assert result == 'roger'

    @pytest.mark.asyncio
    async def test_serializeVoice_withSteffan(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.STEFFAN)
        assert result == 'steffan'

    @pytest.mark.asyncio
    async def test_serializeVoice_withZira(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.ZIRA)
        assert result == 'zira'
