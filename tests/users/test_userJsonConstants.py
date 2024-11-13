from src.users.userJsonConstant import UserJsonConstant


class TestUserJsonConstants:

    def test_jsonKey_withAnivContentScanningEnabled(self):
        result = UserJsonConstant.ANIV_CONTENT_SCANNING_ENABLED.jsonKey
        assert result == 'anivContentScanningEnabled'

    def test_jsonKey_withAnivMessageCopyTimeoutEnabled(self):
        result = UserJsonConstant.ANIV_MESSAGE_COPY_TIMEOUT_ENABLED.jsonKey
        assert result == 'anivMessageCopyTimeoutEnabled'

    def test_jsonKey_withBeanChancesEnabled(self):
        result = UserJsonConstant.BEAN_CHANCES_ENABLED.jsonKey
        assert result == 'beanChancesEnabled'

    def test_jsonKey_withCatJamMessageEnabled(self):
        result = UserJsonConstant.CAT_JAM_MESSAGE_ENABLED.jsonKey
        assert result == 'catJamMessageEnabled'

    def test_jsonKey_withCheerActionsEnabled(self):
        result = UserJsonConstant.CHEER_ACTIONS_ENABLED.jsonKey
        assert result == 'cheerActionsEnabled'

    def test_jsonKey_withCrowdControlEnabled(self):
        result = UserJsonConstant.CROWD_CONTROL_ENABLED.jsonKey
        assert result == 'crowdControlEnabled'

    def test_jsonKey_withCutenessEnabled(self):
        result = UserJsonConstant.CUTENESS_ENABLED.jsonKey
        assert result == 'cutenessEnabled'

    def test_jsonKey_withCynanSourceEnabled(self):
        result = UserJsonConstant.CYNAN_SOURCE_ENABLED.jsonKey
        assert result == 'cynanSourceEnabled'

    def test_jsonKey_withEnabled(self):
        result = UserJsonConstant.ENABLED.jsonKey
        assert result == 'enabled'

    def test_jsonKey_withGiveCutenessEnabled(self):
        result = UserJsonConstant.GIVE_CUTENESS_ENABLED.jsonKey
        assert result == 'giveCutenessEnabled'

    def test_jsonKey_withLocationId(self):
        result = UserJsonConstant.LOCATION_ID.jsonKey
        assert result == 'locationId'

    def test_jsonKey_withRatJamMessageEnabled(self):
        result = UserJsonConstant.RAT_JAM_MESSAGE_ENABLED.jsonKey
        assert result == 'ratJamMessageEnabled'

    def test_jsonKey_withRecurringActionsEnabled(self):
        result = UserJsonConstant.RECURRING_ACTIONS_ENABLED.jsonKey
        assert result == 'recurringActionsEnabled'

    def test_jsonKey_withSoundAlertsEnabled(self):
        result = UserJsonConstant.SOUND_ALERTS_ENABLED.jsonKey
        assert result == 'soundAlertsEnabled'

    def test_jsonKey_withTimeoutActionsEnabled(self):
        result = UserJsonConstant.TIMEOUT_ACTIONS_ENABLED.jsonKey
        assert result == 'timeoutActionsEnabled'

    def test_jsonKey_withTimeZone(self):
        result = UserJsonConstant.TIMEZONE.jsonKey
        assert result == 'timeZone'

    def test_jsonKey_withTimeZones(self):
        result = UserJsonConstant.TIMEZONES.jsonKey
        assert result == 'timeZones'

    def test_jsonKey_withTtsEnabled(self):
        result = UserJsonConstant.TTS_ENABLED.jsonKey
        assert result == 'ttsEnabled'

    def test_jsonKey_withTtsMonsterApiUsageReportingEnabled(self):
        result = UserJsonConstant.TTS_MONSTER_API_USAGE_REPORTING_ENABLED.jsonKey
        assert result == 'ttsMonsterApiUsageReportingEnabled'

    def test_jsonKey_withTwitterUrl(self):
        result = UserJsonConstant.TWITTER_URL.jsonKey
        assert result == 'twitterUrl'

    def test_jsonKey_withWeatherEnabled(self):
        result = UserJsonConstant.WEATHER_ENABLED.jsonKey
        assert result == 'weatherEnabled'
