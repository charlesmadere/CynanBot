import random
import re
from typing import Pattern

from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..timber.timberInterface import TimberInterface
from ..tts.ttsEvent import TtsEvent
from ..tts.ttsJsonMapperInterface import TtsJsonMapperInterface
from ..tts.ttsProvider import TtsProvider
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class TtsChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        ttsJsonMapper: TtsJsonMapperInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__ttsJsonMapper: TtsJsonMapperInterface = ttsJsonMapper
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

        self.__ttsProviderRegEx: Pattern = re.compile(r'^--(\w+)$', re.IGNORECASE)

    async def __getTtsProviderStrings(self) -> list[str]:
        strings: list[str] = list()

        for ttsProvider in list(TtsProvider):
            strings.append(await self.__ttsJsonMapper.serializeProvider(ttsProvider))

        strings.sort(key = lambda ttsProvider: ttsProvider.casefold())
        return strings

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        userId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('TtsCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return
        elif not user.isTtsEnabled():
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            await self.__twitchUtils.safeSend(ctx, '⚠ Missing a message argument! Example: !tts Hello, World!')
            return

        message = ' '.join(splits[1:])
        if not utils.isValidStr(message):
            await self.__twitchUtils.safeSend(ctx, '⚠ Missing a message argument! Example: !tts Hello, World!')
            return

        ttsProvider: TtsProvider = TtsProvider.DEC_TALK
        ttsProviderMatch = self.__ttsProviderRegEx.fullmatch(message.split()[0])

        if ttsProviderMatch is not None:
            try:
                ttsProvider = await self.__ttsJsonMapper.requireProvider(ttsProviderMatch.group(1))
            except ValueError:
                ttsProviderStrings = await self.__getTtsProviderStrings()
                ttsProviderString = ', '.join(ttsProviderStrings)
                await self.__twitchUtils.safeSend(ctx, f'⚠ TTS provider argument is malformed! Available TTS provider(s): {ttsProviderString}. Example: !tts --{random.choice(ttsProviderStrings)} Hello, World!')
                return

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.getHandle(),
            twitchChannelId = userId,
            ttsEvent = TtsEvent(
                message = message,
                twitchChannel = user.getHandle(),
                twitchChannelId = userId,
                userId = ctx.getAuthorId(),
                userName = ctx.getAuthorName(),
                donation = None,
                provider = ttsProvider,
                raidInfo = None
            )
        ))

        self.__timber.log('TtsCommand', f'Handled !tts command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
