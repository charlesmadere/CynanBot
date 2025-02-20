from .absChannelPointRedemption import AbsChannelPointRedemption
from ..chatterPreferredTts.chatterPreferredTtsPresenter import ChatterPreferredTtsPresenter
from ..chatterPreferredTts.helper.chatterPreferredTtsUserMessageHelperInterface import \
    ChatterPreferredTtsUserMessageHelperInterface
from ..chatterPreferredTts.models.chatterPrefferedTts import ChatterPreferredTts
from ..chatterPreferredTts.repository.chatterPreferredTtsRepositoryInterface import \
    ChatterPreferredTtsRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface


class ChatterPreferredTtsPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        chatterPreferredTtsPresenter: ChatterPreferredTtsPresenter,
        chatterPreferredTtsRepository: ChatterPreferredTtsRepositoryInterface,
        chatterPreferredTtsUserMessageHelper: ChatterPreferredTtsUserMessageHelperInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(chatterPreferredTtsPresenter, ChatterPreferredTtsPresenter):
            raise TypeError(f'chatterPreferredTtsPresenter argument is malformed: \"{chatterPreferredTtsPresenter}\"')
        elif not isinstance(chatterPreferredTtsRepository, ChatterPreferredTtsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsRepository argument is malformed: \"{chatterPreferredTtsRepository}\"')
        elif not isinstance(chatterPreferredTtsUserMessageHelper, ChatterPreferredTtsUserMessageHelperInterface):
            raise TypeError(f'chatterPreferredTtsUserMessageHelper argument is malformed: \"{chatterPreferredTtsUserMessageHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__chatterPreferredTtsPresenter: ChatterPreferredTtsPresenter = chatterPreferredTtsPresenter
        self.__chatterPreferredTtsRepository: ChatterPreferredTtsRepositoryInterface = chatterPreferredTtsRepository
        self.__chatterPreferredTtsUserMessageHelper: ChatterPreferredTtsUserMessageHelperInterface = chatterPreferredTtsUserMessageHelper
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.twitchUser
        if not twitchUser.isChatterPreferredTtsEnabled:
            return False

        absPreferredTts = await self.__chatterPreferredTtsUserMessageHelper.parseUserMessage(
            userMessage = twitchChannelPointsMessage.redemptionMessage
        )

        if absPreferredTts is None:
            await self.__twitchUtils.safeSend(twitchChannel, f'⚠️ @{twitchChannelPointsMessage.userName} failed to set your preferred TTS voice! Please try again')
            self.__timber.log('ChatterPreferredTtsPointRedemption', f'Failed to set preferred TTS voice ({twitchChannelPointsMessage=}) ({absPreferredTts=})')
            return False

        preferredTts = ChatterPreferredTts(
            preferredTts = absPreferredTts,
            chatterUserId = twitchChannelPointsMessage.userId,
            twitchChannelId = await twitchChannel.getTwitchChannelId()
        )

        await self.__chatterPreferredTtsRepository.set(
            preferredTts = preferredTts
        )

        printOut = await self.__chatterPreferredTtsPresenter.printOut(preferredTts)
        await self.__twitchUtils.safeSend(twitchChannel, f'ⓘ @{twitchChannelPointsMessage.userName} Here\'s your new preferred TTS: {printOut}')
        self.__timber.log('ChatterPreferredTtsPointRedemption', f'Redeemed for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle}')
        return True
