from enum import Enum, auto


class TwitchApiScope(Enum):

    BITS_READ = auto()
    CHANNEL_BOT = auto()
    CHANNEL_MANAGE_POLLS = auto()
    CHANNEL_MANAGE_PREDICTIONS = auto()
    CHANNEL_MANAGE_REDEMPTIONS = auto()
    CHANNEL_MODERATE = auto()
    CHANNEL_READ_POLLS = auto()
    CHANNEL_READ_PREDICTIONS = auto()
    CHANNEL_READ_REDEMPTIONS = auto()
    CHANNEL_READ_SUBSCRIPTIONS = auto()
    CHAT_EDIT = auto()
    CHAT_READ = auto()
    MODERATION_READ = auto()
    MODERATOR_MANAGE_BANNED_USERS = auto()
    MODERATOR_MANAGE_CHAT_MESSAGES = auto()
    MODERATOR_READ_CHATTERS = auto()
    MODERATOR_READ_CHAT_SETTINGS = auto()
    MODERATOR_READ_FOLLOWERS = auto()
    USER_BOT = auto()
    USER_READ_BROADCAST = auto()
    USER_READ_EMOTES = auto()
    USER_READ_FOLLOWS = auto()
    USER_READ_SUBSCRIPTIONS = auto()
