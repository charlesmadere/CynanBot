from src.users.userJsonConstant import UserJsonConstant


class TestUserJsonConstants:

    def test_allJsonKeyValuesAreCorrectlyImplemented(self):
        allJsonKeys: set[str] = set()

        for userJsonConstant in UserJsonConstant:
            allJsonKeys.add(userJsonConstant.jsonKey)

        assert len(allJsonKeys) == len(UserJsonConstant)

    def test_jsonKey_withAnivContentScanningEnabled(self):
        result = UserJsonConstant.ANIV_CONTENT_SCANNING_ENABLED.jsonKey
        assert result == 'anivContentScanningEnabled'

    def test_jsonKey_withAnivMessageCopyTimeoutChatReportingEnabled(self):
        result = UserJsonConstant.ANIV_MESSAGE_COPY_TIMEOUT_CHAT_REPORTING_ENABLED.jsonKey
        assert result == 'anivMessageCopyTimeoutChatReportingEnabled'

    def test_jsonKey_withAnivMessageCopyTimeoutEnabled(self):
        result = UserJsonConstant.ANIV_MESSAGE_COPY_TIMEOUT_ENABLED.jsonKey
        assert result == 'anivMessageCopyTimeoutEnabled'

    def test_jsonKey_withAsplodieStatsEnabled(self):
        result = UserJsonConstant.ASPLODIE_STATS_ENABLED.jsonKey
        assert result == 'asplodieStatsEnabled'

    def test_jsonKey_withBeanStatsEnabled(self):
        result = UserJsonConstant.BEAN_STATS_ENABLED.jsonKey
        assert result == 'beanStatsEnabled'

    def test_jsonKey_withBlueSkyUrl(self):
        result = UserJsonConstant.BLUE_SKY_URL.jsonKey
        assert result == 'blueSkyUrl'

    def test_jsonKey_withChatterPreferredTtsEnabled(self):
        result = UserJsonConstant.CHATTER_PREFERRED_TTS_ENABLED.jsonKey
        assert result == 'chatterPreferredTtsEnabled'

    def test_jsonKey_withChatSoundAlertsEnabled(self):
        result = UserJsonConstant.CHAT_SOUND_ALERTS_ENABLED.jsonKey
        assert result == 'chatSoundAlertsEnabled'

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

    def test_jsonKey_withDiscordUrl(self):
        result = UserJsonConstant.DISCORD_URL.jsonKey
        assert result == 'discordUrl'

    def test_jsonKey_withEccoEnabled(self):
        result = UserJsonConstant.ECCO_ENABLED.jsonKey
        assert result == 'eccoEnabled'

    def test_jsonKey_withEnabled(self):
        result = UserJsonConstant.ENABLED.jsonKey
        assert result == 'enabled'

    def test_jsonKey_withGiveCutenessEnabled(self):
        result = UserJsonConstant.GIVE_CUTENESS_ENABLED.jsonKey
        assert result == 'giveCutenessEnabled'

    def test_jsonKey_withLocationId(self):
        result = UserJsonConstant.LOCATION_ID.jsonKey
        assert result == 'locationId'

    def test_jsonKey_withMaximumGrenadesWithinCooldown(self):
        result = UserJsonConstant.MAXIMUM_GRENADES_WITHIN_COOLDOWN.jsonKey
        assert result == 'maximumGrenadesWithinCooldown'

    def test_jsonKey_withRecurringActionsEnabled(self):
        result = UserJsonConstant.RECURRING_ACTIONS_ENABLED.jsonKey
        assert result == 'recurringActionsEnabled'

    def test_jsonKey_withRedemptionCountersEnabled(self):
        result = UserJsonConstant.REDEMPTION_COUNTERS_ENABLED.jsonKey
        assert result == 'redemptionCountersEnabled'

    def test_jsonKey_withSoundAlertsEnabled(self):
        result = UserJsonConstant.SOUND_ALERTS_ENABLED.jsonKey
        assert result == 'soundAlertsEnabled'

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

    def test_jsonkey_withVoicemailEnabled(self):
        result = UserJsonConstant.VOICEMAIL_ENABLED.jsonKey
        assert result == 'voicemailEnabled'

    def test_jsonKey_withVulnerableChattersEnabled(self):
        result = UserJsonConstant.VULNERABLE_CHATTERS_ENABLED.jsonKey
        assert result == 'vulnerableChattersEnabled'

    def test_jsonKey_withWeatherEnabled(self):
        result = UserJsonConstant.WEATHER_ENABLED.jsonKey
        assert result == 'weatherEnabled'

    def test_jsonKey_withWhichAnivUser(self):
        result = UserJsonConstant.WHICH_ANIV_USER.jsonKey
        assert result == 'whichAnivUser'
