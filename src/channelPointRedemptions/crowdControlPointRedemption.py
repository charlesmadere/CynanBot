from datetime import datetime

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..crowdControl.actions.buttonPressCrowdControlAction import ButtonPressCrowdControlAction
from ..crowdControl.actions.crowdControlButton import CrowdControlButton
from ..crowdControl.actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from ..crowdControl.crowdControlMachineInterface import CrowdControlMachineInterface
from ..crowdControl.idGenerator.crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface
from ..crowdControl.mapper.crowdControlInputTypeMapperInterface import CrowdControlInputTypeMapperInterface
from ..crowdControl.utils.crowdControlUserInputUtilsInterface import CrowdControlUserInputUtilsInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage
from ..users.crowdControl.crowdControlInputType import CrowdControlInputType


class CrowdControlPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        crowdControlIdGenerator: CrowdControlIdGeneratorInterface,
        crowdControlInputTypeMapper: CrowdControlInputTypeMapperInterface,
        crowdControlMachine: CrowdControlMachineInterface,
        crowdControlUserInputUtils: CrowdControlUserInputUtilsInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface
    ):
        if not isinstance(crowdControlIdGenerator, CrowdControlIdGeneratorInterface):
            raise TypeError(f'crowdControlIdGenerator argument is malformed: \"{crowdControlIdGenerator}\"')
        elif not isinstance(crowdControlInputTypeMapper, CrowdControlInputTypeMapperInterface):
            raise TypeError(f'crowdControlBoosterPackMapper argument is malformed: \"{crowdControlInputTypeMapper}\"')
        elif not isinstance(crowdControlMachine, CrowdControlMachineInterface):
            raise TypeError(f'crowdControlMachine argument is malformed: \"{crowdControlMachine}\"')
        elif not isinstance(crowdControlUserInputUtils, CrowdControlUserInputUtilsInterface):
            raise TypeError(f'crowdControlUserInputUtils argument is malformed: \"{crowdControlUserInputUtils}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__crowdControlIdGenerator: CrowdControlIdGeneratorInterface = crowdControlIdGenerator
        self.__crowdControlInputTypeMapper: CrowdControlInputTypeMapperInterface = crowdControlInputTypeMapper
        self.__crowdControlMachine: CrowdControlMachineInterface = crowdControlMachine
        self.__crowdControlUserInputUtils: CrowdControlUserInputUtilsInterface = crowdControlUserInputUtils
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.twitchUser
        if not twitchUser.isCrowdControlEnabled:
            return False

        boosterPacks = twitchUser.crowdControlBoosterPacks
        if boosterPacks is None or len(boosterPacks) == 0:
            return False

        boosterPack = boosterPacks.get(twitchChannelPointsMessage.rewardId, None)
        if boosterPack is None:
            return False

        now = datetime.now(self.__timeZoneRepository.getDefault())
        actionId = await self.__crowdControlIdGenerator.generateActionId()

        if boosterPack.inputType is CrowdControlInputType.GAME_SHUFFLE:
            self.__crowdControlMachine.submitAction(GameShuffleCrowdControlAction(
                dateTime = now,
                entryWithinGigaShuffle = False,
                startOfGigaShuffleSize = None,
                actionId = actionId,
                chatterUserId = twitchChannelPointsMessage.userId,
                chatterUserName = twitchChannelPointsMessage.userName,
                twitchChannel = twitchUser.handle,
                twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
                twitchChatMessageId = None,
            ))

            self.__timber.log('CrowdControlPointRedemption', f'Created new game shuffle crowd control action from channel point redemption ({twitchChannelPointsMessage=}) ({boosterPack=})')
            return True

        button: CrowdControlButton | None

        if boosterPack.inputType is CrowdControlInputType.USER_INPUT_BUTTON:
            button = await self.__crowdControlUserInputUtils.parseButtonFromUserInput(
                userInput = twitchChannelPointsMessage.redemptionMessage,
            )
        else:
            button = await self.__crowdControlInputTypeMapper.toButton(
                inputType = boosterPack.inputType,
            )

        if button is None:
            self.__timber.log('CrowdControlPointRedemption', f'Unable to create crowd control action from channel point redemption ({twitchChannelPointsMessage=}) ({boosterPack=}) ({button=})')
            return False

        self.__crowdControlMachine.submitAction(ButtonPressCrowdControlAction(
            button = button,
            dateTime = now,
            actionId = actionId,
            chatterUserId = twitchChannelPointsMessage.userId,
            chatterUserName = twitchChannelPointsMessage.userName,
            twitchChannel = twitchUser.handle,
            twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
            twitchChatMessageId = None,
        ))

        self.__timber.log('CrowdControlPointRedemption', f'Created new button press crowd control action from channel point redemption ({twitchChannelPointsMessage=}) ({boosterPack=}) ({button=})')
        return True
