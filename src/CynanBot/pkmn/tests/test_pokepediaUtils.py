import pytest

from CynanBot.pkmn.pokepediaUtils import PokepediaUtils
from CynanBot.pkmn.pokepediaUtilsInterface import PokepediaUtilsInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub


class TestPokepediaUtils():

    timber: TimberInterface = TimberStub()

    pokepediaUtils: PokepediaUtilsInterface = PokepediaUtils(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_getMachineNumber_withHmString(self):
        machineNumber = await self.pokepediaUtils.getMachineNumber('HM02')
        assert machineNumber == 2

        machineNumber = await self.pokepediaUtils.getMachineNumber('HM2')
        assert machineNumber == 2

    @pytest.mark.asyncio
    async def test_getMachineNumber_withTmString(self):
        machineNumber = await self.pokepediaUtils.getMachineNumber('TM50')
        assert machineNumber == 50

        machineNumber = await self.pokepediaUtils.getMachineNumber('TM09')
        assert machineNumber == 9

    @pytest.mark.asyncio
    async def test_getMachineNumber_withTrString(self):
        machineNumber = await self.pokepediaUtils.getMachineNumber('TR01')
        assert machineNumber == 1

        machineNumber = await self.pokepediaUtils.getMachineNumber('TR1')
        assert machineNumber == 1
