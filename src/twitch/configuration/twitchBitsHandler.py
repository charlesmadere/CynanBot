from typing import Final

from ..absTwitchBitsHandler import AbsTwitchBitsHandler
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.models.twitchWebsocketEvent import TwitchWebsocketEvent
from ..localModels.mapper.twitchLocalModelsMapperInterface import TwitchLocalModelsMapperInterface
from ..localModels.twitchBitsUse import TwitchBitsUse
from ...cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...users.userInterface import UserInterface


class TwitchBitsHandler(AbsTwitchBitsHandler):

    def __init__(
        self,
        cheerActionHelper: CheerActionHelperInterface | None,
        timber: TimberInterface,
        twitchLocalModelsMapper: TwitchLocalModelsMapperInterface,
    ):
        if cheerActionHelper is not None and not isinstance(cheerActionHelper, CheerActionHelperInterface):
            raise TypeError(f'cheerActionHelper argument is malformed: \"{cheerActionHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchLocalModelsMapper, TwitchLocalModelsMapperInterface):
            raise TypeError(f'twitchLocalModelsMapper argument is malformed: \"{twitchLocalModelsMapper}\"')

        self.__cheerActionHelper: Final[CheerActionHelperInterface | None] = cheerActionHelper
        self.__timber: Final[TimberInterface] = timber
        self.__twitchLocalModelsMapper: Final[TwitchLocalModelsMapperInterface] = twitchLocalModelsMapper

    async def onNewBits(self, bitsUse: TwitchBitsUse):
        if not isinstance(bitsUse, TwitchBitsUse):
            raise TypeError(f'bitsUse argument is malformed: \"{bitsUse}\"')

        await self.__processCheerAction(
            bitsUse = bitsUse,
        )

    async def onNewBitsDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.requirePayload().event

        if event is None:
            self.__timber.log('TwitchBitsHandler', f'Received a data bundle that has no event ({user=}) ({dataBundle=})')
            return

        bits = await self.__findBitsInEvent(event)
        bitsUserId = event.userId
        bitsUserLogin = event.userLogin
        bitsUserName = event.userName
        bitsUseType = await self.__twitchLocalModelsMapper.mapBitsUseType(event.bitsUseType)
        customPowerUpData = await self.__twitchLocalModelsMapper.mapCustomPowerUpData(event.customPowerUpData)

        if bits is None or not utils.isValidStr(bitsUserId) or not utils.isValidStr(bitsUserLogin) or not utils.isValidStr(bitsUserName) or bitsUseType is None:
            self.__timber.log('TwitchBitsHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({twitchChannelId=}) ({dataBundle=}) ({bits=}) ({bitsUserId=}) ({bitsUserLogin=}) ({bitsUserName=}) ({bitsUseType=}) ({customPowerUpData=})')
            return

        bitsUse = TwitchBitsUse(
            bits = bits,
            bitsUserId = bitsUserId,
            bitsUserLogin = bitsUserLogin,
            bitsUserName = bitsUserName,
            eventId = dataBundle.metadata.messageId,
            message = event.message,
            twitchChannelId = twitchChannelId,
            bitsUseType = bitsUseType,
            customPowerUpData = customPowerUpData,
            twitchUser = user,
        )

        await self.onNewBits(
            bitsUse = bitsUse,
        )

    async def __processCheerAction(self, bitsUse: TwitchBitsUse):
        if self.__cheerActionHelper is None:
            return
        elif not bitsUse.twitchUser.areCheerActionsEnabled:
            return
        elif bitsUse.bits < 1:
            return

        self.__cheerActionHelper.submitCheer(CheerActionHelperInterface.CheerInfo(
            bits = bitsUse.bits,
            cheerUserId = bitsUse.bitsUserId,
            cheerUserLogin = bitsUse.bitsUserLogin,
            cheerUserName = bitsUse.bitsUserName,
            message = bitsUse.message,
            twitchChannelId = bitsUse.twitchChannelId,
            twitchChatMessageId = None,
            twitchUser = bitsUse.twitchUser,
        ))

    async def __findBitsInEvent(
        self,
        event: TwitchWebsocketEvent,
    ) -> int | None:
        if event.cheer is not None and event.cheer.bits >= 1:
            return event.cheer.bits
        elif event.bits is not None and event.bits >= 1:
            return event.bits
        elif event.customPowerUp is not None and event.customPowerUp.bits >= 1:
            return event.customPowerUp.bits
        else:
            return None
