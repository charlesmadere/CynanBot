from dataclasses import dataclass

from frozenlist import FrozenList

from .grenadeAttack import GrenadeAttack


@dataclass(frozen = True)
class RecentGrenadeAttackData:
    grenadeAttacks: FrozenList[GrenadeAttack]
    attackerUserId: str
    twitchChannelId: str
