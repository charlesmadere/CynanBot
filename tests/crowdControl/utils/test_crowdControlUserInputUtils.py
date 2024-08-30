import pytest

from src.crowdControl.actions.crowdControlButton import CrowdControlButton
from src.crowdControl.utils.crowdControlUserInputUtils import CrowdControlUserInputUtils
from src.crowdControl.utils.crowdControlUserInputUtilsInterface import CrowdControlUserInputUtilsInterface


class TestCrowdControlUserInputUtils:

    utils: CrowdControlUserInputUtilsInterface = CrowdControlUserInputUtils()

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withA(self):
        result = await self.utils.parseButtonFromUserInput('a')
        assert result is CrowdControlButton.BUTTON_A

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withB(self):
        result = await self.utils.parseButtonFromUserInput('b')
        assert result is CrowdControlButton.BUTTON_B

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withDn(self):
        result = await self.utils.parseButtonFromUserInput('dn')
        assert result is CrowdControlButton.DPAD_DOWN

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withDown(self):
        result = await self.utils.parseButtonFromUserInput('down')
        assert result is CrowdControlButton.DPAD_DOWN

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withDownDpad(self):
        result = await self.utils.parseButtonFromUserInput('down dpad')
        assert result is CrowdControlButton.DPAD_DOWN

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withDownDpadAndExtraWhitespaceJunk(self):
        result = await self.utils.parseButtonFromUserInput('down  dpad')
        assert result is CrowdControlButton.DPAD_DOWN

        result = await self.utils.parseButtonFromUserInput('  down  \n  dpad ')
        assert result is CrowdControlButton.DPAD_DOWN

        result = await self.utils.parseButtonFromUserInput('\n  down  \n \n dpad \n ')
        assert result is CrowdControlButton.DPAD_DOWN

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withDpadDn(self):
        result = await self.utils.parseButtonFromUserInput('dpad_dn')
        assert result is CrowdControlButton.DPAD_DOWN

        result = await self.utils.parseButtonFromUserInput('dpad dn')
        assert result is CrowdControlButton.DPAD_DOWN

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withDpadDown(self):
        result = await self.utils.parseButtonFromUserInput('dpad_down')
        assert result is CrowdControlButton.DPAD_DOWN

        result = await self.utils.parseButtonFromUserInput('dpad down')
        assert result is CrowdControlButton.DPAD_DOWN

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withDpadLeft(self):
        result = await self.utils.parseButtonFromUserInput('dpad_left')
        assert result is CrowdControlButton.DPAD_LEFT

        result = await self.utils.parseButtonFromUserInput('dpad left')
        assert result is CrowdControlButton.DPAD_LEFT

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withDpadRight(self):
        result = await self.utils.parseButtonFromUserInput('dpad_right')
        assert result is CrowdControlButton.DPAD_RIGHT

        result = await self.utils.parseButtonFromUserInput('dpad right')
        assert result is CrowdControlButton.DPAD_RIGHT

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withDpadUp(self):
        result = await self.utils.parseButtonFromUserInput('dpad_up')
        assert result is CrowdControlButton.DPAD_UP

        result = await self.utils.parseButtonFromUserInput('dpad up')
        assert result is CrowdControlButton.DPAD_UP

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withEmptyString(self):
        result = await self.utils.parseButtonFromUserInput('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withLeft(self):
        result = await self.utils.parseButtonFromUserInput('left')
        assert result is CrowdControlButton.DPAD_LEFT

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withLeftDpad(self):
        result = await self.utils.parseButtonFromUserInput('left dpad')
        assert result is CrowdControlButton.DPAD_LEFT

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withLeftTrigger(self):
        result = await self.utils.parseButtonFromUserInput('left_trigger')
        assert result is CrowdControlButton.TRIGGER_LEFT

        result = await self.utils.parseButtonFromUserInput('left trigger')
        assert result is CrowdControlButton.TRIGGER_LEFT

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withNone(self):
        result = await self.utils.parseButtonFromUserInput(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withPause(self):
        result = await self.utils.parseButtonFromUserInput('pause')
        assert result is CrowdControlButton.START

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withRight(self):
        result = await self.utils.parseButtonFromUserInput('right')
        assert result is CrowdControlButton.DPAD_RIGHT

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withRightDpad(self):
        result = await self.utils.parseButtonFromUserInput('right dpad')
        assert result is CrowdControlButton.DPAD_RIGHT

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withRightTrigger(self):
        result = await self.utils.parseButtonFromUserInput('right_trigger')
        assert result is CrowdControlButton.TRIGGER_RIGHT

        result = await self.utils.parseButtonFromUserInput('right trigger')
        assert result is CrowdControlButton.TRIGGER_RIGHT

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withSel(self):
        result = await self.utils.parseButtonFromUserInput('sel')
        assert result is CrowdControlButton.SELECT

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withSelect(self):
        result = await self.utils.parseButtonFromUserInput('select')
        assert result is CrowdControlButton.SELECT

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withStart(self):
        result = await self.utils.parseButtonFromUserInput('start')
        assert result is CrowdControlButton.START

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withTriggerLeft(self):
        result = await self.utils.parseButtonFromUserInput('trigger_left')
        assert result is CrowdControlButton.TRIGGER_LEFT

        result = await self.utils.parseButtonFromUserInput('trigger left')
        assert result is CrowdControlButton.TRIGGER_LEFT

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withTriggerRight(self):
        result = await self.utils.parseButtonFromUserInput('trigger_right')
        assert result is CrowdControlButton.TRIGGER_RIGHT

        result = await self.utils.parseButtonFromUserInput('trigger right')
        assert result is CrowdControlButton.TRIGGER_RIGHT

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withUp(self):
        result = await self.utils.parseButtonFromUserInput('up')
        assert result is CrowdControlButton.DPAD_UP

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withUpDpad(self):
        result = await self.utils.parseButtonFromUserInput('up dpad')
        assert result is CrowdControlButton.DPAD_UP

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withWhitespaceString(self):
        result = await self.utils.parseButtonFromUserInput(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withX(self):
        result = await self.utils.parseButtonFromUserInput('x')
        assert result is CrowdControlButton.BUTTON_X

    @pytest.mark.asyncio
    async def test_parseButtonFromUserInput_withY(self):
        result = await self.utils.parseButtonFromUserInput('y')
        assert result is CrowdControlButton.BUTTON_Y

    def test_sanity(self):
        assert self.utils is not None
        assert isinstance(self.utils, CrowdControlUserInputUtils)
        assert isinstance(self.utils, CrowdControlUserInputUtilsInterface)
