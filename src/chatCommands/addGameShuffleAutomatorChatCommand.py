import locale
import re
import traceback
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..crowdControl.automator.crowdControlAutomatorAddResult import CrowdControlAutomatorAddResult
from ..crowdControl.automator.crowdControlAutomatorData import CrowdControlAutomatorData
from ..crowdControl.automator.crowdControlAutomatorInterface import CrowdControlAutomatorInterface
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class AddGameShuffleAutomatorChatCommand(AbsChatCommand2):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        crowdControlAutomator: CrowdControlAutomatorInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        if not isinstance(crowdControlAutomator, CrowdControlAutomatorInterface):
            raise TypeError(f'crowdControlAutomator argument is malformed: \"{crowdControlAutomator}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__crowdControlAutomator: Final[CrowdControlAutomatorInterface] = crowdControlAutomator
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!addgameshuffleautomator\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'AddGameShuffleAutomatorChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isCrowdControlEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            self.__twitchChatMessenger.send(
                text = f'⚠ A number of seconds argument is necessary for the !addgameshuffleautomator command. Example using 5 minutes: !addgameshuffleautomator 300',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Less than 2 arguments ({splits=}) ({chatMessage=})')
            return ChatCommandResult.CONSUMED

        reoccurSecondsString = splits[1]

        try:
            reoccurSeconds = int(reoccurSecondsString)
        except Exception as e:
            self.__twitchChatMessenger.send(
                text = f'⚠ The given number of seconds argument is malformed. Example using 5 minutes: !addgameshuffleautomator 300',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Unable to convert reoccur seconds into an int ({reoccurSecondsString=}) ({splits=}) ({chatMessage=})', e, traceback.format_exc())
            return ChatCommandResult.CONSUMED

        if reoccurSeconds < 10 or reoccurSeconds > utils.getIntMaxSafeSize():
            self.__twitchChatMessenger.send(
                text = f'⚠ The given number of seconds argument is out of bounds. Example using 5 minutes: !addgameshuffleautomator 300',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log('AddGameShuffleAutomatorChatCommand', f'The reoccur seconds argument is out of bounds ({reoccurSeconds=}) ({reoccurSecondsString=}) ({splits=}) ({chatMessage=})')
            return ChatCommandResult.CONSUMED

        result = await self.__crowdControlAutomator.addGameShuffleAutomator(CrowdControlAutomatorData(
            reoccurSeconds = reoccurSeconds,
            twitchChannelId = chatMessage.twitchChannelId,
        ))

        reoccurSecondsString = locale.format_string("%d", reoccurSeconds, grouping = True)

        match result:
            case CrowdControlAutomatorAddResult.OK:
                self.__twitchChatMessenger.send(
                    text = f'ⓘ Added {reoccurSecondsString} second(s) game shuffle automator',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

            case CrowdControlAutomatorAddResult.REPLACED:
                self.__twitchChatMessenger.send(
                    text = f'ⓘ Replaced existing game shuffle automator with a new {reoccurSecondsString} second(s) game shuffle automator',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

            case _:
                raise RuntimeError(f'Unknown CrowdControlAutomatorAddResult: \"{result}\"')

        self.__timber.log(self.commandName, f'Handled ({result=}) ({reoccurSeconds=}) ({splits=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId
        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()
        return isStreamer or isAdministrator
