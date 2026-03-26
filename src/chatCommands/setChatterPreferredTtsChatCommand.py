import re
import traceback
from dataclasses import dataclass
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..chatterPreferredTts.chatterPreferredTtsPresenter import ChatterPreferredTtsPresenter
from ..chatterPreferredTts.exceptions import FailedToChooseRandomTtsException, NoEnabledTtsProvidersException, \
    TtsProviderIsNotEnabledException, UnableToParseUserMessageIntoTtsException
from ..chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ..chatterPreferredTts.models.chatterPrefferedTts import ChatterPreferredTts
from ..chatterPreferredTts.settings.chatterPreferredTtsSettingsRepositoryInterface import \
    ChatterPreferredTtsSettingsRepositoryInterface
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.userInterface import UserInterface


class SetChatterPreferredTtsChatCommand(AbsChatCommand2):

    @dataclass(frozen = True, slots = True)
    class LookupUserInfo:
        userId: str | None
        userName: str

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        chatterPreferredTtsPresenter: ChatterPreferredTtsPresenter,
        chatterPreferredTtsSettingsRepository: ChatterPreferredTtsSettingsRepositoryInterface,
        timber: TimberInterface,
        ttsJsonMapper: TtsJsonMapperInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        userIdsRepository: UserIdsRepositoryInterface,
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
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface] = chatterPreferredTtsHelper
        self.__chatterPreferredTtsPresenter: Final[ChatterPreferredTtsPresenter] = chatterPreferredTtsPresenter
        self.__chatterPreferredTtsSettingsRepository: Final[ChatterPreferredTtsSettingsRepositoryInterface] = chatterPreferredTtsSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__ttsJsonMapper: Final[TtsJsonMapperInterface] = ttsJsonMapper
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!set(?:preferred)?tts(?:provider)?\b', re.IGNORECASE),
        })

        self.__randomRegEx: Final[Pattern] = re.compile(r'^\s*\"?random(?:ize)?\"?\s*$', re.IGNORECASE)

    @property
    def commandName(self) -> str:
        return 'SetChatterPreferredTtsChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def __getExampleTtsProvider(self, user: UserInterface) -> str:
        return await self.__ttsJsonMapper.asyncSerializeProvider(
            ttsProvider = user.defaultTtsProvider
        )

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isChatterPreferredTtsEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__chatterPreferredTtsSettingsRepository.isEnabled():
            return ChatCommandResult.IGNORED
        elif not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        exampleTtsProvider = await self.__getExampleTtsProvider(chatMessage.twitchUser)

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 3:
            self.__twitchChatMessenger.send(
                text = f'⚠ Username and preferred TTS voice is necessary for this command. Example: !setpreferredtts @{twitchHandle} {exampleTtsProvider}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Less than 2 arguments given ({splits=}) ({chatMessage=})')
            return ChatCommandResult.HANDLED

        lookupUser = await self.__lookupUser(
            twitchChannelId = chatMessage.twitchChannelId,
            userName = splits[1],
        )

        if lookupUser is None:
            self.__twitchChatMessenger.send(
                text = f'⚠ Username and preferred TTS voice is necessary for this command. Example: !setpreferredtts @{twitchHandle} {exampleTtsProvider}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Encountered invalid username argument ({lookupUser=}) ({splits=}) ({chatMessage=})')
            return ChatCommandResult.HANDLED
        elif not utils.isValidStr(lookupUser.userId):
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to find info for user \"{lookupUser.userName}\". A username and preferred TTS voice is necessary for this command. Example: !setpreferredtts @{twitchHandle} {exampleTtsProvider}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Encountered unknown username argument ({lookupUser=}) ({splits=}) ({chatMessage=})')
            return ChatCommandResult.HANDLED

        userMessage = utils.cleanStr(' '.join(splits[2:]))
        preferredTts: ChatterPreferredTts

        try:
            if self.__randomRegEx.fullmatch(userMessage):
                preferredTts = await self.__chatterPreferredTtsHelper.applyRandomPreferredTts(
                    chatterUserId = lookupUser.userId,
                    twitchChannelId = chatMessage.twitchChannelId,
                )
            else:
                preferredTts = await self.__chatterPreferredTtsHelper.applyUserMessagePreferredTts(
                    chatterUserId = lookupUser.userId,
                    twitchChannelId = chatMessage.twitchChannelId,
                    userMessage = userMessage,
                )
        except (FailedToChooseRandomTtsException, NoEnabledTtsProvidersException, UnableToParseUserMessageIntoTtsException) as e:
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to set preferred TTS for @{lookupUser.userName}! Please check your input and try again.',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Failed to set preferred TTS ({lookupUser=}) ({userMessage=}) ({splits=}) ({chatMessage=})', e, traceback.format_exc())
            return ChatCommandResult.HANDLED
        except TtsProviderIsNotEnabledException as e:
            self.__twitchChatMessenger.send(
                text = f'⚠ The TTS provider requested for @{lookupUser.userName} is not available! Please try a different TTS provider.',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'The given TTS Provider is not enabled ({lookupUser=}) ({userMessage=}) ({splits=}) ({chatMessage=})', e, traceback.format_exc())
            return ChatCommandResult.HANDLED

        printOut = await self.__chatterPreferredTtsPresenter.printOut(
            preferredTts = preferredTts,
        )

        self.__twitchChatMessenger.send(
            text = f'ⓘ New preferred TTS set for @{lookupUser.userName} — {printOut}',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({preferredTts=}) ({lookupUser=}) ({chatMessage=})')
        return ChatCommandResult.HANDLED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId

        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()

        return isStreamer or isAdministrator

    async def __lookupUser(
        self,
        twitchChannelId: str,
        userName: str | None,
    ) -> LookupUserInfo | None:
        if not utils.isValidStr(userName):
            return None

        userName = utils.removePreceedingAt(userName)
        if not utils.strContainsAlphanumericCharacters(userName):
            return None

        userId = await self.__userIdsRepository.fetchUserId(
            userName = userName,
            twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                twitchChannelId = twitchChannelId,
            ),
        )

        return SetChatterPreferredTtsChatCommand.LookupUserInfo(
            userId = userId,
            userName = userName,
        )
