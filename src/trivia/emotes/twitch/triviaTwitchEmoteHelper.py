from typing import Final

from .triviaTwitchEmoteHelperInterface import TriviaTwitchEmoteHelperInterface
from ....trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface


class TriviaTwitchEmoteHelper(TriviaTwitchEmoteHelperInterface):

    def __init__(
        self,
        trollmojiHelper: TrollmojiHelperInterface
    ):
        if not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')

        self.__trollmojiHelper: Final[TrollmojiHelperInterface] = trollmojiHelper

    async def getCelebratoryEmote(self) -> str | None:
        return await self.__trollmojiHelper.getHypeEmote()

    async def getOutOfTimeEmote(self) -> str | None:
        return await self.__trollmojiHelper.getShrugEmote()

    async def getWrongAnswerEmote(self) -> str | None:
        return await self.__trollmojiHelper.getThumbsDownEmote()
