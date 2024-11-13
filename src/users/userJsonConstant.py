from enum import Enum, auto


class UserJsonConstant(Enum):

    ANIV_CONTENT_SCANNING_ENABLED = auto()
    ANIV_MESSAGE_COPY_TIMEOUT_ENABLED = auto()
    BEAN_CHANCES_ENABLED = auto()
    CAT_JAM_MESSAGE_ENABLED = auto()
    CHEER_ACTIONS_ENABLED = auto()
    CROWD_CONTROL_ENABLED = auto()
    CUTENESS_ENABLED = auto()
    CYNAN_SOURCE_ENABLED = auto()
    ENABLED = auto()
    GIVE_CUTENESS_ENABLED = auto()
    LOCATION_ID = auto()
    RAT_JAM_MESSAGE_ENABLED = auto()
    RECURRING_ACTIONS_ENABLED = auto()
    SOUND_ALERTS_ENABLED = auto()
    TIMEOUT_ACTIONS_ENABLED = auto()
    TIMEZONE = auto()
    TIMEZONES = auto()
    TTS_ENABLED = auto()
    TTS_MONSTER_API_USAGE_REPORTING_ENABLED = auto()
    TWITTER_URL = auto()
    WEATHER_ENABLED = auto()

    @property
    def jsonKey(self) -> str:
        match self:
            case UserJsonConstant.ANIV_CONTENT_SCANNING_ENABLED: return 'anivContentScanningEnabled'
            case UserJsonConstant.ANIV_MESSAGE_COPY_TIMEOUT_ENABLED: return 'anivMessageCopyTimeoutEnabled'
            case UserJsonConstant.BEAN_CHANCES_ENABLED: return 'beanChancesEnabled'
            case UserJsonConstant.CAT_JAM_MESSAGE_ENABLED: return 'catJamMessageEnabled'
            case UserJsonConstant.CHEER_ACTIONS_ENABLED: return 'cheerActionsEnabled'
            case UserJsonConstant.CROWD_CONTROL_ENABLED: return 'crowdControlEnabled'
            case UserJsonConstant.CUTENESS_ENABLED: return 'cutenessEnabled'
            case UserJsonConstant.CYNAN_SOURCE_ENABLED: return 'cynanSourceEnabled'
            case UserJsonConstant.ENABLED: return 'enabled'
            case UserJsonConstant.GIVE_CUTENESS_ENABLED: return 'giveCutenessEnabled'
            case UserJsonConstant.LOCATION_ID: return 'locationId'
            case UserJsonConstant.RAT_JAM_MESSAGE_ENABLED: return 'ratJamMessageEnabled'
            case UserJsonConstant.RECURRING_ACTIONS_ENABLED: return 'recurringActionsEnabled'
            case UserJsonConstant.SOUND_ALERTS_ENABLED: return 'soundAlertsEnabled'
            case UserJsonConstant.TIMEOUT_ACTIONS_ENABLED: return 'timeoutActionsEnabled'
            case UserJsonConstant.TIMEZONE: return 'timeZone'
            case UserJsonConstant.TIMEZONES: return 'timeZones'
            case UserJsonConstant.TTS_ENABLED: return 'ttsEnabled'
            case UserJsonConstant.TTS_MONSTER_API_USAGE_REPORTING_ENABLED: return 'ttsMonsterApiUsageReportingEnabled'
            case UserJsonConstant.TWITTER_URL: return 'twitterUrl'
            case UserJsonConstant.WEATHER_ENABLED: return 'weatherEnabled'
            case _: raise ValueError(f'unknown UserJsonConstant value: \"{self}\"')
