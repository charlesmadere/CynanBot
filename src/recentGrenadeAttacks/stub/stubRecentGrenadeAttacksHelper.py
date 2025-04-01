from ..helper.recentGrenadeAttacksHelperInterface import RecentGrenadeAttacksHelperInterface


class StubRecentGrenadeAttacksHelper(RecentGrenadeAttacksHelperInterface):

    async def canThrowGrenade(
        self,
        attackerUserId: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> bool:
        # this method is intentionally empty
        return True

    async def fetchAvailableGrenades(
        self,
        attackerUserId: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> int | None:
        # this method is intentionally empty
        return None

    async def throwGrenade(
        self,
        attackedUserId: str,
        attackerUserId: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> int | None:
        # this method is intentionally empty
        return None
