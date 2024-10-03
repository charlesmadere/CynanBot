import pytest

from src.crowdControl.bizhawk.bizhawkKey import BizhawkKey
from src.crowdControl.bizhawk.bizhawkKeyMapper import BizhawkKeyMapper
from src.crowdControl.bizhawk.bizhawkKeyMapperInterface import BizhawkKeyMapperInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestBizhawkKeyMapper:

    timber: TimberInterface = TimberStub()

    mapper: BizhawkKeyMapperInterface = BizhawkKeyMapper(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_fromString_withEmptyString(self):
        result = await self.mapper.fromString('')
        assert result is None

    @pytest.mark.asyncio
    async def test_fromString_withEsc(self):
        result = await self.mapper.fromString('esc')
        assert result is BizhawkKey.ESC

    @pytest.mark.asyncio
    async def test_fromString_withF1(self):
        result = await self.mapper.fromString('f1')
        assert result is BizhawkKey.F1

    @pytest.mark.asyncio
    async def test_fromString_withF2(self):
        result = await self.mapper.fromString('f2')
        assert result is BizhawkKey.F2

    @pytest.mark.asyncio
    async def test_fromString_withF3(self):
        result = await self.mapper.fromString('f3')
        assert result is BizhawkKey.F3

    @pytest.mark.asyncio
    async def test_fromString_withF4(self):
        result = await self.mapper.fromString('f4')
        assert result is BizhawkKey.F4

    @pytest.mark.asyncio
    async def test_fromString_withF5(self):
        result = await self.mapper.fromString('f5')
        assert result is BizhawkKey.F5

    @pytest.mark.asyncio
    async def test_fromString_withF6(self):
        result = await self.mapper.fromString('f6')
        assert result is BizhawkKey.F6

    @pytest.mark.asyncio
    async def test_fromString_withF7(self):
        result = await self.mapper.fromString('f7')
        assert result is BizhawkKey.F7

    @pytest.mark.asyncio
    async def test_fromString_withF8(self):
        result = await self.mapper.fromString('f8')
        assert result is BizhawkKey.F8

    @pytest.mark.asyncio
    async def test_fromString_withF9(self):
        result = await self.mapper.fromString('f9')
        assert result is BizhawkKey.F9

    @pytest.mark.asyncio
    async def test_fromString_withF10(self):
        result = await self.mapper.fromString('f10')
        assert result is BizhawkKey.F10

    @pytest.mark.asyncio
    async def test_fromString_withF11(self):
        result = await self.mapper.fromString('f11')
        assert result is BizhawkKey.F11

    @pytest.mark.asyncio
    async def test_fromString_withF12(self):
        result = await self.mapper.fromString('f12')
        assert result is BizhawkKey.F12

    @pytest.mark.asyncio
    async def test_fromString_withF13(self):
        result = await self.mapper.fromString('f13')
        assert result is BizhawkKey.F13

    @pytest.mark.asyncio
    async def test_fromString_withF14(self):
        result = await self.mapper.fromString('f14')
        assert result is BizhawkKey.F14

    @pytest.mark.asyncio
    async def test_fromString_withF15(self):
        result = await self.mapper.fromString('f15')
        assert result is BizhawkKey.F15

    @pytest.mark.asyncio
    async def test_fromString_withNone(self):
        result = await self.mapper.fromString(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_fromString_withWhitespaceString(self):
        result = await self.mapper.fromString(' ')
        assert result is None
