import locale
import traceback
from dataclasses import dataclass
from typing import Final

from frozenlist import FrozenList

from .absChatCommand import AbsChatCommand
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..misc.simpleDateTime import SimpleDateTime
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..users.exceptions import NoSuchUserException
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface
from ..voicemail.helpers.voicemailHelperInterface import VoicemailHelperInterface
from ..voicemail.models.preparedVoicemailData import PreparedVoicemailData
from ..voicemail.settings.voicemailSettingsRepositoryInterface import VoicemailSettingsRepositoryInterface


class VoicemailsChatCommand(AbsChatCommand):

    @dataclass(frozen = True)
    class VoicemailLookupData:
        voicemails: FrozenList[PreparedVoicemailData]
        chatterUserId: str
        chatterUserName: str

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        voicemailHelper: VoicemailHelperInterface,
        voicemailSettingsRepository: VoicemailSettingsRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(voicemailHelper, VoicemailHelperInterface):
            raise TypeError(f'voicemailHelper argument is malformed: \"{voicemailHelper}\"')
        elif not isinstance(voicemailSettingsRepository, VoicemailSettingsRepositoryInterface):
            raise TypeError(f'voicemailSettingsRepository argument is malformed: \"{voicemailSettingsRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository
        self.__voicemailHelper: Final[VoicemailHelperInterface] = voicemailHelper
        self.__voicemailSettingsRepository: Final[VoicemailSettingsRepositoryInterface] = voicemailSettingsRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        if not await self.__voicemailSettingsRepository.isEnabled():
            return

        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        if not user.isVoicemailEnabled or not user.isTtsEnabled:
            return

        messageContent = utils.cleanStr(ctx.getMessageContent())

        try:
            voicemailLookupData = await self.__lookupVoicemails(
                messageContent = messageContent,
                chatterUserId = ctx.getAuthorId(),
                chatterUserName = ctx.getAuthorName(),
                twitchChannelId = await ctx.getTwitchChannelId()
            )
        except NoSuchUserException as e:
            self.__timber.log('VoicemailsChatCommand', f'Failed to find user ID information for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({messageContent=})', e, traceback.format_exc())

            self.__twitchChatMessenger.send(
                text = f'⚠ Failed to find voicemail info for the given user',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

            return

        self.__twitchChatMessenger.send(
            text = await self.__toString(
                ctx = ctx,
                voicemailLookupData = voicemailLookupData
            ),
            twitchChannelId = await ctx.getTwitchChannelId(),
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('VoicemailsChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

    async def __lookupVoicemails(
        self,
        messageContent: str | None,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannelId: str
    ) -> VoicemailLookupData:
        splits = utils.getCleanedSplits(messageContent)
        lookupUserName: str
        lookupUserId: str

        if len(splits) >= 2:
            lookupUserName = utils.removePreceedingAt(splits[1])

            lookupUserId = await self.__userIdsRepository.requireUserId(
                userName = lookupUserName,
                twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                    twitchChannelId = twitchChannelId
                )
            )
        else:
            lookupUserName = chatterUserName
            lookupUserId = chatterUserId

        voicemails = await self.__voicemailHelper.getAllForTargetUser(
            targetUserId = lookupUserId,
            twitchChannelId = twitchChannelId
        )

        return VoicemailsChatCommand.VoicemailLookupData(
            voicemails = voicemails,
            chatterUserId = lookupUserId,
            chatterUserName = lookupUserName
        )

    async def __toString(
        self,
        ctx: TwitchContext,
        voicemailLookupData: VoicemailLookupData
    ) -> str:
        voicemailsSize = len(voicemailLookupData.voicemails)
        voicemailsSizeStr = locale.format_string("%d", voicemailsSize, grouping = True)

        voicemailsPlurality: str
        if voicemailsSize == 1:
            voicemailsPlurality = 'voicemail'
        else:
            voicemailsPlurality = 'voicemails'

        maximumVoicemails = await self.__voicemailSettingsRepository.getMaximumPerTargetUser()
        maximumVoicemailsStr = locale.format_string("%d", maximumVoicemails, grouping = True)

        if voicemailsSize == 0:
            return f'ⓘ @{voicemailLookupData.chatterUserName} has {voicemailsSizeStr} {voicemailsPlurality} (maximum voicemail inbox size is {maximumVoicemailsStr})'

        mostRecentVoicemail = voicemailLookupData.voicemails[voicemailsSize - 1]
        mostRecentVoicemailUserName = mostRecentVoicemail.originatingUserName
        mostRecentVoicemailDateTime = SimpleDateTime(mostRecentVoicemail.createdDateTime).getDateAndTimeStr()

        commandTutorialMessage: str
        if voicemailLookupData.chatterUserId == ctx.getAuthorId():
            commandTutorialMessage = ''
        else:
            commandTutorialMessage = ' You can play voicemails with the !playvoicemail command!'

        return f'ⓘ @{voicemailLookupData.chatterUserName} has {voicemailsSizeStr} {voicemailsPlurality} (most recent voicemail is from @{mostRecentVoicemailUserName}, {mostRecentVoicemailDateTime}).{commandTutorialMessage} (maximum voicemail inbox size is {maximumVoicemailsStr})'
