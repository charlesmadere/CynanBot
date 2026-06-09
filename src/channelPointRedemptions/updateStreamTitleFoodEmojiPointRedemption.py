import traceback
from dataclasses import dataclass
from typing import Final

import emoji
from emoji import Token

from .absChannelPointsRedemption import AbsChannelPointRedemption
from .pointsRedemptionResult import PointsRedemptionResult
from ..emojiHelper.emojiData import EmojiData
from ..emojiHelper.emojiHelperInterface import EmojiHelperInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.channelInformationHelper.twitchChannelInformationHelperInterface import \
    TwitchChannelInformationHelperInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ..users.userInterface import UserInterface


class UpdateStreamTitleFoodEmojiPointRedemption(AbsChannelPointRedemption):

    @dataclass(frozen = True, slots = True)
    class TitleAndEmoji:
        newEmoji: EmojiData
        newTitle: str

    def __init__(
        self,
        emojiHelper: EmojiHelperInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchChannelInformationHelper: TwitchChannelInformationHelperInterface,
    ):
        if not isinstance(emojiHelper, EmojiHelperInterface):
            raise TypeError(f'emojiHelper argument is malformed: \"{emojiHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchChannelInformationHelper, TwitchChannelInformationHelperInterface):
            raise TypeError(f'twitchChannelInformationHelper argument is malformed: \"{twitchChannelInformationHelper}\"')

        self.__emojiHelper: Final[EmojiHelperInterface] = emojiHelper
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchChannelInformationHelper: Final[TwitchChannelInformationHelperInterface] = twitchChannelInformationHelper

    async def __determineNextTitleAndEmoji(self, currentTitle: str) -> TitleAndEmoji:
        emojiList: list[Token] = list(emoji.analyze(currentTitle))
        newEmoji = await self.__emojiHelper.getRandomFoodAndDrinkEmoji()
        newTitle: str

        if len(emojiList) >= 1:
            existingEmoji = emojiList[0]

            while newEmoji.emoji == existingEmoji.value.emoji:
                newEmoji = await self.__emojiHelper.getRandomFoodAndDrinkEmoji()

            newTitle = f'{currentTitle[0:existingEmoji.value.start]}{newEmoji.emoji}{currentTitle[existingEmoji.value.end:]}'
        else:
            newTitle = f'{currentTitle} {newEmoji.emoji}'

        return UpdateStreamTitleFoodEmojiPointRedemption.TitleAndEmoji(
            newEmoji = newEmoji,
            newTitle = newTitle,
        )

    async def handlePointsRedemption(
        self,
        pointsRedemption: TwitchChannelPointsRedemption,
    ) -> PointsRedemptionResult:
        try:
            oldTitle = await self.__twitchChannelInformationHelper.requireTitle(
                twitchChannelId = pointsRedemption.twitchChannelId,
            )
        except Exception as e:
            self.__timber.log(self.pointsRedemptionName, f'Failed to fetch current stream title ({pointsRedemption=})', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ Failed to fetch current stream title',
                twitchChannelId = pointsRedemption.twitchChannelId,
            )
            return PointsRedemptionResult.CONSUMED

        nextTitleAndEmoji = await self.__determineNextTitleAndEmoji(
            currentTitle = oldTitle,
        )

        try:
            newTitle = await self.__twitchChannelInformationHelper.setTitle(
                title = nextTitleAndEmoji.newTitle,
                twitchChannelId = pointsRedemption.twitchChannelId,
            )
        except Exception as e:
            self.__timber.log(self.pointsRedemptionName, f'Failed to set new stream title ({nextTitleAndEmoji=}) ({pointsRedemption=})', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ Failed to set new stream title',
                twitchChannelId = pointsRedemption.twitchChannelId,
            )
            return PointsRedemptionResult.CONSUMED

        self.__twitchChatMessenger.send(
            text = f'ⓘ New stream title food emoji is {nextTitleAndEmoji.newEmoji.emoji} {nextTitleAndEmoji.newEmoji.emoji}!',
            twitchChannelId = pointsRedemption.twitchChannelId,
        )

        self.__timber.log(self.pointsRedemptionName, f'Redeemed ({newTitle=}) ({nextTitleAndEmoji=}) ({oldTitle=}) ({pointsRedemption=})')
        return PointsRedemptionResult.CONSUMED

    @property
    def pointsRedemptionName(self) -> str:
        return 'UpdateStreamTitleFoodEmojiPointRedemption'

    def relevantRewardIds(
        self,
        twitchUser: UserInterface,
    ) -> frozenset[str]:
        rewardId = twitchUser.updateStreamTitleFoodEmojiRewardId

        if utils.isValidStr(rewardId):
            return frozenset({ rewardId })
        else:
            return frozenset()
