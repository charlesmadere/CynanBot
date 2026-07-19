import math
import re
import traceback
from typing import Any, Collection, Final, Pattern

from frozenlist import FrozenList

from ..absTwitchChatHandler import AbsTwitchChatHandler
from ..activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..localModels.mapper.twitchLocalModelsMapperInterface import TwitchLocalModelsMapperInterface
from ..localModels.twitchChatMessage import TwitchChatMessage
from ..localModels.twitchChatMessageFragment import TwitchChatMessageFragment
from ..localModels.twitchChatMessageFragmentType import TwitchChatMessageFragmentType
from ..officialAccounts.officialTwitchAccountUserIdProviderInterface import \
    OfficialTwitchAccountUserIdProviderInterface
from ..tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...aniv.helpers.mostRecentAnivMessageTimeoutHelperInterface import MostRecentAnivMessageTimeoutHelperInterface
from ...chatActions.absChatAction import AbsChatAction
from ...chatActions.chatActionResult import ChatActionResult
from ...chatCommands.absChatCommand import AbsChatCommand
from ...chatCommands.chatCommandResult import ChatCommandResult
from ...chatLogger.chatLoggerInterface import ChatLoggerInterface
from ...cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from ...misc import utils as utils
from ...mostRecentChat.mostRecentChat import MostRecentChat
from ...mostRecentChat.mostRecentChatsRepositoryInterface import MostRecentChatsRepositoryInterface
from ...timber.timberInterface import TimberInterface
from ...trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from ...trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class TwitchChatHandler(AbsTwitchChatHandler):

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        chatLogger: ChatLoggerInterface,
        cheerActionHelper: CheerActionHelperInterface | None,
        mostRecentAnivMessageTimeoutHelper: MostRecentAnivMessageTimeoutHelperInterface | None,
        mostRecentChatsRepository: MostRecentChatsRepositoryInterface,
        officialTwitchAccountUserIdProvider: OfficialTwitchAccountUserIdProviderInterface,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface | None,
        triviaGameMachine: TriviaGameMachineInterface | None,
        twitchLocalModelsMapper: TwitchLocalModelsMapperInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        chatActions: Collection[AbsChatAction | Any | None] | None,
        chatCommands: Collection[AbsChatCommand | Any | None] | None,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif cheerActionHelper is not None and not isinstance(cheerActionHelper, CheerActionHelperInterface):
            raise TypeError(f'cheerActionHelper argument is malformed: \"{cheerActionHelper}\"')
        elif mostRecentAnivMessageTimeoutHelper is not None and not isinstance(mostRecentAnivMessageTimeoutHelper, MostRecentAnivMessageTimeoutHelperInterface):
            raise TypeError(f'mostRecentAnivMessageTimeoutHelper argument is malformed: \"{mostRecentAnivMessageTimeoutHelper}\"')
        elif not isinstance(mostRecentChatsRepository, MostRecentChatsRepositoryInterface):
            raise TypeError(f'mostRecentChatsRepository argument is malformed: \"{mostRecentChatsRepository}\"')
        elif not isinstance(officialTwitchAccountUserIdProvider, OfficialTwitchAccountUserIdProviderInterface):
            raise TypeError(f'officialTwitchAccountUserIdProvider argument is malformed: \"{officialTwitchAccountUserIdProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif triviaGameBuilder is not None and not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise TypeError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif triviaGameMachine is not None and not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(twitchLocalModelsMapper, TwitchLocalModelsMapperInterface):
            raise TypeError(f'twitchLocalModelsMapper argument is malformed: \"{twitchLocalModelsMapper}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif chatActions is not None and not isinstance(chatActions, Collection):
            raise TypeError(f'chatActions argument is malformed: \"{chatActions}\"')
        elif chatCommands is not None and not isinstance(chatCommands, Collection):
            raise TypeError(f'chatCommands argument is malformed: \"{chatCommands}\"')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__chatLogger: Final[ChatLoggerInterface] = chatLogger
        self.__cheerActionHelper: Final[CheerActionHelperInterface | None] = cheerActionHelper
        self.__mostRecentAnivMessageTimeoutHelper: Final[MostRecentAnivMessageTimeoutHelperInterface | None] = mostRecentAnivMessageTimeoutHelper
        self.__mostRecentChatsRepository: Final[MostRecentChatsRepositoryInterface] = mostRecentChatsRepository
        self.__officialTwitchAccountUserIdProvider: Final[OfficialTwitchAccountUserIdProviderInterface] = officialTwitchAccountUserIdProvider
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameBuilder: Final[TriviaGameBuilderInterface | None] = triviaGameBuilder
        self.__triviaGameMachine: Final[TriviaGameMachineInterface | None] = triviaGameMachine
        self.__twitchLocalModelsMapper: Final[TwitchLocalModelsMapperInterface] = twitchLocalModelsMapper
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__chatCommandPrefixRegEx: Final[Pattern] = re.compile(r'^\s*!\w+\b', re.IGNORECASE)

        self.__chatActions: Final[Collection[AbsChatAction]] = self.__buildChatActionsCollection(chatActions)
        self.__chatCommands: Final[Collection[AbsChatCommand]] = self.__buildChatCommandsCollection(chatCommands)

    def __buildChatActionsCollection(
        self,
        chatActions: Collection[AbsChatAction | Any | None] | None,
    ) -> Collection[AbsChatAction]:
        if chatActions is None:
            emptyChatActions: FrozenList[AbsChatAction] = FrozenList()
            emptyChatActions.freeze()
            return emptyChatActions

        frozenChatActions: FrozenList[AbsChatAction | Any | None] = FrozenList(chatActions)
        frozenChatActions.freeze()

        validChatActions: FrozenList[AbsChatAction] = FrozenList()

        for index, chatAction in enumerate(frozenChatActions):
            if chatAction is None:
                continue
            elif isinstance(chatAction, AbsChatAction):
                validChatActions.append(chatAction)
            else:
                exception = TypeError(f'Encountered an invalid AbsChatAction instance ({index=}) ({chatAction=}) ({frozenChatActions=})')
                self.__timber.log('TwitchChatHandler', f'Encountered an invalid AbsChatAction instance ({index=}) ({chatAction=}) ({frozenChatActions=})', exception, traceback.format_exc())
                raise exception

        validChatActions.freeze()
        return validChatActions

    def __buildChatCommandsCollection(
        self,
        chatCommands: Collection[AbsChatCommand | Any | None] | None,
    ) -> Collection[AbsChatCommand]:
        if chatCommands is None:
            return frozenset()

        frozenChatCommands: FrozenList[AbsChatCommand | Any | None] = FrozenList(chatCommands)
        frozenChatCommands.freeze()

        validChatCommands: set[AbsChatCommand] = set()

        for index, chatCommand in enumerate(frozenChatCommands):
            if chatCommand is None:
                continue
            elif isinstance(chatCommand, AbsChatCommand):
                validChatCommands.add(chatCommand)
            else:
                exception = TypeError(f'Encountered an invalid AbsChatCommand instance ({index=}) ({chatCommand=}) ({frozenChatCommands=})')
                self.__timber.log('TwitchChatHandler', f'Encountered an invalid AbsChatCommand instance ({index=}) ({chatCommand=}) ({frozenChatCommands=})', exception, traceback.format_exc())
                raise exception

        return frozenset(validChatCommands)

    async def __logChat(self, chatMessage: TwitchChatMessage):
        if not utils.isValidStr(chatMessage.text):
            return

        bits: int | None = None

        if chatMessage.cheerMetadata is not None and chatMessage.cheerMetadata.bits > 0:
            bits = chatMessage.cheerMetadata.bits

        self.__chatLogger.logMessage(
            bits = bits,
            chatterUserId = chatMessage.chatterUserId,
            chatterUserLogin = chatMessage.chatterUserLogin,
            message = chatMessage.text,
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
        )

    async def onNewChat(self, chatMessage: TwitchChatMessage):
        if not isinstance(chatMessage, TwitchChatMessage):
            raise TypeError(f'chatMessage argument is malformed: \"{chatMessage}\"')

        if utils.isValidStr(chatMessage.sourceMessageId):
            # This is a chat message that originated from a shared chat/stream. As such, let's not
            # even bother to process it or work with it at all. In the future, we may have a reason to
            # change this. But for now, it's better/easier to just ignore these messages completely.
            return

        if chatMessage.twitchUser.isChatLoggingEnabled:
            await self.__logChat(
                chatMessage = chatMessage,
            )

        await self.__activeChattersRepository.add(
            chatterUserId = chatMessage.chatterUserId,
            chatterUserLogin = chatMessage.chatterUserLogin,
            chatterUserName = chatMessage.chatterUserName,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        mostRecentChat = await self.__mostRecentChatsRepository.get(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        await self.__mostRecentChatsRepository.set(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        await self.__processChatActions(
            mostRecentChat = mostRecentChat,
            chatMessage = chatMessage,
        )

        if chatMessage.twitchUser.areCheerActionsEnabled:
            await self.__processCheerAction(
                chatMessage = chatMessage,
            )

        if chatMessage.twitchUser.isSuperTriviaGameEnabled:
            await self.__processSuperTriviaEvent(
                chatMessage = chatMessage,
            )

        if self.__chatCommandPrefixRegEx.match(chatMessage.text):
            await self.__processChatCommand(
                chatMessage = chatMessage,
            )

        await self.__processAnivCopyMessageTimeout(
            chatMessage = chatMessage,
        )

    async def onNewChatDataBundle(
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
            self.__timber.log('TwitchChatHandler', f'Received a data bundle that has no event: ({user=}) ({twitchChannelId=}) ({dataBundle=})')
            return

        chatterUserId = event.chatterUserId
        chatterUserLogin = event.chatterUserLogin
        chatterUserName = event.chatterUserName
        chatMessage = event.chatMessage

        if (event.isAnonymous is True or event.isChatterAnonymous is True) and (not utils.isValidStr(chatterUserId) and not utils.isValidStr(chatterUserLogin) and not utils.isValidStr(chatterUserName)):
            chatterUserId = await self.__officialTwitchAccountUserIdProvider.getTwitchAnonymousGifterUserId()

            twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                twitchChannelId = twitchChannelId,
            )

            chatterUserName = await self.__userIdsRepository.fetchUserName(
                userId = chatterUserId,
                twitchAccessToken = twitchAccessToken,
            )

            chatterUserLogin = chatterUserName

        if not utils.isValidStr(chatterUserId) or not utils.isValidStr(chatterUserLogin) or not utils.isValidStr(chatterUserName) or chatMessage is None:
            self.__timber.log('TwitchChatHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({twitchChannelId=}) ({dataBundle=}) ({chatterUserId=}) ({chatterUserLogin=}) ({chatterUserName=}) ({chatMessage=})')
            return

        messageFragments = await self.__twitchLocalModelsMapper.mapChatMessageFragments(chatMessage.fragments)
        textWithoutCheers = await self.__purgeChatMessageOfCheers(messageFragments)
        cheerMetadata = await self.__twitchLocalModelsMapper.mapCheerMetadata(event.cheer)
        watchStreak = await self.__twitchLocalModelsMapper.mapWatchStreak(event.watchStreak)

        if event.customPowerUp is not None or event.customPowerUpData is not None:
            # just including this for testing/debug purposes for the time being
            self.__timber.log('TwitchChatHandler', f'This event has custom power up data ({user=}) ({twitchChannelId=}) ({dataBundle=})')

        chatMessage = TwitchChatMessage(
            messageFragments = messageFragments,
            chatterUserId = chatterUserId,
            chatterUserLogin = chatterUserLogin,
            chatterUserName = chatterUserName,
            eventId = dataBundle.metadata.messageId,
            sourceMessageId = event.sourceMessageId,
            text = chatMessage.text,
            textWithoutCheers = textWithoutCheers,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = event.messageId,
            cheerMetadata = cheerMetadata,
            watchStreak = watchStreak,
            twitchUser = user,
        )

        await self.onNewChat(
            chatMessage = chatMessage,
        )

    async def __processAnivCopyMessageTimeout(
        self,
        chatMessage: TwitchChatMessage,
    ):
        if self.__mostRecentAnivMessageTimeoutHelper is None:
            return

        cheer = chatMessage.cheerMetadata
        if cheer is not None and cheer.bits > 0:
            return

        await self.__mostRecentAnivMessageTimeoutHelper.checkMessageAndMaybeTimeout(
            chatterMessage = chatMessage.text,
            chatterUserId = chatMessage.chatterUserId,
            chatterUserName = chatMessage.chatterUserName,
            twitchChannelId = chatMessage.twitchChannelId,
            user = chatMessage.twitchUser,
        )

    async def __processChatActions(
        self,
        mostRecentChat: MostRecentChat | None,
        chatMessage: TwitchChatMessage,
    ):
        for index, chatAction in enumerate(self.__chatActions):
            try:
                result = await chatAction.handleChatAction(
                    mostRecentChat = mostRecentChat,
                    chatMessage = chatMessage,
                )

                match result:
                    case ChatActionResult.CONSUMED: return
                    case ChatActionResult.HANDLED: pass
                    case ChatActionResult.IGNORED: pass
            except Exception as e:
                self.__timber.log('TwitchChatHandler', f'Encountered an unexpected error while handling a chat action ({index=}) ({chatAction=}) ({chatMessage=}) ({mostRecentChat=})', e, traceback.format_exc())

    async def __processChatCommand(self, chatMessage: TwitchChatMessage):
        if not utils.isValidStr(chatMessage.text):
            # this probably shouldn't be necessary here, but let's just be safe
            return

        for index, chatCommand in enumerate(self.__chatCommands):
            try:
                for commandPattern in chatCommand.commandPatterns:
                    if not commandPattern.match(chatMessage.text):
                        continue

                    result = await chatCommand.handleChatCommand(
                        chatMessage = chatMessage,
                    )

                    match result:
                        case ChatCommandResult.CONSUMED: return
                        case ChatCommandResult.HANDLED: break
                        case ChatCommandResult.IGNORED: pass
            except Exception as e:
                self.__timber.log('TwitchChatHandler', f'Encountered an unexpected error while handling a chat command ({index=}) ({chatCommand=}) ({chatMessage=})', e, traceback.format_exc())

    async def __processCheerAction(self, chatMessage: TwitchChatMessage):
        if self.__cheerActionHelper is None:
            return
        elif not chatMessage.twitchUser.areCheerActionsEnabled:
            return

        cheer = chatMessage.cheerMetadata
        if cheer is None or cheer.bits <= 0:
            return

        self.__cheerActionHelper.submitCheer(CheerActionHelperInterface.CheerInfo(
            bits = cheer.bits,
            cheerUserId = chatMessage.chatterUserId,
            cheerUserLogin = chatMessage.chatterUserLogin,
            cheerUserName = chatMessage.chatterUserName,
            message = chatMessage.textWithoutCheers,
            twitchChannelId = chatMessage.twitchChannelId,
            twitchChatMessageId = chatMessage.twitchChatMessageId,
            twitchUser = chatMessage.twitchUser,
        ))

    async def __processSuperTriviaEvent(self, chatMessage: TwitchChatMessage):
        user = chatMessage.twitchUser

        if not user.isSuperTriviaGameEnabled:
            return
        elif self.__triviaGameBuilder is None or self.__triviaGameMachine is None:
            return

        cheer = chatMessage.cheerMetadata
        if cheer is None or cheer.bits <= 0:
            return

        superTriviaCheerTriggerAmount = user.superTriviaCheerTriggerAmount
        superTriviaCheerTriggerMaximum = user.superTriviaCheerTriggerMaximum

        if superTriviaCheerTriggerAmount is None or superTriviaCheerTriggerAmount < 1 or cheer.bits < superTriviaCheerTriggerAmount:
            return

        numberOfGames = int(math.floor(float(cheer.bits) / float(superTriviaCheerTriggerAmount)))

        if numberOfGames < 1:
            return
        elif superTriviaCheerTriggerMaximum is not None and numberOfGames > superTriviaCheerTriggerMaximum:
            numberOfGames = int(min(numberOfGames, superTriviaCheerTriggerMaximum))

        action = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
            numberOfGames = numberOfGames,
        )

        if action is not None:
            self.__triviaGameMachine.submitAction(action)

    async def __purgeChatMessageOfCheers(
        self,
        messageFragments: Collection[TwitchChatMessageFragment] | None,
    ) -> str:
        if messageFragments is None:
            return ''

        chunks: list[str] = list()

        for messageFragment in messageFragments:
            if messageFragment.fragmentType is not TwitchChatMessageFragmentType.CHEERMOTE:
                chunks.append(messageFragment.text)

        purgedMessage = ' '.join(chunks)
        return utils.cleanStr(purgedMessage)
