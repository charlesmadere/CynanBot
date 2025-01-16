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
    async def test_fromString_withA(self):
        result = await self.mapper.fromString('a')
        assert result is BizhawkKey.A

    @pytest.mark.asyncio
    async def test_fromString_withArrowDown(self):
        result = await self.mapper.fromString('arrow_down')
        assert result is BizhawkKey.ARROW_DOWN

    @pytest.mark.asyncio
    async def test_fromString_withArrowLeft(self):
        result = await self.mapper.fromString('arrow_left')
        assert result is BizhawkKey.ARROW_LEFT

    @pytest.mark.asyncio
    async def test_fromString_withArrowRight(self):
        result = await self.mapper.fromString('arrow_right')
        assert result is BizhawkKey.ARROW_RIGHT

    @pytest.mark.asyncio
    async def test_fromString_withArrowUp(self):
        result = await self.mapper.fromString('arrow_up')
        assert result is BizhawkKey.ARROW_UP

    @pytest.mark.asyncio
    async def test_fromString_withB(self):
        result = await self.mapper.fromString('b')
        assert result is BizhawkKey.B

    @pytest.mark.asyncio
    async def test_fromString_withC(self):
        result = await self.mapper.fromString('c')
        assert result is BizhawkKey.C

    @pytest.mark.asyncio
    async def test_fromString_withD(self):
        result = await self.mapper.fromString('d')
        assert result is BizhawkKey.D

    @pytest.mark.asyncio
    async def test_fromString_withE(self):
        result = await self.mapper.fromString('e')
        assert result is BizhawkKey.E

    @pytest.mark.asyncio
    async def test_fromString_withEmptyString(self):
        result = await self.mapper.fromString('')
        assert result is None

    @pytest.mark.asyncio
    async def test_fromString_withEnter(self):
        result = await self.mapper.fromString('enter')
        assert result is BizhawkKey.ENTER

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
    async def test_fromString_withS(self):
        result = await self.mapper.fromString('s')
        assert result is BizhawkKey.S

    @pytest.mark.asyncio
    async def test_fromString_withSpace(self):
        result = await self.mapper.fromString('space')
        assert result is BizhawkKey.SPACE

    @pytest.mark.asyncio
    async def test_fromString_withW(self):
        result = await self.mapper.fromString('w')
        assert result is BizhawkKey.W

    @pytest.mark.asyncio
    async def test_fromString_withWhitespaceString(self):
        result = await self.mapper.fromString(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_fromString_withX(self):
        result = await self.mapper.fromString('x')
        assert result is BizhawkKey.X

    @pytest.mark.asyncio
    async def test_fromString_withY(self):
        result = await self.mapper.fromString('y')
        assert result is BizhawkKey.Y

    @pytest.mark.asyncio
    async def test_fromString_withZ(self):
        result = await self.mapper.fromString('z')
        assert result is BizhawkKey.Z

    @pytest.mark.asyncio
    async def test_toString_withA(self):
        result = await self.mapper.toString(BizhawkKey.A)
        assert result == 'a'

    @pytest.mark.asyncio
    async def test_toString_withArrowDown(self):
        result = await self.mapper.toString(BizhawkKey.ARROW_DOWN)
        assert result == 'arrow_down'

    @pytest.mark.asyncio
    async def test_toString_withArrowLeft(self):
        result = await self.mapper.toString(BizhawkKey.ARROW_LEFT)
        assert result == 'arrow_left'

    @pytest.mark.asyncio
    async def test_toString_withArrowRight(self):
        result = await self.mapper.toString(BizhawkKey.ARROW_RIGHT)
        assert result == 'arrow_right'

    @pytest.mark.asyncio
    async def test_toString_withArrowUp(self):
        result = await self.mapper.toString(BizhawkKey.ARROW_UP)
        assert result == 'arrow_up'

    @pytest.mark.asyncio
    async def test_toString_withB(self):
        result = await self.mapper.toString(BizhawkKey.B)
        assert result == 'b'

    @pytest.mark.asyncio
    async def test_toString_withC(self):
        result = await self.mapper.toString(BizhawkKey.C)
        assert result == 'c'

    @pytest.mark.asyncio
    async def test_toString_withD(self):
        result = await self.mapper.toString(BizhawkKey.D)
        assert result == 'd'

    @pytest.mark.asyncio
    async def test_toString_withE(self):
        result = await self.mapper.toString(BizhawkKey.E)
        assert result == 'e'

    @pytest.mark.asyncio
    async def test_toString_withEnter(self):
        result = await self.mapper.toString(BizhawkKey.ENTER)
        assert result == 'enter'

    @pytest.mark.asyncio
    async def test_toString_withEsc(self):
        result = await self.mapper.toString(BizhawkKey.ESC)
        assert result == 'esc'

    @pytest.mark.asyncio
    async def test_toString_withF1(self):
        result = await self.mapper.toString(BizhawkKey.F1)
        assert result == 'f1'

    @pytest.mark.asyncio
    async def test_toString_withF2(self):
        result = await self.mapper.toString(BizhawkKey.F2)
        assert result == 'f2'

    @pytest.mark.asyncio
    async def test_toString_withF3(self):
        result = await self.mapper.toString(BizhawkKey.F3)
        assert result == 'f3'

    @pytest.mark.asyncio
    async def test_toString_withF4(self):
        result = await self.mapper.toString(BizhawkKey.F4)
        assert result == 'f4'

    @pytest.mark.asyncio
    async def test_toString_withF5(self):
        result = await self.mapper.toString(BizhawkKey.F5)
        assert result == 'f5'

    @pytest.mark.asyncio
    async def test_toString_withF6(self):
        result = await self.mapper.toString(BizhawkKey.F6)
        assert result == 'f6'

    @pytest.mark.asyncio
    async def test_toString_withF7(self):
        result = await self.mapper.toString(BizhawkKey.F7)
        assert result == 'f7'

    @pytest.mark.asyncio
    async def test_toString_withF8(self):
        result = await self.mapper.toString(BizhawkKey.F8)
        assert result == 'f8'

    @pytest.mark.asyncio
    async def test_toString_withF9(self):
        result = await self.mapper.toString(BizhawkKey.F9)
        assert result == 'f9'

    @pytest.mark.asyncio
    async def test_toString_withF10(self):
        result = await self.mapper.toString(BizhawkKey.F10)
        assert result == 'f10'

    @pytest.mark.asyncio
    async def test_toString_withF11(self):
        result = await self.mapper.toString(BizhawkKey.F11)
        assert result == 'f11'

    @pytest.mark.asyncio
    async def test_toString_withF12(self):
        result = await self.mapper.toString(BizhawkKey.F12)
        assert result == 'f12'

    @pytest.mark.asyncio
    async def test_toString_withF13(self):
        result = await self.mapper.toString(BizhawkKey.F13)
        assert result == 'f13'

    @pytest.mark.asyncio
    async def test_toString_withF14(self):
        result = await self.mapper.toString(BizhawkKey.F14)
        assert result == 'f14'

    @pytest.mark.asyncio
    async def test_toString_withF15(self):
        result = await self.mapper.toString(BizhawkKey.F15)
        assert result == 'f15'

    @pytest.mark.asyncio
    async def test_toString_withS(self):
        result = await self.mapper.toString(BizhawkKey.S)
        assert result == 's'

    @pytest.mark.asyncio
    async def test_toString_withSpace(self):
        result = await self.mapper.toString(BizhawkKey.SPACE)
        assert result == 'space'

    @pytest.mark.asyncio
    async def test_toString_withW(self):
        result = await self.mapper.toString(BizhawkKey.W)
        assert result == 'w'

    @pytest.mark.asyncio
    async def test_toString_withX(self):
        result = await self.mapper.toString(BizhawkKey.X)
        assert result == 'x'

    @pytest.mark.asyncio
    async def test_toString_withY(self):
        result = await self.mapper.toString(BizhawkKey.Y)
        assert result == 'y'

    @pytest.mark.asyncio
    async def test_toString_withZ(self):
        result = await self.mapper.toString(BizhawkKey.Z)
        assert result == 'z'
