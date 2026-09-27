import locale
import re
import traceback
from dataclasses import dataclass
from typing import Collection, Final, Pattern

from frozenlist import FrozenList

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc.simpleDateTime import SimpleDateTime
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..twitch.userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface
from ..voicemail.helpers.voicemailHelperInterface import VoicemailHelperInterface
from ..voicemail.models.preparedVoicemailData import PreparedVoicemailData
from ..voicemail.settings.voicemailSettingsRepositoryInterface import VoicemailSettingsRepositoryInterface


class VoicemailsChatCommand(AbsChatCommand):

    @dataclass(frozen = True, slots = True)
    class Arguments:
        chatterUserId: str
        chatterUserLogin: str
        chatterUserName: str

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
        voicemailHelper: VoicemailHelperInterface,
        voicemailSettingsRepository: VoicemailSettingsRepositoryInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchUserIdsHelper, TwitchUserIdsHelperInterface):
            raise TypeError(f'twitchUserIdsHelper argument is malformed: \"{twitchUserIdsHelper}\"')
        elif not isinstance(voicemailHelper, VoicemailHelperInterface):
            raise TypeError(f'voicemailHelper argument is malformed: \"{voicemailHelper}\"')
        elif not isinstance(voicemailSettingsRepository, VoicemailSettingsRepositoryInterface):
            raise TypeError(f'voicemailSettingsRepository argument is malformed: \"{voicemailSettingsRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper
        self.__voicemailHelper: Final[VoicemailHelperInterface] = voicemailHelper
        self.__voicemailSettingsRepository: Final[VoicemailSettingsRepositoryInterface] = voicemailSettingsRepository

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!voicemails?\b', re.IGNORECASE),
        })

        self.__argumentsPattern: Final[Pattern] = re.compile(r'^\s*!\w+\s+@?(\w+)', re.IGNORECASE)

    @property
    def commandName(self) -> str:
        return 'VoicemailsChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not await self.__voicemailSettingsRepository.isEnabled():
            return ChatCommandResult.IGNORED
        elif not chatMessage.twitchUser.isTtsEnabled:
            return ChatCommandResult.IGNORED

        arguments = await self.__parseArguments(
            chatMessage = chatMessage,
        )

        if arguments is None:
            self.__twitchChatMessenger.send(
                text = f'⚠ Invalid arguments! Example use: !voicemails @{chatMessage.chatterUserLogin}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Invalid arguments ({arguments=}) ({chatMessage=})')
            return ChatCommandResult.CONSUMED

        voicemails = await self.__voicemailHelper.getAllForTargetUser(
            targetUserId = arguments.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        self.__twitchChatMessenger.send(
            text = await self.__toString(
                arguments = arguments,
                voicemails = voicemails,
                chatMessage = chatMessage,
            ),
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Consumed ({voicemails=}) ({arguments=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __parseArguments(self, chatMessage: TwitchChatMessage) -> Arguments | None:
        argumentsMatch = self.__argumentsPattern.match(chatMessage.text)

        if argumentsMatch is None:
            return VoicemailsChatCommand.Arguments(
                chatterUserId = chatMessage.chatterUserId,
                chatterUserLogin = chatMessage.chatterUserLogin,
                chatterUserName = chatMessage.chatterUserName,
            )

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

        return VoicemailsChatCommand.Arguments(
            chatterUserId = chatterUserData.userId,
            chatterUserLogin = chatterUserData.userLogin,
            chatterUserName = chatterUserData.userName,
        )

    async def __toString(
        self,
        arguments: Arguments,
        voicemails: FrozenList[PreparedVoicemailData],
        chatMessage: TwitchChatMessage,
    ) -> str:
        voicemailsSize = len(voicemails)
        voicemailsSizeStr = locale.format_string("%d", voicemailsSize, grouping = True)

        voicemailsPlurality: str
        if voicemailsSize == 1:
            voicemailsPlurality = 'voicemail'
        else:
            voicemailsPlurality = 'voicemails'

        maximumVoicemails = await self.__voicemailSettingsRepository.getMaximumPerTargetUser()
        maximumVoicemailsStr = locale.format_string("%d", maximumVoicemails, grouping = True)

        if voicemailsSize == 0:
            return f'ⓘ @{arguments.chatterUserLogin} has {voicemailsSizeStr} {voicemailsPlurality} (maximum voicemail inbox size is {maximumVoicemailsStr})'

        mostRecentVoicemail = voicemails[voicemailsSize - 1]
        mostRecentVoicemailUserName = mostRecentVoicemail.originatingUserName
        mostRecentVoicemailDateTime = SimpleDateTime(mostRecentVoicemail.createdDateTime).getDateAndTimeStr()

        commandTutorialMessage: str
        if arguments.chatterUserId == chatMessage.chatterUserId:
            commandTutorialMessage = ''
        else:
            commandTutorialMessage = ' You can play voicemails with the !playvoicemail command!'

        return f'ⓘ @{arguments.chatterUserLogin} has {voicemailsSizeStr} {voicemailsPlurality} (most recent voicemail is from @{mostRecentVoicemailUserName}, {mostRecentVoicemailDateTime}).{commandTutorialMessage} (maximum voicemail inbox size is {maximumVoicemailsStr})'
