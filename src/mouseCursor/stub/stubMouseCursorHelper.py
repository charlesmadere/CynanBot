from ..mouseCursorHelperInterface import MouseCursorHelperInterface
from ...users.userInterface import UserInterface


class StubMouseCursorHelper(MouseCursorHelperInterface):

    async def applyMouseCursor(
        self,
        twitchChannelId: str,
        twitchUser: UserInterface,
    ) -> bool:
        # this method is intentionally empty
        return False
