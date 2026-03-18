import math
import re
import traceback
from typing import Any, Collection, Final, Pattern

from frozenlist import FrozenList

from ..absTwitchChatHandler import AbsTwitchChatHandler
from ..api.models.twitchChatMessageFragment import TwitchChatMessageFragment as ApiTwitchChatMessageFragment
from ..api.models.twitchChatMessageFragmentCheermote import \
    TwitchChatMessageFragmentCheermote as ApiTwitchChatMessageFragmentCheermote
from ..api.models.twitchChatMessageFragmentEmote import \
    TwitchChatMessageFragmentEmote as ApiTwitchChatMessageFragmentEmote
from ..api.models.twitchChatMessageFragmentMention import \
    TwitchChatMessageFragmentMention as ApiTwitchChatMessageFragmentMention
from ..api.models.twitchChatMessageFragmentType import TwitchChatMessageFragmentType as ApiTwitchChatMessageFragmentType
from ..api.models.twitchCheerMetadata import TwitchCheerMetadata as ApiTwitchCheerMetadata
from ..api.models.twitchEmoteImageFormat import TwitchEmoteImageFormat as ApiTwitchEmoteImageFormat
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..localModels.twitchChatMessage import TwitchChatMessage
from ..localModels.twitchChatMessageFragment import TwitchChatMessageFragment
from ..localModels.twitchChatMessageFragmentCheermote import TwitchChatMessageFragmentCheermote
from ..localModels.twitchChatMessageFragmentEmote import TwitchChatMessageFragmentEmote
from ..localModels.twitchChatMessageFragmentMention import TwitchChatMessageFragmentMention
from ..localModels.twitchChatMessageFragmentType import TwitchChatMessageFragmentType
from ..localModels.twitchCheerMetadata import TwitchCheerMetadata
from ..localModels.twitchEmoteImageFormat import TwitchEmoteImageFormat
from ...aniv.helpers.mostRecentAnivMessageTimeoutHelperInterface import MostRecentAnivMessageTimeoutHelperInterface
from ...chatActions.absChatAction2 import AbsChatAction2
from ...chatActions.anivCheckChatAction import AnivCheckChatAction
from ...chatActions.chatActionResult import ChatActionResult
from ...chatActions.saveMostRecentAnivMessageChatAction import SaveMostRecentAnivMessageChatAction
from ...chatCommands.absChatCommand2 import AbsChatCommand2
from ...chatCommands.chatCommandResult import ChatCommandResult
from ...chatLogger.chatLoggerInterface import ChatLoggerInterface
from ...cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from ...misc import utils as utils
from ...mostRecentChat.mostRecentChat import MostRecentChat
from ...mostRecentChat.mostRecentChatsRepositoryInterface import MostRecentChatsRepositoryInterface
from ...soundPlayerManager.soundAlert import SoundAlert
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from ...trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ...tts.models.ttsCheerDonation import TtsCheerDonation
from ...tts.models.ttsEvent import TtsEvent
from ...tts.models.ttsProvider import TtsProvider
from ...tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ...users.userInterface import UserInterface


class TwitchChatHandler(AbsTwitchChatHandler):

    def __init__(
        self,
        anivCheckChatAction: AnivCheckChatAction | None,
        chatLogger: ChatLoggerInterface,
        cheerActionHelper: CheerActionHelperInterface | None,
        mostRecentAnivMessageTimeoutHelper: MostRecentAnivMessageTimeoutHelperInterface | None,
        mostRecentChatsRepository: MostRecentChatsRepositoryInterface,
        saveMostRecentAnivMessageChatAction: SaveMostRecentAnivMessageChatAction | None,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface | None,
        triviaGameMachine: TriviaGameMachineInterface | None,
        chatActions: Collection[AbsChatCommand2 | Any | None] | None,
        chatCommands: Collection[AbsChatCommand2 | Any | None] | None,
    ):
        if anivCheckChatAction is not None and not isinstance(anivCheckChatAction, AnivCheckChatAction):
            raise TypeError(f'anivCheckChatAction argument is malformed: \"{anivCheckChatAction}\"')
        elif not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif cheerActionHelper is not None and not isinstance(cheerActionHelper, CheerActionHelperInterface):
            raise TypeError(f'cheerActionHelper argument is malformed: \"{cheerActionHelper}\"')
        elif mostRecentAnivMessageTimeoutHelper is not None and not isinstance(mostRecentAnivMessageTimeoutHelper, MostRecentAnivMessageTimeoutHelperInterface):
            raise TypeError(f'mostRecentAnivMessageTimeoutHelper argument is malformed: \"{mostRecentAnivMessageTimeoutHelper}\"')
        elif not isinstance(mostRecentChatsRepository, MostRecentChatsRepositoryInterface):
            raise TypeError(f'mostRecentChatsRepository argument is malformed: \"{mostRecentChatsRepository}\"')
        elif saveMostRecentAnivMessageChatAction is not None and not isinstance(saveMostRecentAnivMessageChatAction, SaveMostRecentAnivMessageChatAction):
            raise TypeError(f'saveMostRecentAnivMessageChatAction argument is malformed: \"{saveMostRecentAnivMessageChatAction}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif triviaGameBuilder is not None and not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise TypeError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif triviaGameMachine is not None and not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif chatActions is not None and not isinstance(chatActions, Collection):
            raise TypeError(f'chatActions argument is malformed: \"{chatActions}\"')
        elif chatCommands is not None and not isinstance(chatCommands, Collection):
            raise TypeError(f'chatCommands argument is malformed: \"{chatCommands}\"')

        self.__anivCheckChatAction: Final[AbsChatAction2 | None] = anivCheckChatAction
        self.__chatLogger: Final[ChatLoggerInterface] = chatLogger
        self.__cheerActionHelper: Final[CheerActionHelperInterface | None] = cheerActionHelper
        self.__mostRecentAnivMessageTimeoutHelper: Final[MostRecentAnivMessageTimeoutHelperInterface | None] = mostRecentAnivMessageTimeoutHelper
        self.__mostRecentChatsRepository: Final[MostRecentChatsRepositoryInterface] = mostRecentChatsRepository
        self.__saveMostRecentAnivMessageChatAction: Final[AbsChatAction2 | None] = saveMostRecentAnivMessageChatAction
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameBuilder: Final[TriviaGameBuilderInterface | None] = triviaGameBuilder
        self.__triviaGameMachine: Final[TriviaGameMachineInterface | None] = triviaGameMachine

        self.__chatCommandPrefixRegEx: Final[Pattern] = re.compile(r'^\s*!\w+\.*', re.IGNORECASE)

        self.__chatActions: Final[Collection[AbsChatAction2]] = self.__buildChatActionsCollection(chatActions)
        self.__chatCommands: Final[Collection[AbsChatCommand2]] = self.__buildChatCommandsCollection(chatCommands)

    def __buildChatActionsCollection(
        self,
        chatActions: Collection[AbsChatAction2 | Any | None] | None,
    ) -> Collection[AbsChatAction2]:
        if chatActions is None:
            emptyChatActions: FrozenList[AbsChatAction2] = FrozenList()
            emptyChatActions.freeze()
            return emptyChatActions

        frozenChatActions: FrozenList[AbsChatAction2 | Any | None] = FrozenList(chatActions)
        frozenChatActions.freeze()

        validChatActions: FrozenList[AbsChatAction2] = FrozenList()

        for index, chatAction in enumerate(frozenChatActions):
            if chatAction is None:
                continue
            elif isinstance(chatAction, AbsChatAction2):
                validChatActions.append(chatAction)
            else:
                exception = TypeError(f'Encountered an invalid AbsChatAction2 instance ({index=}) ({chatAction=}) ({frozenChatActions=})')
                self.__timber.log('TwitchChatHandler', f'Encountered an invalid AbsChatAction2 instance ({index=}) ({chatAction=}) ({frozenChatActions=})', exception, traceback.format_exc())
                raise exception

        validChatActions.freeze()
        return validChatActions

    def __buildChatCommandsCollection(
        self,
        chatCommands: Collection[AbsChatCommand2 | Any | None] | None,
    ) -> Collection[AbsChatCommand2]:
        if chatCommands is None:
            return frozenset()

        frozenChatCommands: FrozenList[AbsChatCommand2 | Any | None] = FrozenList(chatCommands)
        frozenChatCommands.freeze()

        validChatCommands: set[AbsChatCommand2] = set()

        for index, chatCommand in enumerate(frozenChatCommands):
            if chatCommand is None:
                continue
            elif isinstance(chatCommand, AbsChatCommand2):
                validChatCommands.add(chatCommand)
            else:
                exception = TypeError(f'Encountered an invalid AbsChatCommand2 instance ({index=}) ({chatCommand=}) ({frozenChatCommands=})')
                self.__timber.log('TwitchChatHandler', f'Encountered an invalid AbsChatCommand2 instance ({index=}) ({chatCommand=}) ({frozenChatCommands=})', exception, traceback.format_exc())
                raise exception

        return frozenset(validChatCommands)

    async def __logChat(self, chatMessage: TwitchChatMessage):
        bits: int | None = None

        if chatMessage.cheerMetadata is not None and chatMessage.cheerMetadata.bits > 0:
            bits = chatMessage.cheerMetadata.bits

        self.__chatLogger.logCheer(
            bits = bits,
            cheerUserId = chatMessage.chatterUserId,
            cheerUserLogin = chatMessage.chatterUserLogin,
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

        if chatMessage.twitchUser.isChatLoggingEnabled:
            await self.__logChat(chatMessage)

        if chatMessage.twitchUser.areCheerActionsEnabled:
            await self.__processCheerAction(chatMessage)

        if chatMessage.twitchUser.isSuperTriviaGameEnabled:
            await self.__processSuperTriviaEvent(chatMessage)

        if chatMessage.twitchUser.isTtsEnabled:
            await self.__processTtsEvent(chatMessage)

        if self.__chatCommandPrefixRegEx.match(chatMessage.text):
            await self.__processChatCommand(chatMessage)

        await self.__processAnivChatActions(
            mostRecentChat = mostRecentChat,
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

        eventId = dataBundle.metadata.messageId
        chatterUserId = event.chatterUserId
        chatterUserLogin = event.chatterUserLogin
        chatterUserName = event.chatterUserName
        chatMessage = event.chatMessage

        if not utils.isValidStr(eventId) or not utils.isValidStr(chatterUserId) or not utils.isValidStr(chatterUserLogin) or not utils.isValidStr(chatterUserName) or chatMessage is None:
            self.__timber.log('TwitchChatHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({twitchChannelId=}) ({dataBundle=}) ({chatterUserId=}) ({chatterUserLogin=}) ({chatterUserName=}) ({chatMessage=})')
            return

        messageFragments = await self.__mapApiMessageFragments(chatMessage.fragments)
        cheer = await self.__mapApiCheerMetadata(event.cheer)

        chatMessage = TwitchChatMessage(
            messageFragments = messageFragments,
            chatterUserId = chatterUserId,
            chatterUserLogin = chatterUserLogin,
            chatterUserName = chatterUserName,
            eventId = eventId,
            sourceMessageId = event.sourceMessageId,
            text = chatMessage.text,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = event.messageId,
            cheerMetadata = cheer,
            twitchUser = user,
        )

        await self.onNewChat(
            chatMessage = chatMessage,
        )

    async def __processAnivChatActions(
        self,
        mostRecentChat: MostRecentChat | None,
        chatMessage: TwitchChatMessage,
    ):
        if self.__saveMostRecentAnivMessageChatAction is not None:
            await self.__saveMostRecentAnivMessageChatAction.handleChatAction(
                mostRecentChat = mostRecentChat,
                chatMessage = chatMessage,
            )

            if self.__mostRecentAnivMessageTimeoutHelper is not None:
                await self.__mostRecentAnivMessageTimeoutHelper.checkMessageAndMaybeTimeout(
                    chatterMessage = chatMessage.text,
                    chatterUserId = chatMessage.chatterUserId,
                    chatterUserName = chatMessage.chatterUserName,
                    twitchChannelId = chatMessage.twitchChannelId,
                    user = chatMessage.twitchUser,
                )

        if self.__anivCheckChatAction is not None:
            await self.__anivCheckChatAction.handleChatAction(
                mostRecentChat = mostRecentChat,
                chatMessage = chatMessage,
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
            # this shouldn't be necessary here, but let's just be safe
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

    async def __processCheerAction(self, chatMessage: TwitchChatMessage) -> bool:
        user = chatMessage.twitchUser

        if not user.areCheerActionsEnabled:
            return False
        elif self.__cheerActionHelper is None:
            return False

        cheer = chatMessage.cheerMetadata
        if cheer is None or cheer.bits < 1:
            return False

        messageWithoutCheerText = await self.__purgeChatMessageOfCheers(chatMessage)
        self.__timber.log('TwitchChatHandler', f'Purged message of cheers ({messageWithoutCheerText=}) ({chatMessage=})')

        return await self.__cheerActionHelper.handleCheerAction(
            bits = cheer.bits,
            cheerUserId = chatMessage.chatterUserId,
            cheerUserName = chatMessage.chatterUserLogin,
            message = chatMessage.text,
            twitchChannelId = chatMessage.twitchChannelId,
            twitchChatMessageId = chatMessage.twitchChatMessageId,
            user = user,
        )

    async def __processSuperTriviaEvent(self, chatMessage: TwitchChatMessage):
        user = chatMessage.twitchUser

        if not user.isSuperTriviaGameEnabled:
            return
        elif self.__triviaGameBuilder is None or self.__triviaGameMachine is None:
            return

        cheer = chatMessage.cheerMetadata
        if cheer is None or cheer.bits < 1:
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

    async def __processTtsEvent(self, chatMessage: TwitchChatMessage):
        user = chatMessage.twitchUser
        if not user.isTtsEnabled:
            return

        cheer = chatMessage.cheerMetadata
        if cheer is None or cheer.bits < 1:
            return

        provider: TtsProvider | None = None
        ttsBoosterPacks = user.ttsBoosterPacks

        if ttsBoosterPacks is None or len(ttsBoosterPacks) == 0:
            return

        for ttsBoosterPack in ttsBoosterPacks:
            if ttsBoosterPack.isEnabled and cheer.bits >= ttsBoosterPack.cheerAmount:
                provider = ttsBoosterPack.ttsProvider
                break

        if provider is None:
            return

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.CHEER,
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
            ttsEvent = TtsEvent(
                message = chatMessage.text,
                twitchChannel = chatMessage.twitchChannel,
                twitchChannelId = chatMessage.twitchChannelId,
                userId = chatMessage.chatterUserId,
                userName = chatMessage.chatterUserLogin,
                donation = TtsCheerDonation(
                    bits = cheer.bits,
                ),
                provider = provider,
                providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
                raidInfo = None,
            ),
        ))

    async def __purgeChatMessageOfCheers(self, message: TwitchChatMessage) -> str:
        chunks: list[str] = list()

        for messageFragment in message.messageFragments:
            if messageFragment.fragmentType is not TwitchChatMessageFragmentType.CHEERMOTE:
                chunks.append(messageFragment.text)

        purgedMessage = ' '.join(chunks)
        return utils.cleanStr(purgedMessage)

    async def __mapApiCheerMetadata(
        self,
        apiCheer: ApiTwitchCheerMetadata | None,
    ) -> TwitchCheerMetadata | None:
        if apiCheer is None or apiCheer.bits < 1:
            return None

        return TwitchCheerMetadata(
            bits = apiCheer.bits,
        )

    async def __mapApiMessageFragments(
        self,
        apiMessageFragments: Collection[ApiTwitchChatMessageFragment],
    ) -> FrozenList[TwitchChatMessageFragment]:
        messageFragments: FrozenList[TwitchChatMessageFragment] = FrozenList()

        for apiMessageFragment in apiMessageFragments:
            messageFragment = await self.__mapApiMessageFragment(apiMessageFragment)
            messageFragments.append(messageFragment)

        messageFragments.freeze()
        return messageFragments

    async def __mapApiMessageFragment(
        self,
        apiMessageFragment: ApiTwitchChatMessageFragment,
    ) -> TwitchChatMessageFragment:
        cheermote = await self.__mapApiMessageFragmentCheermote(apiMessageFragment.cheermote)
        emote = await self.__mapApiMessageFragmentEmote(apiMessageFragment.emote)
        mention = await self.__mapApiMessageFragmentMention(apiMessageFragment.mention)
        fragmentType = await self.__mapApiMessageFragmentType(apiMessageFragment.fragmentType)

        return TwitchChatMessageFragment(
            text = apiMessageFragment.text,
            cheermote = cheermote,
            emote = emote,
            mention = mention,
            fragmentType = fragmentType,
        )

    async def __mapApiMessageFragmentCheermote(
        self,
        apiCheermote: ApiTwitchChatMessageFragmentCheermote | None,
    ) -> TwitchChatMessageFragmentCheermote | None:
        if apiCheermote is None:
            return None

        return TwitchChatMessageFragmentCheermote(
            bits = apiCheermote.bits,
            tier = apiCheermote.tier,
            prefix = apiCheermote.prefix,
        )

    async def __mapApiMessageFragmentEmote(
        self,
        apiEmote: ApiTwitchChatMessageFragmentEmote | None,
    ) -> TwitchChatMessageFragmentEmote | None:
        if apiEmote is None:
            return None

        imageFormats: set[TwitchEmoteImageFormat] = set()

        for apiImageFormat in apiEmote.imageFormats:
            imageFormat = await self.__mapApiEmoteImageFormat(apiImageFormat)
            imageFormats.add(imageFormat)

        return TwitchChatMessageFragmentEmote(
            imageFormats = frozenset(imageFormats),
            emoteId = apiEmote.emoteId,
            emoteSetId = apiEmote.emoteSetId,
            ownerId = apiEmote.ownerId,
        )

    async def __mapApiEmoteImageFormat(
        self,
        apiImageFormat: ApiTwitchEmoteImageFormat,
    ) -> TwitchEmoteImageFormat:
        match apiImageFormat:
            case ApiTwitchEmoteImageFormat.ANIMATED: return TwitchEmoteImageFormat.ANIMATED
            case ApiTwitchEmoteImageFormat.STATIC: return TwitchEmoteImageFormat.STATIC
            case _: raise ValueError(f'Encountered unknown ApiTwitchEmoteImageFormat: \"{apiImageFormat}\"')

    async def __mapApiMessageFragmentMention(
        self,
        apiMention: ApiTwitchChatMessageFragmentMention | None,
    ) -> TwitchChatMessageFragmentMention | None:
        if apiMention is None:
            return None

        return TwitchChatMessageFragmentMention(
            userId = apiMention.userId,
            userLogin = apiMention.userLogin,
            userName = apiMention.userName,
        )

    async def __mapApiMessageFragmentType(
        self,
        apiFragmentType: ApiTwitchChatMessageFragmentType,
    ) -> TwitchChatMessageFragmentType:
        match apiFragmentType:
            case ApiTwitchChatMessageFragmentType.CHEERMOTE: return TwitchChatMessageFragmentType.CHEERMOTE
            case ApiTwitchChatMessageFragmentType.EMOTE: return TwitchChatMessageFragmentType.EMOTE
            case ApiTwitchChatMessageFragmentType.MENTION: return TwitchChatMessageFragmentType.MENTION
            case ApiTwitchChatMessageFragmentType.TEXT: return TwitchChatMessageFragmentType.TEXT
            case _: raise ValueError(f'Encountered unknown ApiTwitchChatMessageFragmentType: \"{apiFragmentType}\"')
