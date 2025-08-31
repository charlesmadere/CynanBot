from enum import Enum, auto


class UserJsonConstant(Enum):

    ANIV_CONTENT_SCANNING_ENABLED = auto()
    ANIV_MESSAGE_COPY_TIMEOUT_CHAT_REPORTING_ENABLED = auto()
    ANIV_MESSAGE_COPY_TIMEOUT_ENABLED = auto()
    ASPLODIE_STATS_ENABLED = auto()
    BEAN_STATS_ENABLED = auto()
    BLUE_SKY_URL = auto()
    CHATTER_INVENTORY_ENABLED = auto()
    CHATTER_PREFERRED_TTS_ENABLED = auto()
    CHAT_SOUND_ALERTS_ENABLED = auto()
    CHEER_ACTIONS_ENABLED = auto()
    CROWD_CONTROL_ENABLED = auto()
    CUTENESS_ENABLED = auto()
    CYNAN_SOURCE_ENABLED = auto()
    DISCORD_URL = auto()
    ECCO_ENABLED = auto()
    ENABLED = auto()
    GIVE_CUTENESS_ENABLED = auto()
    LOCATION_ID = auto()
    MASTODON_URL = auto()
    MAXIMUM_GRENADES_WITHIN_COOLDOWN = auto()
    NOTIFY_OF_RAID_ENABLED = auto()
    PRANKS_ENABLED = auto()
    RECURRING_ACTIONS_ENABLED = auto()
    REDEMPTION_COUNTERS_ENABLED = auto()
    SOUND_ALERTS_ENABLED = auto()
    TIMEZONE = auto()
    TIMEZONES = auto()
    TTS_ENABLED = auto()
    VOICEMAIL_ENABLED = auto()
    VULNERABLE_CHATTERS_ENABLED = auto()
    WEATHER_ENABLED = auto()
    WHICH_ANIV_USER = auto()

    @property
    def jsonKey(self) -> str:
        match self:
            case UserJsonConstant.ANIV_CONTENT_SCANNING_ENABLED: return 'anivContentScanningEnabled'
            case UserJsonConstant.ANIV_MESSAGE_COPY_TIMEOUT_CHAT_REPORTING_ENABLED: return 'anivMessageCopyTimeoutChatReportingEnabled'
            case UserJsonConstant.ANIV_MESSAGE_COPY_TIMEOUT_ENABLED: return 'anivMessageCopyTimeoutEnabled'
            case UserJsonConstant.ASPLODIE_STATS_ENABLED: return 'asplodieStatsEnabled'
            case UserJsonConstant.BEAN_STATS_ENABLED: return 'beanStatsEnabled'
            case UserJsonConstant.BLUE_SKY_URL: return 'blueSkyUrl'
            case UserJsonConstant.CHATTER_INVENTORY_ENABLED: return 'chatterInventoryEnabled'
            case UserJsonConstant.CHATTER_PREFERRED_TTS_ENABLED: return 'chatterPreferredTtsEnabled'
            case UserJsonConstant.CHAT_SOUND_ALERTS_ENABLED: return 'chatSoundAlertsEnabled'
            case UserJsonConstant.CHEER_ACTIONS_ENABLED: return 'cheerActionsEnabled'
            case UserJsonConstant.CROWD_CONTROL_ENABLED: return 'crowdControlEnabled'
            case UserJsonConstant.CUTENESS_ENABLED: return 'cutenessEnabled'
            case UserJsonConstant.CYNAN_SOURCE_ENABLED: return 'cynanSourceEnabled'
            case UserJsonConstant.DISCORD_URL: return 'discordUrl'
            case UserJsonConstant.ECCO_ENABLED: return 'eccoEnabled'
            case UserJsonConstant.ENABLED: return 'enabled'
            case UserJsonConstant.GIVE_CUTENESS_ENABLED: return 'giveCutenessEnabled'
            case UserJsonConstant.LOCATION_ID: return 'locationId'
            case UserJsonConstant.MASTODON_URL: return 'mastodonUrl'
            case UserJsonConstant.MAXIMUM_GRENADES_WITHIN_COOLDOWN: return 'maximumGrenadesWithinCooldown'
            case UserJsonConstant.NOTIFY_OF_RAID_ENABLED: return 'notifyOfRaidEnabled'
            case UserJsonConstant.PRANKS_ENABLED: return 'pranksEnabled'
            case UserJsonConstant.RECURRING_ACTIONS_ENABLED: return 'recurringActionsEnabled'
            case UserJsonConstant.REDEMPTION_COUNTERS_ENABLED: return 'redemptionCountersEnabled'
            case UserJsonConstant.SOUND_ALERTS_ENABLED: return 'soundAlertsEnabled'
            case UserJsonConstant.TIMEZONE: return 'timeZone'
            case UserJsonConstant.TIMEZONES: return 'timeZones'
            case UserJsonConstant.TTS_ENABLED: return 'ttsEnabled'
            case UserJsonConstant.VOICEMAIL_ENABLED: return 'voicemailEnabled'
            case UserJsonConstant.VULNERABLE_CHATTERS_ENABLED: return 'vulnerableChattersEnabled'
            case UserJsonConstant.WEATHER_ENABLED: return 'weatherEnabled'
            case UserJsonConstant.WHICH_ANIV_USER: return 'whichAnivUser'
            case _: raise ValueError(f'unknown UserJsonConstant value: \"{self}\"')
