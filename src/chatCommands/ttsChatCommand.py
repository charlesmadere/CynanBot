import random
import re
from typing import Final, Pattern

from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..timber.timberInterface import TimberInterface
from ..tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from ..tts.models.ttsEvent import TtsEvent
from ..tts.models.ttsProvider import TtsProvider
from ..tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.tts.ttsBoosterPack import TtsBoosterPack
from ..users.userInterface import UserInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class TtsChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        ttsJsonMapper: TtsJsonMapperInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__ttsJsonMapper: Final[TtsJsonMapperInterface] = ttsJsonMapper
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

        self.__ttsProviderRegEx: Final[Pattern] = re.compile(r'^--(\w+)$', re.IGNORECASE)

    async def __displayTtsCheerAmounts(self, ctx: TwitchContext, user: UserInterface):
        cheerAmountStrings = await self.__getTtsCheerAmountStrings(user)

        if len(cheerAmountStrings) == 0:
            self.__twitchChatMessenger.send(
                text = f'ⓘ TTS cheers have not been set up for this channel',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
        else:
            cheerAmountString = ', '.join(cheerAmountStrings)

            self.__twitchChatMessenger.send(
                text = f'ⓘ TTS cheer information — {cheerAmountString}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

    async def __getTtsCheerAmountStrings(self, user: UserInterface) -> list[str]:
        ttsBoosterPacks = user.ttsBoosterPacks
        strings: list[str] = list()

        if ttsBoosterPacks is None or len(ttsBoosterPacks) == 0:
            return strings

        for ttsBoosterPack in ttsBoosterPacks:
            if not ttsBoosterPack.isEnabled:
                continue

            bitsString: str

            if ttsBoosterPack.cheerAmount == 1:
                bitsString = 'bit'
            else:
                bitsString = 'bits'

            string = f'{ttsBoosterPack.cheerAmountStr} {bitsString} or more for {ttsBoosterPack.ttsProvider.humanName}'
            strings.append(string)

        return strings

    async def __getTtsProviderStrings(self) -> list[str]:
        strings: list[str] = list()

        for ttsProvider in TtsProvider:
            strings.append(await self.__ttsJsonMapper.asyncSerializeProvider(ttsProvider))

        strings.sort(key = lambda ttsProvider: ttsProvider.casefold())
        return strings

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isTtsEnabled:
            return

        userId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            await self.__displayTtsCheerAmounts(ctx, user)
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            await self.__displayTtsCheerAmounts(ctx, user)
            return

        message = ' '.join(splits[1:])
        if not utils.isValidStr(message):
            await self.__displayTtsCheerAmounts(ctx, user)
            return

        ttsProvider = user.defaultTtsProvider
        ttsProviderMatch = self.__ttsProviderRegEx.fullmatch(message.split()[0])

        if ttsProviderMatch is not None and utils.isValidStr(ttsProviderMatch.group(1)) and len(splits) >= 3:
            try:
                ttsProvider = await self.__ttsJsonMapper.asyncRequireProvider(ttsProviderMatch.group(1))
                message = ' '.join(splits[2:])
            except ValueError:
                ttsProviderStrings = await self.__getTtsProviderStrings()
                ttsProviderString = ', '.join(ttsProviderStrings)

                self.__twitchChatMessenger.send(
                    text = f'⚠ TTS provider argument is malformed! Available TTS provider(s): {ttsProviderString}. Example: !tts --{random.choice(ttsProviderStrings)} Hello, World!',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )

                return

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.handle,
            twitchChannelId = userId,
            ttsEvent = TtsEvent(
                message = message,
                twitchChannel = user.handle,
                twitchChannelId = userId,
                userId = ctx.getAuthorId(),
                userName = ctx.getAuthorName(),
                donation = None,
                provider = ttsProvider,
                providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
                raidInfo = None,
            ),
        ))

        self.__twitchChatMessenger.send(
            text = f'ⓘ Submitted TTS message using {ttsProvider.humanName}…',
            twitchChannelId = await ctx.getTwitchChannelId(),
            replyMessageId = await ctx.getMessageId(),
        )

        self.__timber.log('TtsChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
