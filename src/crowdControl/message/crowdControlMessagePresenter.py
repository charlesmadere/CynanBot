from typing import Final

from .crowdControlMessage import CrowdControlMessage
from .crowdControlMessagePresenterInterface import CrowdControlMessagePresenterInterface
from ..actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from ...trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface


class CrowdControlMessagePresenter(CrowdControlMessagePresenterInterface):

    def __init__(
        self,
        trollmojiHelper: TrollmojiHelperInterface,
    ):
        if not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')

        self.__trollmojiHelper: Final[TrollmojiHelperInterface] = trollmojiHelper

    async def toString(self, message: CrowdControlMessage) -> str | None:
        if not isinstance(message, CrowdControlMessage):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        if not isinstance(message, GameShuffleCrowdControlAction) or message.startOfGigaShuffleSize is None or message.startOfGigaShuffleSize <= 1:
            return None

        gottemEmote = await self.__trollmojiHelper.getGottemEmoteOrBackup()
        return f'{gottemEmote} just started a {message.startOfGigaShuffleSizeStr} GIGA SHUFFLE {gottemEmote}'
