import re
import traceback
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..language.languagesRepositoryInterface import LanguagesRepositoryInterface
from ..language.wordOfTheDay.wordOfTheDayPresenterInterface import WordOfTheDayPresenterInterface
from ..language.wordOfTheDay.wordOfTheDayRepositoryInterface import WordOfTheDayRepositoryInterface
from ..language.wordOfTheDay.wordOfTheDayResponse import WordOfTheDayResponse
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class WordChatCommand(AbsChatCommand2):

    def __init__(
        self,
        languagesRepository: LanguagesRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        wordOfTheDayPresenter: WordOfTheDayPresenterInterface,
        wordOfTheDayRepository: WordOfTheDayRepositoryInterface,
    ):
        if not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(wordOfTheDayPresenter, WordOfTheDayPresenterInterface):
            raise TypeError(f'wordOfTheDayPresenter argument is malformed: \"{wordOfTheDayPresenter}\"')
        elif not isinstance(wordOfTheDayRepository, WordOfTheDayRepositoryInterface):
            raise TypeError(f'wordOfTheDayRepository argument is malformed: \"{wordOfTheDayRepository}\"')

        self.__languagesRepository: Final[LanguagesRepositoryInterface] = languagesRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__wordOfTheDayPresenter: Final[WordOfTheDayPresenterInterface] = wordOfTheDayPresenter
        self.__wordOfTheDayRepository: Final[WordOfTheDayRepositoryInterface] = wordOfTheDayRepository

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!word\b', re.IGNORECASE),
            re.compile(r'^\s*!wordoftheday\b', re.IGNORECASE),
            re.compile(r'^\s*!wotd\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'WordChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isWordOfTheDayEnabled:
            return ChatCommandResult.IGNORED

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            exampleEntry = await self.__languagesRepository.getExampleLanguageEntry(hasWotdApiCode = True)
            allWotdApiCodes = await self.__languagesRepository.getAllWotdApiCodes()
            self.__twitchChatMessenger.send(
                text = f'⚠ A language code is necessary for the !word command. Example: !word {exampleEntry.requireWotdApiCode()}. Available languages: {allWotdApiCodes}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.HANDLED

        language: str | None = splits[1]
        if not utils.isValidStr(language):

            return ChatCommandResult.HANDLED

        try:
            languageEntry = await self.__languagesRepository.requireLanguageForCommand(
                command = language,
                hasWotdApiCode = True
            )
        except Exception as e:
            allWotdApiCodes = await self.__languagesRepository.getAllWotdApiCodes()

            self.__twitchChatMessenger.send(
                text = f'⚠ The given language code is not supported by the !word command. Available languages: {allWotdApiCodes}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Error retrieving LanguageEntry ({language=})', e, traceback.format_exc())
            return ChatCommandResult.HANDLED

        wordOfTheDayResponse: WordOfTheDayResponse | None = None

        try:
            wordOfTheDayResponse = await self.__wordOfTheDayRepository.fetchWotd(
                languageEntry = languageEntry,
            )

            printOut = await self.__wordOfTheDayPresenter.toString(
                includeRomaji = False,
                wordOfTheDay = wordOfTheDayResponse,
            )

            self.__twitchChatMessenger.send(
                text = printOut,
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
        except Exception as e:
            self.__twitchChatMessenger.send(
                text = f'⚠ Error fetching Word Of The Day for \"{languageEntry.humanName}\"',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Error fetching Word Of The Day ({wordOfTheDayResponse=}) ({languageEntry=}) ({chatMessage=})', e, traceback.format_exc())

        self.__timber.log(self.commandName, f'Handled ({wordOfTheDayResponse=}) ({languageEntry=}) ({chatMessage=})')
        return ChatCommandResult.HANDLED
