import pytest

from src.pkmn.pokepediaBerryFlavor import PokepediaBerryFlavor
from src.pkmn.pokepediaJsonMapper import PokepediaJsonMapper
from src.pkmn.pokepediaJsonMapperInterface import PokepediaJsonMapperInterface
from src.pkmn.pokepediaMachineType import PokepediaMachineType
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestPokepediaJsonMapper():

    timber: TimberInterface = TimberStub()

    jsonMapper: PokepediaJsonMapperInterface = PokepediaJsonMapper(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_parseBerryFlavor_withNegative1(self):
        result = await self.jsonMapper.parseBerryFlavor(-1)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseBerryFlavor_withNone(self):
        result = await self.jsonMapper.parseBerryFlavor(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseBerryFlavor_with0(self):
        result = await self.jsonMapper.parseBerryFlavor(0)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseBerryFlavor_with1(self):
        result = await self.jsonMapper.parseBerryFlavor(1)
        assert result is PokepediaBerryFlavor.SPICY

    @pytest.mark.asyncio
    async def test_parseBerryFlavor_with2(self):
        result = await self.jsonMapper.parseBerryFlavor(2)
        assert result is PokepediaBerryFlavor.DRY

    @pytest.mark.asyncio
    async def test_parseBerryFlavor_with3(self):
        result = await self.jsonMapper.parseBerryFlavor(3)
        assert result is PokepediaBerryFlavor.SWEET

    @pytest.mark.asyncio
    async def test_parseBerryFlavor_with4(self):
        result = await self.jsonMapper.parseBerryFlavor(4)
        assert result is PokepediaBerryFlavor.BITTER

    @pytest.mark.asyncio
    async def test_parseBerryFlavor_with5(self):
        result = await self.jsonMapper.parseBerryFlavor(5)
        assert result is PokepediaBerryFlavor.SOUR

    @pytest.mark.asyncio
    async def test_parseMachineNumber_withEmptyString(self):
        result = await self.jsonMapper.parseMachineNumber('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseMachineNumber_withHm01String(self):
        result = await self.jsonMapper.parseMachineNumber('HM01')
        assert result == 1

    @pytest.mark.asyncio
    async def test_parseMachineNumber_withNone(self):
        result = await self.jsonMapper.parseMachineNumber(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseMachineNumber_withTm21String(self):
        result = await self.jsonMapper.parseMachineNumber('tm21')
        assert result == 21

    @pytest.mark.asyncio
    async def test_parseMachineNumber_withTr98765String(self):
        result = await self.jsonMapper.parseMachineNumber('TR98765')
        assert result == 98765

    @pytest.mark.asyncio
    async def test_parseMachineNumber_withWhitespaceString(self):
        result = await self.jsonMapper.parseMachineNumber(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseMachineNumber_with21String(self):
        result = await self.jsonMapper.parseMachineNumber('21')
        assert result == 21

    @pytest.mark.asyncio
    async def test_parseMachineType_withEmptyString(self):
        result = await self.jsonMapper.parseMachineType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseMachineType_withHmString(self):
        result = await self.jsonMapper.parseMachineType('hm')
        assert result is PokepediaMachineType.HM

        result = await self.jsonMapper.parseMachineType('HM')
        assert result is PokepediaMachineType.HM

    @pytest.mark.asyncio
    async def test_parseMachineType_withHm0String(self):
        result = await self.jsonMapper.parseMachineType('hm0')
        assert result is PokepediaMachineType.HM

        result = await self.jsonMapper.parseMachineType('HM0')
        assert result is PokepediaMachineType.HM

    @pytest.mark.asyncio
    async def test_parseMachineType_withHm05String(self):
        result = await self.jsonMapper.parseMachineType('hm05')
        assert result is PokepediaMachineType.HM

        result = await self.jsonMapper.parseMachineType('HM05')
        assert result is PokepediaMachineType.HM

    @pytest.mark.asyncio
    async def test_parseMachineType_withHm9999String(self):
        result = await self.jsonMapper.parseMachineType('hm9999')
        assert result is PokepediaMachineType.HM

        result = await self.jsonMapper.parseMachineType('HM9999')
        assert result is PokepediaMachineType.HM

    @pytest.mark.asyncio
    async def test_parseMachineType_withTmString(self):
        result = await self.jsonMapper.parseMachineType('tm')
        assert result is PokepediaMachineType.TM

        result = await self.jsonMapper.parseMachineType('TM')
        assert result is PokepediaMachineType.TM

    @pytest.mark.asyncio
    async def test_parseMachineType_withTm0String(self):
        result = await self.jsonMapper.parseMachineType('tm0')
        assert result is PokepediaMachineType.TM

        result = await self.jsonMapper.parseMachineType('TM0')
        assert result is PokepediaMachineType.TM

    @pytest.mark.asyncio
    async def test_parseMachineType_withTm24String(self):
        result = await self.jsonMapper.parseMachineType('tm24')
        assert result is PokepediaMachineType.TM

        result = await self.jsonMapper.parseMachineType('TM24')
        assert result is PokepediaMachineType.TM

    @pytest.mark.asyncio
    async def test_parseMachineType_withTm9999String(self):
        result = await self.jsonMapper.parseMachineType('tm9999')
        assert result is PokepediaMachineType.TM

        result = await self.jsonMapper.parseMachineType('TM9999')
        assert result is PokepediaMachineType.TM

    @pytest.mark.asyncio
    async def test_parseMachineType_withTrString(self):
        result = await self.jsonMapper.parseMachineType('tr')
        assert result is PokepediaMachineType.TR

        result = await self.jsonMapper.parseMachineType('TR')
        assert result is PokepediaMachineType.TR

    @pytest.mark.asyncio
    async def test_parseMachineType_withTr0String(self):
        result = await self.jsonMapper.parseMachineType('tr0')
        assert result is PokepediaMachineType.TR

        result = await self.jsonMapper.parseMachineType('TR0')
        assert result is PokepediaMachineType.TR

    @pytest.mark.asyncio
    async def test_parseMachineType_withTr01String(self):
        result = await self.jsonMapper.parseMachineType('tr01')
        assert result is PokepediaMachineType.TR

        result = await self.jsonMapper.parseMachineType('TR01')
        assert result is PokepediaMachineType.TR

    @pytest.mark.asyncio
    async def test_parseMachineType_withTr9999String(self):
        result = await self.jsonMapper.parseMachineType('tr9999')
        assert result is PokepediaMachineType.TR

        result = await self.jsonMapper.parseMachineType('TR9999')
        assert result is PokepediaMachineType.TR

    @pytest.mark.asyncio
    async def test_parseMachineType_withNone(self):
        result = await self.jsonMapper.parseMachineType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_requireBerryFlavor_withNegative1(self):
        result: PokepediaBerryFlavor | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireBerryFlavor(-1)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireBerryFlavor_withNone(self):
        result: PokepediaBerryFlavor | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireBerryFlavor(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireBerryFlavor_with0(self):
        result: PokepediaBerryFlavor | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireBerryFlavor(0)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireBerryFlavor_with1(self):
        result = await self.jsonMapper.requireBerryFlavor(1)
        assert result is PokepediaBerryFlavor.SPICY

    @pytest.mark.asyncio
    async def test_requireBerryFlavor_with2(self):
        result = await self.jsonMapper.requireBerryFlavor(2)
        assert result is PokepediaBerryFlavor.DRY

    @pytest.mark.asyncio
    async def test_requireBerryFlavor_with3(self):
        result = await self.jsonMapper.requireBerryFlavor(3)
        assert result is PokepediaBerryFlavor.SWEET

    @pytest.mark.asyncio
    async def test_requireBerryFlavor_with4(self):
        result = await self.jsonMapper.requireBerryFlavor(4)
        assert result is PokepediaBerryFlavor.BITTER

    @pytest.mark.asyncio
    async def test_requireBerryFlavor_with5(self):
        result = await self.jsonMapper.requireBerryFlavor(5)
        assert result is PokepediaBerryFlavor.SOUR

    @pytest.mark.asyncio
    async def test_requireMachineType_withEmptyString(self):
        result: PokepediaMachineType | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireMachineType('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireMachineType_withHmString(self):
        result = await self.jsonMapper.requireMachineType('hm')
        assert result is PokepediaMachineType.HM

        result = await self.jsonMapper.requireMachineType('HM')
        assert result is PokepediaMachineType.HM

    @pytest.mark.asyncio
    async def test_requireMachineType_withTmString(self):
        result = await self.jsonMapper.requireMachineType('tm')
        assert result is PokepediaMachineType.TM

        result = await self.jsonMapper.requireMachineType('TM')
        assert result is PokepediaMachineType.TM

    @pytest.mark.asyncio
    async def test_requireMachineType_withTrString(self):
        result = await self.jsonMapper.requireMachineType('tr')
        assert result is PokepediaMachineType.TR

        result = await self.jsonMapper.requireMachineType('TR')
        assert result is PokepediaMachineType.TR

    @pytest.mark.asyncio
    async def test_requireMachineType_withTr500String(self):
        result = await self.jsonMapper.requireMachineType('tr500')
        assert result is PokepediaMachineType.TR

    @pytest.mark.asyncio
    async def test_requireMachineType_withNone(self):
        result: PokepediaMachineType | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireMachineType(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireMachineType_withWhitespaceString(self):
        result: PokepediaMachineType | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireMachineType(' ')

        assert result is None
