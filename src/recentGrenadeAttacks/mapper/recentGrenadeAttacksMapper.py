from typing import Any

from .recentGrenadeAttacksMapperInterface import RecentGrenadeAttacksMapperInterface
from ..models.grenadeAttack import GrenadeAttack
from ...misc import utils as utils


class RecentGrenadeAttacksMapper(RecentGrenadeAttacksMapperInterface):

    async def parseGrenadeAttack(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> GrenadeAttack:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        attackedDateTime = utils.getDateTimeFromDict(jsonContents, 'dateTime')
        attackedUserId = utils.getStrFromDict(jsonContents, 'userId')

        return GrenadeAttack(
            attackedDateTime = attackedDateTime,
            attackedUserId = attackedUserId
        )

    async def serializeGrenadeAttack(
        self,
        grenadeAttack: GrenadeAttack
    ) -> dict[str, Any]:
        if not isinstance(grenadeAttack, GrenadeAttack):
            raise TypeError(f'grenadeAttack argument is malformed: \"{grenadeAttack}\"')

        dateTime = grenadeAttack.attackedDateTime.isoformat()

        return {
            'dateTime': dateTime,
            'userId': grenadeAttack.attackedUserId
        }
