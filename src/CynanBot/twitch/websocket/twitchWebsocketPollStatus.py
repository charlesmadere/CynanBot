from enum import auto

from CynanBot.misc.enumWithToFromStr import EnumWithToFromStr


class TwitchWebsocketPollStatus(EnumWithToFromStr):

    ARCHIVED = auto()
    COMPLETED = auto()
    TERMINATED = auto()
