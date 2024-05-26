import random
from datetime import datetime, timedelta

import CynanBot.misc.utils as utils
from CynanBot.aniv.anivSettingsRepositoryInterface import \
    AnivSettingsRepositoryInterface
from CynanBot.aniv.anivUserIdProviderInterface import \
    AnivUserIdProviderInterface
from CynanBot.aniv.mostRecentAnivMessageRepositoryInterface import \
    MostRecentAnivMessageRepositoryInterface
from CynanBot.aniv.mostRecentAnivMessageTimeoutHelperInterface import \
    MostRecentAnivMessageTimeoutHelperInterface
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchChannelProvider import \
    TwitchChannelProvider
from CynanBot.twitch.timeout.twitchTimeoutHelperInterface import \
    TwitchTimeoutHelperInterface
from CynanBot.twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult
from CynanBot.twitch.twitchHandleProviderInterface import \
    TwitchHandleProviderInterface
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.userInterface import UserInterface


class MostRecentAnivMessageTimeoutHelper(MostRecentAnivMessageTimeoutHelperInterface):

    def __init__(
        self,
        anivSettingsRepository: AnivSettingsRepositoryInterface,
        anivUserIdProvider: AnivUserIdProviderInterface,
        mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(anivSettingsRepository, AnivSettingsRepositoryInterface):
            raise TypeError(f'anivSettingsRepository argument is malformed: \"{anivSettingsRepository}\"')
        elif not isinstance(anivUserIdProvider, AnivUserIdProviderInterface):
            raise TypeError(f'anivUserIdProvider argument is malformed: \"{anivUserIdProvider}\"')
        elif not isinstance(mostRecentAnivMessageRepository, MostRecentAnivMessageRepositoryInterface):
            raise TypeError(f'mostRecentAnivMessageRepository argument is malformed: \"{mostRecentAnivMessageRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTimeoutHelper, TwitchTimeoutHelperInterface):
            raise TypeError(f'twitchTimeoutHelper argument is malformed: \"{twitchTimeoutHelper}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__anivSettingsRepository: AnivSettingsRepositoryInterface = anivSettingsRepository
        self.__anivUserIdProvider: AnivUserIdProviderInterface = anivUserIdProvider
        self.__mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface = mostRecentAnivMessageRepository
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTimeoutHelper: TwitchTimeoutHelperInterface = twitchTimeoutHelper
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def checkMessageAndMaybeTimeout(
        self,
        chatterMessage: str | None,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannelId: str,
        user: UserInterface
    ) -> bool:
        if not user.isAnivMessageCopyTimeoutEnabled():
            return False

        anivUserId = await self.__anivUserIdProvider.getAnivUserId()

        if not utils.isValidStr(anivUserId) or anivUserId == chatterUserId or twitchChannelId == chatterUserId:
            return False

        chatterMessage = utils.cleanStr(chatterMessage)
        anivMessage = await self.__mostRecentAnivMessageRepository.get(twitchChannelId)

        if not utils.isValidStr(chatterMessage) or anivMessage is None:
            return False

        anivMessageText = anivMessage.message
        now = datetime.now(self.__timeZoneRepository.getDefault())
        expirationTime = anivMessage.dateTime + timedelta(seconds = await self.__anivSettingsRepository.getCopyMessageMaxAgeSeconds())

        if not utils.isValidStr(anivMessageText) or chatterMessage.casefold() != anivMessageText.casefold() or expirationTime < now:
            return False

        timeoutProbability = user.getAnivMessageCopyTimeoutChance()
        if not utils.isValidNum(timeoutProbability):
            timeoutProbability = await self.__anivSettingsRepository.getCopyMessageTimeoutProbability()

        if random.random() > timeoutProbability:
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'User {chatterUserName}:{chatterUserId} got away with copying a message from aniv! ({timeoutProbability=})')
            return False

        durationSeconds = user.getAnivMessageCopyTimeoutSeconds()
        if not utils.isValidInt(durationSeconds):
            durationSeconds = await self.__anivSettingsRepository.getCopyMessageTimeoutSeconds()

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(twitchHandle)
        if not utils.isValidStr(twitchAccessToken):
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'Failed to fetch Twitch access token when trying to time out {chatterUserName}:{chatterUserId} for copying a message from aniv')
            return False

        twitchChannelAccessToken = await self.__twitchTokensRepository.getAccessTokenById(twitchChannelId)
        if not utils.isValidStr(twitchChannelAccessToken):
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'Failed to fetch Twitch channel access token when trying to time out {chatterUserName}:{chatterUserId} for copying a message from aniv')
            return False

        timeoutResult = await self.__twitchTimeoutHelper.timeout(
            durationSeconds = durationSeconds,
            reason = None,
            twitchAccessToken = twitchAccessToken,
            twitchChannelAccessToken = twitchChannelAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = chatterUserId,
            user = user
        )

        if timeoutResult is not TwitchTimeoutResult.SUCCESS:
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'Failed to timeout user {chatterUserName}:{chatterUserId} after they copied a message from aniv ({timeoutResult=})')
            return False

        self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'User {chatterUserName}:{chatterUserId} was timed out for copying a message from aniv')

        twitchChannelProvider = self.__twitchChannelProvider
        if twitchChannelProvider is not None:
            twitchChannel = await twitchChannelProvider.getTwitchChannel(user.getHandle())
            await self.__twitchUtils.safeSend(twitchChannel, f'@{chatterUserName} RIPBOZO')

        return True

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
