from ..mouseCursorHelperInterface import MouseCursorHelperInterface


class StubMouseCursorHelper(MouseCursorHelperInterface):

    async def applyMouseCursor(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> bool:
        # this method is intentionally empty
        return False
