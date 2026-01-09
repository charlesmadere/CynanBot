import re
import traceback
from typing import Final, Pattern

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..chatterPreferredTts.chatterPreferredTtsPresenter import ChatterPreferredTtsPresenter
from ..chatterPreferredTts.exceptions import FailedToChooseRandomTtsException, NoEnabledTtsProvidersException, \
    TtsProviderIsNotEnabledException, UnableToParseUserMessageIntoTtsException
from ..chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ..chatterPreferredTts.models.chatterPrefferedTts import ChatterPreferredTts
from ..chatterPreferredTts.settings.chatterPreferredTtsSettingsRepositoryInterface import \
    ChatterPreferredTtsSettingsRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage


class ChatterPreferredTtsPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        chatterPreferredTtsPresenter: ChatterPreferredTtsPresenter,
        chatterPreferredTtsSettingsRepository: ChatterPreferredTtsSettingsRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(chatterPreferredTtsPresenter, ChatterPreferredTtsPresenter):
            raise TypeError(f'chatterPreferredTtsPresenter argument is malformed: \"{chatterPreferredTtsPresenter}\"')
        elif not isinstance(chatterPreferredTtsSettingsRepository, ChatterPreferredTtsSettingsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsSettingsRepository argument is malformed: \"{chatterPreferredTtsSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface] = chatterPreferredTtsHelper
        self.__chatterPreferredTtsPresenter: Final[ChatterPreferredTtsPresenter] = chatterPreferredTtsPresenter
        self.__chatterPreferredTtsSettingsRepository: Final[ChatterPreferredTtsSettingsRepositoryInterface] = chatterPreferredTtsSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__randomRegEx: Final[Pattern] = re.compile(r'^\s*\"?random(?:ize)?\"?\s*$', re.IGNORECASE)

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage,
    ) -> bool:
        if not await self.__chatterPreferredTtsSettingsRepository.isEnabled():
            return False

        twitchUser = twitchChannelPointsMessage.twitchUser
        if not twitchUser.isChatterPreferredTtsEnabled:
            return False

        userMessage = utils.cleanStr(twitchChannelPointsMessage.redemptionMessage)
        preferredTts: ChatterPreferredTts

        try:
            if self.__randomRegEx.fullmatch(userMessage):
                preferredTts = await self.__chatterPreferredTtsHelper.applyRandomPreferredTts(
                    chatterUserId = twitchChannelPointsMessage.userId,
                    twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
                )
            else:
                preferredTts = await self.__chatterPreferredTtsHelper.applyUserMessagePreferredTts(
                    chatterUserId = twitchChannelPointsMessage.userId,
                    twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
                    userMessage = userMessage,
                )
        except (FailedToChooseRandomTtsException, NoEnabledTtsProvidersException, UnableToParseUserMessageIntoTtsException) as e:
            self.__timber.log('ChatterPreferredTtsPointRedemption', f'Failed to set preferred TTS given by {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle} ({twitchChannelPointsMessage=}) ({userMessage=})', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ @{twitchChannelPointsMessage.userName} unable to set your preferred TTS! Please check your input and try again.',
                twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
            )
            return True
        except TtsProviderIsNotEnabledException as e:
            self.__timber.log('ChatterPreferredTtsPointRedemption', f'The TTS Provider requested by {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle} is not enabled ({userMessage=})', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ @{twitchChannelPointsMessage.userName} the TTS provider you requested is not available! Please try a different TTS provider.',
                twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
            )
            return True

        printOut = await self.__chatterPreferredTtsPresenter.printOut(
            preferredTts = preferredTts,
        )

        self.__twitchChatMessenger.send(
            text = f'ⓘ @{twitchChannelPointsMessage.userName} here\'s your new preferred TTS: {printOut}',
            twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
        )

        self.__timber.log('ChatterPreferredTtsPointRedemption', f'Redeemed for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle}')
        return True
