import re
import traceback
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..language.languageEntry import LanguageEntry
from ..language.languagesRepositoryInterface import LanguagesRepositoryInterface
from ..language.translationHelperInterface import TranslationHelperInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class TranslateChatCommand(AbsChatCommand2):

    def __init__(
        self,
        languagesRepository: LanguagesRepositoryInterface,
        timber: TimberInterface,
        translationHelper: TranslationHelperInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(translationHelper, TranslationHelperInterface):
            raise TypeError(f'translationHelper argument is malformed: \"{translationHelper}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__languagesRepository: Final[LanguagesRepositoryInterface] = languagesRepository
        self.__timber: Final[TimberInterface] = timber
        self.__translationHelper: Final[TranslationHelperInterface] = translationHelper
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!translate\b', re.IGNORECASE),
            re.compile(r'^\s*!translation\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'TranslateChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def __determineOptionalLanguageEntry(self, splits: list[str]) -> LanguageEntry | None:
        if len(splits[1]) >= 3 and splits[1][0:2] == '--':
            return await self.__languagesRepository.getLanguageForCommand(
                command = splits[1][2:],
                hasIso6391Code = True,
            )

        return None

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isTranslateEnabled:
            return ChatCommandResult.IGNORED

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            self.__twitchChatMessenger.send(
                text = f'⚠ Please specify the text you want to translate. Example: !translate I like tamales',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.CONSUMED

        targetLanguageEntry = await self.__determineOptionalLanguageEntry(
            splits = splits,
        )

        startSplitIndex = 1
        if targetLanguageEntry is not None:
            startSplitIndex = 2

        text = ' '.join(splits[startSplitIndex:])

        try:
            response = await self.__translationHelper.translate(
                text = text,
                targetLanguage = targetLanguageEntry,
            )

            self.__twitchChatMessenger.send(
                text = response.toStr(),
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
        except Exception as e:
            self.__timber.log(self.commandName, f'Error translating ({targetLanguageEntry=}) ({text=}) ({chatMessage=})', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = '⚠ Error translating',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        self.__timber.log(self.commandName, f'Handled ({targetLanguageEntry=}) ({text=}) ({chatMessage=})')
        return ChatCommandResult.HANDLED
