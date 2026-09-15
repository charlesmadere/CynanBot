import re
import traceback
from dataclasses import dataclass
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..chatterPreferredTts.chatterPreferredTtsPresenter import ChatterPreferredTtsPresenter
from ..chatterPreferredTts.exceptions import FailedToChooseRandomTtsException, NoEnabledTtsProvidersException, \
    TtsProviderIsNotEnabledException, UnableToParseUserMessageIntoTtsException
from ..chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ..chatterPreferredTts.models.chatterPrefferedTts import ChatterPreferredTts
from ..chatterPreferredTts.settings.chatterPreferredTtsSettingsRepositoryInterface import \
    ChatterPreferredTtsSettingsRepositoryInterface
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..twitch.userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface
from ..users.userInterface import UserInterface


class SetChatterPreferredTtsChatCommand(AbsChatCommand):

    @dataclass(frozen = True, slots = True)
    class Arguments:
        newPreferredTts: ChatterPreferredTts
        chatterUserId: str
        chatterUserLogin: str
        chatterUserName: str
        newPreferredTtsString: str

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        chatterPreferredTtsPresenter: ChatterPreferredTtsPresenter,
        chatterPreferredTtsSettingsRepository: ChatterPreferredTtsSettingsRepositoryInterface,
        timber: TimberInterface,
        ttsJsonMapper: TtsJsonMapperInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(chatterPreferredTtsPresenter, ChatterPreferredTtsPresenter):
            raise TypeError(f'chatterPreferredTtsPresenter argument is malformed: \"{chatterPreferredTtsPresenter}\"')
        elif not isinstance(chatterPreferredTtsSettingsRepository, ChatterPreferredTtsSettingsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsSettingsRepository argument is malformed: \"{chatterPreferredTtsSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchUserIdsHelper, TwitchUserIdsHelperInterface):
            raise TypeError(f'twitchUserIdsHelper argument is malformed: \"{twitchUserIdsHelper}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface] = chatterPreferredTtsHelper
        self.__chatterPreferredTtsPresenter: Final[ChatterPreferredTtsPresenter] = chatterPreferredTtsPresenter
        self.__chatterPreferredTtsSettingsRepository: Final[ChatterPreferredTtsSettingsRepositoryInterface] = chatterPreferredTtsSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__ttsJsonMapper: Final[TtsJsonMapperInterface] = ttsJsonMapper
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!set(?:preferred)?tts(?:provider)?\b', re.IGNORECASE),
        })

        self.__argumentsRegEx: Final[Pattern] = re.compile(r'^\s*!\w+\s+@?(\w+)\s+(\w+)', re.IGNORECASE)
        self.__randomRegEx: Final[Pattern] = re.compile(r'^\s*[\'\"]?rando(?:m(?:ize)?)?[\'\"]?\s*$', re.IGNORECASE)

    @property
    def commandName(self) -> str:
        return 'SetChatterPreferredTtsChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def __getExampleTtsProvider(self, twitchUser: UserInterface) -> str:
        return await self.__ttsJsonMapper.asyncSerializeProvider(
            ttsProvider = twitchUser.defaultTtsProvider,
        )

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isChatterPreferredTtsEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__chatterPreferredTtsSettingsRepository.isEnabled():
            return ChatCommandResult.IGNORED
        elif not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        try:
            arguments = await self.__parseArguments(
                chatMessage = chatMessage,
            )
        except (FailedToChooseRandomTtsException, NoEnabledTtsProvidersException, UnableToParseUserMessageIntoTtsException) as e:
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to set preferred TTS! Please check your input and try again.',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Failed to set preferred TTS ({chatMessage=})', e, traceback.format_exc())
            return ChatCommandResult.CONSUMED
        except TtsProviderIsNotEnabledException as e:
            self.__twitchChatMessenger.send(
                text = f'⚠ The TTS provider requested is not available! Please try a different TTS provider.',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'The given TTS Provider is not enabled ({chatMessage=})', e, traceback.format_exc())
            return ChatCommandResult.CONSUMED

        if arguments is None:
            exampleTtsProvider = await self.__getExampleTtsProvider(
                twitchUser = chatMessage.twitchUser,
            )

            self.__twitchChatMessenger.send(
                text = f'⚠ Invalid arguments! Example use: !setpreferredtts @{chatMessage.chatterUserLogin} {exampleTtsProvider}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Invalid arguments ({arguments=}) ({chatMessage=})')
            return ChatCommandResult.CONSUMED

        printOut = await self.__chatterPreferredTtsPresenter.printOut(
            preferredTts = arguments.newPreferredTts,
        )

        self.__twitchChatMessenger.send(
            text = f'ⓘ New preferred TTS set for @{arguments.chatterUserLogin} — {printOut}',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Consumed ({arguments=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId

        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()

        return isStreamer or isAdministrator

    async def __parseArguments(self, chatMessage: TwitchChatMessage) -> Arguments | None:
        argumentsMatch = self.__argumentsRegEx.match(chatMessage.text)
        if argumentsMatch is None:
            return None

        chatterUserName = argumentsMatch.group(1)

        try:
            chatterUserData = await self.__twitchUserIdsHelper.requireByLoginOrName(
                userLoginOrName = chatterUserName,
                twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                    twitchChannelId = chatMessage.twitchChannelId,
                ),
            )
        except Exception as e:
            self.__timber.log(self.commandName, f'Failed to fetch user data for the given chatter username ({chatterUserName=}) ({argumentsMatch=}) ({chatMessage=})', e, traceback.format_exc())
            return None

        preferredTtsString = argumentsMatch.group(2)
        preferredTts: ChatterPreferredTts

        if self.__randomRegEx.fullmatch(preferredTtsString):
            preferredTts = await self.__chatterPreferredTtsHelper.applyRandomPreferredTts(
                chatterUserId = chatterUserData.userId,
                twitchChannelId = chatMessage.twitchChannelId,
            )
        else:
            preferredTts = await self.__chatterPreferredTtsHelper.applyUserMessagePreferredTts(
                chatterUserId = chatterUserData.userId,
                twitchChannelId = chatMessage.twitchChannelId,
                userMessage = preferredTtsString,
            )

        return SetChatterPreferredTtsChatCommand.Arguments(
            newPreferredTts = preferredTts,
            chatterUserId = chatterUserData.userId,
            chatterUserLogin = chatterUserData.userLogin,
            chatterUserName = chatterUserData.userName,
            newPreferredTtsString = preferredTtsString,
        )
