import re
import traceback
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..cuteness.cutenessPresenterInterface import CutenessPresenterInterface
from ..cuteness.exceptions import CutenessFeatureIsDisabledException
from ..cuteness.helpers.cutenessHelperInterface import CutenessHelperInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class MyCutenessChatCommand(AbsChatCommand):

    def __init__(
        self,
        cutenessHelper: CutenessHelperInterface,
        cutenessPresenter: CutenessPresenterInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(cutenessHelper, CutenessHelperInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessHelper}\"')
        elif not isinstance(cutenessPresenter, CutenessPresenterInterface):
            raise TypeError(f'cutenessPresenter argument is malformed: \"{cutenessPresenter}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__cutenessHelper: Final[CutenessHelperInterface] = cutenessHelper
        self.__cutenessPresenter: Final[CutenessPresenterInterface] = cutenessPresenter
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!mycuteness(?:history)?\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'MyCutenessChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isCutenessEnabled:
            return ChatCommandResult.IGNORED

        try:
            result = await self.__cutenessHelper.fetchCutenessHistory(
                chatterUserId = chatMessage.chatterUserId,
                twitchChannelId = chatMessage.twitchChannelId,
            )
        except CutenessFeatureIsDisabledException as e:
            self.__timber.log(self.commandName, f'Failed to fetch history as the feature is disabled ({chatMessage=})', e, traceback.format_exc())
            return ChatCommandResult.IGNORED

        printOut = self.__cutenessPresenter.printCutenessHistory(
            result = result,
        )

        self.__twitchChatMessenger.send(
            text = printOut,
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Consumed ({result=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED
