from src.cheerActions.timeout.timeoutCheerActionTargetType import TimeoutCheerActionTargetType


class TestTimeoutCheerActionTargetType:

    def test_humanName(self):
        results: set[str] = set()

        for targetType in TimeoutCheerActionTargetType:
            results.add(targetType.humanName)

        assert len(results) == len(TimeoutCheerActionTargetType)

    def test_humanName_withAny(self):
        result = TimeoutCheerActionTargetType.ANY.humanName
        assert result == 'any'

    def test_humanName_withRandomOnly(self):
        result = TimeoutCheerActionTargetType.RANDOM_ONLY.humanName
        assert result == 'random only'

    def test_humanName_withSpecificTargetOnly(self):
        result = TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY.humanName
        assert result == 'specific target only'
