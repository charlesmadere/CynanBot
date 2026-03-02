import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..ecco.eccoHelperInterface import EccoHelperInterface
from ..ecco.exceptions import EccoFailedToFetchTimeRemaining
from ..ecco.models.absEccoTimeRemaining import AbsEccoTimeRemaining
from ..ecco.models.eccoReleased import EccoReleased
from ..ecco.models.eccoTimeRemaining import EccoTimeRemaining
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class EccoChatCommand(AbsChatCommand2):

    def __init__(
        self,
        eccoHelper: EccoHelperInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(eccoHelper, EccoHelperInterface):
            raise TypeError(f'eccoHelper argument is malformed: \"{eccoHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__eccoHelper: Final[EccoHelperInterface] = eccoHelper
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!ecco', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'EccoChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isEccoEnabled:
            return ChatCommandResult.IGNORED

        try:
            eccoTimeRemaining = await self.__eccoHelper.fetchEccoTimeRemaining()
        except EccoFailedToFetchTimeRemaining as e:
            self.__timber.log(self.commandName, f'Failed to fetch Ecco time remaining ({chatMessage=})', e)
            self.__twitchChatMessenger.send(
                text = f'⚠ Error fetching Ecco time remaining',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.HANDLED

        self.__twitchChatMessenger.send(
            text = await self.__toString(eccoTimeRemaining),
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({chatMessage=}) ({eccoTimeRemaining=})')
        return ChatCommandResult.HANDLED

    async def __toString(self, eccoTimeRemaining: AbsEccoTimeRemaining) -> str:
        if isinstance(eccoTimeRemaining, EccoReleased):
            return f'🐬 Ecco info is available now! https://www.eccothedolphin.com/'

        elif isinstance(eccoTimeRemaining, EccoTimeRemaining):
            durationMessage = utils.secondsToDurationMessage(eccoTimeRemaining.remainingSeconds)
            return f'🐬 New Ecco info coming in {durationMessage}!'

        else:
            raise RuntimeError(f'Encountered unknown AbsEccoTimeRemaining type: \"{eccoTimeRemaining}\"')
