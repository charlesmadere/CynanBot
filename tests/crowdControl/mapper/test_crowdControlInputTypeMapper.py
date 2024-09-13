import pytest

from src.crowdControl.actions.crowdControlButton import CrowdControlButton
from src.crowdControl.mapper.crowdControlInputTypeMapper import CrowdControlInputTypeMapper
from src.crowdControl.mapper.crowdControlInputTypeMapperInterface import CrowdControlInputTypeMapperInterface
from src.users.crowdControl.crowdControlInputType import CrowdControlInputType


class TestCrowdControlInputTypeMapper:

    mapper: CrowdControlInputTypeMapperInterface = CrowdControlInputTypeMapper()

    @pytest.mark.asyncio
    async def test_toButton_withButtonA(self):
        result = await self.mapper.toButton(CrowdControlInputType.BUTTON_A)
        assert result is CrowdControlButton.BUTTON_A

    @pytest.mark.asyncio
    async def test_toButton_withButtonB(self):
        result = await self.mapper.toButton(CrowdControlInputType.BUTTON_B)
        assert result is CrowdControlButton.BUTTON_B

    @pytest.mark.asyncio
    async def test_toButton_withButtonC(self):
        result = await self.mapper.toButton(CrowdControlInputType.BUTTON_C)
        assert result is CrowdControlButton.BUTTON_C

    @pytest.mark.asyncio
    async def test_toButton_withButtonX(self):
        result = await self.mapper.toButton(CrowdControlInputType.BUTTON_X)
        assert result is CrowdControlButton.BUTTON_X

    @pytest.mark.asyncio
    async def test_toButton_withButtonY(self):
        result = await self.mapper.toButton(CrowdControlInputType.BUTTON_Y)
        assert result is CrowdControlButton.BUTTON_Y

    @pytest.mark.asyncio
    async def test_toButton_withButtonZ(self):
        result = await self.mapper.toButton(CrowdControlInputType.BUTTON_Z)
        assert result is CrowdControlButton.BUTTON_Z

    @pytest.mark.asyncio
    async def test_toButton_withDpadDown(self):
        result = await self.mapper.toButton(CrowdControlInputType.DPAD_DOWN)
        assert result is CrowdControlButton.DPAD_DOWN

    @pytest.mark.asyncio
    async def test_toButton_withDpadLeft(self):
        result = await self.mapper.toButton(CrowdControlInputType.DPAD_LEFT)
        assert result is CrowdControlButton.DPAD_LEFT

    @pytest.mark.asyncio
    async def test_toButton_withDpadRight(self):
        result = await self.mapper.toButton(CrowdControlInputType.DPAD_RIGHT)
        assert result is CrowdControlButton.DPAD_RIGHT

    @pytest.mark.asyncio
    async def test_toButton_withDpadUp(self):
        result = await self.mapper.toButton(CrowdControlInputType.DPAD_UP)
        assert result is CrowdControlButton.DPAD_UP

    @pytest.mark.asyncio
    async def test_toButton_withGameShuffle(self):
        result: CrowdControlButton | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.toButton(CrowdControlInputType.GAME_SHUFFLE)

        assert result is None

    @pytest.mark.asyncio
    async def test_toButton_withNone(self):
        result = await self.mapper.toButton(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_toButton_withSelect(self):
        result = await self.mapper.toButton(CrowdControlInputType.SELECT)
        assert result is CrowdControlButton.SELECT

    @pytest.mark.asyncio
    async def test_toButton_withStart(self):
        result = await self.mapper.toButton(CrowdControlInputType.START)
        assert result is CrowdControlButton.START

    @pytest.mark.asyncio
    async def test_toButton_withTriggerLeft(self):
        result = await self.mapper.toButton(CrowdControlInputType.TRIGGER_LEFT)
        assert result is CrowdControlButton.TRIGGER_LEFT

    @pytest.mark.asyncio
    async def test_toButton_withTriggerRight(self):
        result = await self.mapper.toButton(CrowdControlInputType.TRIGGER_RIGHT)
        assert result is CrowdControlButton.TRIGGER_RIGHT

    @pytest.mark.asyncio
    async def test_toButton_withUserInputButton(self):
        result: CrowdControlButton | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.toButton(CrowdControlInputType.USER_INPUT_BUTTON)

        assert result is None
