import traceback
from typing import Final

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..chatterPreferredName.exceptions import ChatterPreferredNameFeatureIsDisabledException, \
    ChatterPreferredNameIsInvalidException
from ..chatterPreferredName.helpers.chatterPreferredNameHelperInterface import ChatterPreferredNameHelperInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage


class ChatterPreferredNamePointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        chatterPreferredNameHelper: ChatterPreferredNameHelperInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(chatterPreferredNameHelper, ChatterPreferredNameHelperInterface):
            raise TypeError(f'chatterPreferredNameHelper argument is malformed: \"{chatterPreferredNameHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__chatterPreferredTtsHelper: Final[ChatterPreferredNameHelperInterface] = chatterPreferredNameHelper
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage,
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.twitchUser
        if not twitchUser.isChatterPreferredNameEnabled:
            return False

        try:
            preferredNameData = await self.__chatterPreferredTtsHelper.set(
                chatterUserId = twitchChannelPointsMessage.userId,
                preferredName = twitchChannelPointsMessage.redemptionMessage,
                twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
            )
        except ChatterPreferredNameFeatureIsDisabledException as e:
            self.__timber.log('ChatterPreferredNamePointRedemption', f'Preferred name feature is disabled; redeemed by {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle} ({twitchChannelPointsMessage=})', e, traceback.format_exc())
            return False
        except ChatterPreferredNameIsInvalidException as e:
            self.__timber.log('ChatterPreferredNamePointRedemption', f'The given preferred name is invalid as redeemed by {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle} ({twitchChannelPointsMessage=})', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ @{twitchChannelPointsMessage.userName} unable to set your preferred name! Please check your input and try again.',
                twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
            )
            return False

        self.__twitchChatMessenger.send(
            text = f'ⓘ @{twitchChannelPointsMessage.userName} here\'s your new preferred name: {preferredNameData.preferredName}',
            twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
        )

        self.__timber.log('ChatterPreferredNamePointRedemption', f'Redeemed for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle}')
        return True
