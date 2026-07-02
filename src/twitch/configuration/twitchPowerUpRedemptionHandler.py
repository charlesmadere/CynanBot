from typing import Final

from ..absTwitchPowerUpRedemptionHandler import AbsTwitchPowerUpRedemptionHandler
from ..api.models.twitchCustomPowerUp import TwitchCustomPowerUp as ApiTwitchCustomPowerUp
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..localModels.twitchCustomPowerUp import TwitchCustomPowerUp
from ..localModels.twitchPowerUpRedemption import TwitchPowerUpRedemption
from ...cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...users.userInterface import UserInterface


class TwitchPowerUpRedemptionHandler(AbsTwitchPowerUpRedemptionHandler):

    def __init__(
        self,
        cheerActionHelper: CheerActionHelperInterface | None,
        timber: TimberInterface,
    ):
        if cheerActionHelper is not None and not isinstance(cheerActionHelper, CheerActionHelperInterface):
            raise TypeError(f'cheerActionHelper argument is malformed: \"{cheerActionHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__cheerActionHelper: Final[CheerActionHelperInterface | None] = cheerActionHelper
        self.__timber: Final[TimberInterface] = timber

    async def onNewPowerUpRedemption(self, powerUpRedemption: TwitchPowerUpRedemption):
        if not isinstance(powerUpRedemption, TwitchPowerUpRedemption):
            raise TypeError(f'powerUpRedemption argument is malformed: \"{powerUpRedemption}\"')

        await self.__processCheerAction(
            powerUpRedemption = powerUpRedemption,
        )

    async def onNewPowerUpRedemptionDataBundle(
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
            self.__timber.log('TwitchPowerUpRedemptionHandler', f'Received a data bundle that has no event ({user=}) ({dataBundle=})')
            return

        redemptionUserId = event.userId
        redemptionUserLogin = event.userLogin
        redemptionUserName = event.userName
        customPowerUp = await self.__mapApiCustomPowerUp(event.customPowerUp)

        if not utils.isValidStr(redemptionUserId) or not utils.isValidStr(redemptionUserLogin) or not utils.isValidStr(redemptionUserName) or customPowerUp is None:
            self.__timber.log('TwitchPowerUpRedemptionHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({twitchChannelId=}) ({dataBundle=}) ({redemptionUserId=}) ({redemptionUserLogin=}) ({redemptionUserName=}) ({customPowerUp=})')
            return

        if event.chatMessage is not None:
            # just including this for testing/debug purposes for the time being
            self.__timber.log('TwitchPowerUpRedemptionHandler', f'This event has a chat message ({user=}) ({twitchChannelId=}) ({dataBundle=}) ({redemptionUserId=}) ({redemptionUserLogin=}) ({redemptionUserName=}) ({customPowerUp=})')

        powerUpRedemption = TwitchPowerUpRedemption(
            eventId = dataBundle.metadata.messageId,
            redemptionMessage = event.userInput,
            redemptionUserId = redemptionUserId,
            redemptionUserLogin = redemptionUserLogin,
            redemptionUserName = redemptionUserName,
            twitchChannelId = twitchChannelId,
            customPowerUp = customPowerUp,
            twitchUser = user,
        )

        await self.onNewPowerUpRedemption(
            powerUpRedemption = powerUpRedemption,
        )

    async def __processCheerAction(self, powerUpRedemption: TwitchPowerUpRedemption):
        if self.__cheerActionHelper is None:
            return
        elif not powerUpRedemption.twitchUser.areCheerActionsEnabled:
            return
        elif powerUpRedemption.bits < 1:
            return

        self.__cheerActionHelper.submitCheer(CheerActionHelperInterface.CheerInfo(
            bits = powerUpRedemption.bits,
            cheerUserId = powerUpRedemption.redemptionUserId,
            cheerUserLogin = powerUpRedemption.redemptionUserLogin,
            cheerUserName = powerUpRedemption.redemptionUserName,
            message = powerUpRedemption.redemptionMessage,
            twitchChannelId = powerUpRedemption.twitchChannelId,
            twitchChatMessageId = None,
            twitchUser = powerUpRedemption.twitchUser,
        ))

    async def __mapApiCustomPowerUp(
        self,
        apiCustomPowerUp: ApiTwitchCustomPowerUp | None,
    ) -> TwitchCustomPowerUp | None:
        if apiCustomPowerUp is None:
            return None

        return TwitchCustomPowerUp(
            bits = apiCustomPowerUp.bits,
            prompt = apiCustomPowerUp.prompt,
            powerUpId = apiCustomPowerUp.powerUpId,
            title = apiCustomPowerUp.title,
        )
