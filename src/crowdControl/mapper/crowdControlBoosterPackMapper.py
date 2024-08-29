from datetime import datetime

from .crowdControlBoosterPackMapperInterface import CrowdControlBoosterPackMapperInterface
from ..actions.buttonPressCrowdControlAction import ButtonPressCrowdControlAction
from ..actions.crowdControlAction import CrowdControlAction
from ..actions.crowdControlButton import CrowdControlButton
from ..actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from ..idGenerator.crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...users.crowdControl.crowdControlBoosterPack import CrowdControlBoosterPack
from ...users.crowdControl.crowdControlInputType import CrowdControlInputType


class CrowdControlBoosterPackMapper(CrowdControlBoosterPackMapperInterface):

    def __init__(
        self,
        crowdControlIdGenerator: CrowdControlIdGeneratorInterface,
        timeZoneRepository: TimeZoneRepositoryInterface
    ):
        if not isinstance(crowdControlIdGenerator, CrowdControlIdGeneratorInterface):
            raise TypeError(f'crowdControlIdGenerator argument is malformed: \"{crowdControlIdGenerator}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__crowdControlIdGenerator: CrowdControlIdGeneratorInterface = crowdControlIdGenerator
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

    async def toAction(
        self,
        boosterPack: CrowdControlBoosterPack,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> CrowdControlAction:
        if not isinstance(boosterPack, CrowdControlBoosterPack):
            raise TypeError(f'boosterPack argument is malformed: \"{boosterPack}\"')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(chatterUserName):
            raise TypeError(f'chatterUserName argument is malformed: \"{chatterUserName}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        dateTime = datetime.now(self.__timeZoneRepository.getDefault())
        actionId = await self.__crowdControlIdGenerator.generateActionId()

        if boosterPack.inputType is CrowdControlInputType.GAME_SHUFFLE:
            return GameShuffleCrowdControlAction(
                dateTime = dateTime,
                actionId = actionId,
                chatterUserId = chatterUserId,
                chatterUserName = chatterUserName,
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId
            )
        else:
            button = await self.toButton(
                inputType = boosterPack.inputType
            )

            return ButtonPressCrowdControlAction(
                button = button,
                dateTime = dateTime,
                actionId = actionId,
                chatterUserId = chatterUserId,
                chatterUserName = chatterUserName,
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId
            )

    async def toButton(
        self,
        inputType: CrowdControlInputType
    ) -> CrowdControlButton:
        if not isinstance(inputType, CrowdControlInputType):
            raise TypeError(f'inputType argument is malformed: \"{inputType}\"')

        match inputType:
            case CrowdControlInputType.BUTTON_A: return CrowdControlButton.BUTTON_A
            case CrowdControlInputType.BUTTON_B: return CrowdControlButton.BUTTON_B
            case CrowdControlInputType.BUTTON_X: return CrowdControlButton.BUTTON_X
            case CrowdControlInputType.BUTTON_Y: return CrowdControlButton.BUTTON_Y
            case CrowdControlInputType.DPAD_DOWN: return CrowdControlButton.DPAD_DOWN
            case CrowdControlInputType.DPAD_LEFT: return CrowdControlButton.DPAD_LEFT
            case CrowdControlInputType.DPAD_RIGHT: return CrowdControlButton.DPAD_RIGHT
            case CrowdControlInputType.DPAD_UP: return CrowdControlButton.DPAD_UP
            case CrowdControlInputType.GAME_SHUFFLE: raise ValueError(f'Encountered unsupported CrowdControlInputType: \"{inputType}\"')
            case CrowdControlInputType.SELECT: return CrowdControlButton.SELECT
            case CrowdControlInputType.START: return CrowdControlButton.START
            case CrowdControlInputType.TRIGGER_LEFT: return CrowdControlButton.TRIGGER_LEFT
            case CrowdControlInputType.TRIGGER_RIGHT: return CrowdControlButton.TRIGGER_RIGHT
            case _: raise ValueError(f'Encountered unknown CrowdControlInputType: \"{inputType}\"')
