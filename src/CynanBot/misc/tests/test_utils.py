import math
from datetime import datetime
from typing import Any

import pytest

import CynanBot.misc.utils as utils


class TestUtils():

    def test_areAllStrsInts_withEmptyList(self):
        result: bool | None = None
        exception: Exception | None = None

        try:
            result = utils.areAllStrsInts(list())
        except Exception as e:
            exception = e

        assert result is None
        assert exception is not None
        assert isinstance(exception, Exception)

    def test_areAllStrsInts_withIntList(self):
        result = utils.areAllStrsInts([ '1', '10', '100', '1000' ])
        assert result is True

    def test_areAllStrsInts_withMixedList(self):
        result = utils.areAllStrsInts([ '1', '10', '100', 'hello', '1000', 'world' ])
        assert result is False

    def test_areAllStrsInts_withNone(self):
        result: bool | None = None

        with pytest.raises(Exception):
            result = utils.areAllStrsInts(None)

        assert result is None

    def test_areAllStrsInts_withWordList(self):
        result = utils.areAllStrsInts([ 'hello', 'world' ])
        assert result is False

    def test_areValidBools_withEmptyList(self):
        result = utils.areValidBools(list())
        assert result is False

    def test_areValidBools_withEmptyStringList(self):
        result = utils.areValidBools([ '', '\n', 'hello', 'world', '' ])
        assert result is False

    def test_areValidBools_withIntList(self):
        result = utils.areValidBools([ 100, 200 ])
        assert result is False

    def test_areValidBools_withMixedTypeList(self):
        result = utils.areValidBools([ True, 'hello', 1, False ])
        assert result is False

    def test_areValidBools_withNone(self):
        result = utils.areValidBools(None)
        assert result is False

    def test_areValidBools_withValidList(self):
        result = utils.areValidBools([ True, False, False, True ])
        assert result is True

    def test_areValidStrs_withEmptyList(self):
        result = utils.areValidStrs(list())
        assert result is False

    def test_areValidStrs_withEmptyStringList(self):
        result = utils.areValidStrs([ '', '\n', 'hello', 'world', '' ])
        assert result is False

    def test_areValidStrs_withIntList(self):
        result = utils.areValidStrs([ 100, 200 ])
        assert result is False

    def test_areValidStrs_withMixedTypeList(self):
        result = utils.areValidStrs([ True, 'hello', 1, False ])
        assert result is False

    def test_areValidStrs_withNone(self):
        result = utils.areValidStrs(None)
        assert result is False

    def test_areValidStrs_withValidList(self):
        result = utils.areValidStrs([ 'hello', 'world' ])
        assert result is True

    def test_boolToNum_withFalse(self):
        result = utils.boolToNum(False)
        assert result == 0

    def test_boolToNum_withTrue(self):
        result = utils.boolToNum(True)
        assert result == 1

    def test_containsUrl_withEmptyString(self):
        result = utils.containsUrl('')
        assert result is False

    def test_containsUrl_withGoogle(self):
        result = utils.containsUrl('https://www.google.com/')
        assert result is True

    def test_containsUrl_withGoogleSentence(self):
        result = utils.containsUrl('There\'s a URL here: https://www.google.com/ in this sentence.')
        assert result is True

    def test_containsUrl_withNone(self):
        result = utils.containsUrl(None)
        assert result is False

    def test_containsUrl_withRandomNoise1(self):
        result = utils.containsUrl('Qd19u(KAyCuZ~qNQkd-iy\\%\\E|KxRc')
        assert result is False

    def test_containsUrl_withRandomNoise2(self):
        result = utils.containsUrl('.s*&Sxwa}RZ\\\'AIkvD6:&OkVT#_YA`')
        assert result is False

    def test_copyList_withEmptyList(self):
        original: list[Any] = list()
        result = utils.copyList(original)
        assert result is not None
        assert len(result) == 0
        assert result is not original

    def test_copyList_withIntList(self):
        original: list[int] = [ 1, 2, 3, 4 ]
        result = utils.copyList(original)
        assert result is not None
        assert len(result) == 4
        assert result is not original
        assert result == original

    def test_copyList_withNone(self):
        result: list = utils.copyList(None)
        assert result is not None
        assert len(result) == 0

    def test_copyList_withStrList(self):
        original: list[str] = [ '1', '2', '3', '4' ]
        result = utils.copyList(original)
        assert result is not None
        assert len(result) == 4
        assert result is not original
        assert result == original

    def test_getBoolFromDict_withEmptyDict(self):
        d: dict[str, Any] = dict()
        value: bool | None = None
        exception: Exception | None = None

        try:
            value = utils.getBoolFromDict(d = d, key = "hello")
        except Exception as e:
            exception = e

        assert value is None
        assert exception is not None

    def test_getBoolFromDict_withEmptyDictAndNoneFallback(self):
        d: dict[str, Any] = dict()
        value: bool | None = None
        exception: Exception | None = None

        try:
            value = utils.getBoolFromDict(d = d, key = "hello")
        except Exception as e:
            exception = e

        assert value is None
        assert exception is not None

    def test_getBoolFromDict_withNoneDict(self):
        d: dict[str, Any] | None = None
        value: bool | None = None
        exception: Exception | None = None

        try:
            value = utils.getBoolFromDict(d = d, key = "hello", fallback = True)
        except Exception as e:
            exception = e

        assert value is True
        assert exception is None

    def test_getBoolFromDict_withNoneDictAndNoneFallback(self):
        d: dict[str, Any] | None = None
        value: bool | None = None
        exception: Exception | None = None

        try:
            value = utils.getBoolFromDict(d = d, key = "hello")
        except Exception as e:
            exception = e

        assert value is None
        assert exception is not None

    def test_getCleanedSplits_withEmptyString(self):
        original = ''
        result = utils.getCleanedSplits(original)
        assert result is not None
        assert len(result) == 0

    def test_getCleanedSplits_withHelloWorld(self):
        original = 'Hello, World!'
        result = utils.getCleanedSplits(original)
        assert result is not None
        assert len(result) == 2
        assert result[0] == 'Hello,'
        assert result[1] == 'World!'

    def test_getCleanedSplits_withNone(self):
        original: str | None = None
        result = utils.getCleanedSplits(original)
        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 0

    def test_getCleanedSplits_withWhitespaceString(self):
        original = ' '
        result = utils.getCleanedSplits(original)
        assert result is not None
        assert len(result) == 0

    def test_getDateTimeFromStr_withDateTimeString1(self):
        result = utils.getDateTimeFromStr('2002-01-01T23:11:59')
        assert isinstance(result, datetime)
        assert result.year == 2002
        assert result.month == 1
        assert result.day == 1
        assert result.hour == 23
        assert result.minute == 11
        assert result.second == 59

    def test_getDateTimeFromStr_withEmptyString(self):
        result = utils.getDateTimeFromStr('')
        assert result is None

    def test_getDateTimeFromStr_withNone(self):
        result = utils.getDateTimeFromStr(None)
        assert result is None

    def test_getDateTimeFromStr_withTwitchDateTimeString(self):
        result = utils.getDateTimeFromStr('2023-10-21T14:11:45.338014562Z')
        assert isinstance(result, datetime)
        assert result.year == 2023
        assert result.month == 10
        assert result.day == 21
        assert result.hour == 14
        assert result.minute == 11
        assert result.second == 45

    def test_getDateTimeFromStr_withZPlusDateTimeString(self):
        result = utils.getDateTimeFromStr('2023-11-11T17:13:41Z+00:00')
        assert isinstance(result, datetime)
        assert result.year == 2023
        assert result.month == 11
        assert result.day == 11
        assert result.hour == 17
        assert result.minute == 13
        assert result.second == 41

    def test_getFloatFromDict_withEmptyDict(self):
        d: dict[str, Any] = dict()
        value: float | None = None
        exception: Exception | None = None

        try:
            value = utils.getFloatFromDict(d = d, key = "hello", fallback = 3.14)
        except Exception as e:
            exception = e

        assert value == 3.14
        assert exception is None

    def test_getFloatFromDict_withEmptyDictAndNoneFallback(self):
        d: dict[str, Any] = dict()
        value: float | None = None
        exception: Exception | None = None

        try:
            value = utils.getFloatFromDict(d = d, key = "hello")
        except Exception as e:
            exception = e

        assert value is None
        assert exception is not None

    def test_getFloatFromDict_withNoneDict(self):
        d: dict[str, Any] | None = None
        value: float | None = None
        exception: Exception | None = None

        try:
            value = utils.getFloatFromDict(d = d, key = "hello", fallback = 1.1)
        except Exception as e:
            exception = e

        assert value == 1.1
        assert exception is None

    def test_getFloatFromDict_withNoneDictAndNoneFallback(self):
        d: dict[str, Any] | None = None
        value: float | None = None
        exception: Exception | None = None

        try:
            value = utils.getFloatFromDict(d = d, key = "hello")
        except Exception as e:
            exception = e

        assert value is None
        assert exception is not None

    def test_getIntFromDict_withEmptyDict(self):
        d: dict[str, Any] = dict()
        value: int | None = None
        exception: Exception | None = None

        try:
            value = utils.getIntFromDict(d = d, key = "hello", fallback = 64)
        except Exception as e:
            exception = e

        assert value == 64
        assert exception is None

    def test_getIntFromDict_withEmptyDictAndNoneFallback(self):
        d: dict[str, Any] = dict()
        value: int | None = None
        exception: Exception | None = None

        try:
            value = utils.getIntFromDict(d = d, key = "hello")
        except Exception as e:
            exception = e

        assert value is None
        assert exception is not None

    def test_getIntFromDict_withNoneDict(self):
        d: dict[str, Any] | None = None
        value: int | None = None
        exception: Exception | None = None

        try:
            value = utils.getIntFromDict(d = d, key = "hello", fallback = 2000)
        except Exception as e:
            exception = e

        assert value == 2000
        assert exception is None

    def test_getIntFromDict_withNoneDictAndNoneFallback(self):
        d: dict[str, Any] | None = None
        value: int | None = None
        exception: Exception | None = None

        try:
            value = utils.getIntFromDict(d = d, key = "hello")
        except Exception as e:
            exception = e

        assert value is None
        assert exception is not None

    def test_isValidBool_withFalse(self):
        result = utils.isValidBool(False)
        assert result is True

    def test_isValidBool_withNone(self):
        result = utils.isValidBool(None)
        assert result is False

    def test_isValidBool_withTrue(self):
        result = utils.isValidBool(True)
        assert result is True

    def test_isValidInt_withNan(self):
        result = utils.isValidInt(math.nan)
        assert result is False

    def test_isValidInt_withNegativeOne(self):
        result = utils.isValidInt(-1)
        assert result is True

    def test_isValidInt_withNone(self):
        result = utils.isValidInt(None)
        assert result is False

    def test_isValidInt_withOne(self):
        result = utils.isValidInt(1)
        assert result is True

    def test_isValidInt_withPi(self):
        result = utils.isValidInt(math.pi)
        assert result is False

    def test_isValidInt_withTwo(self):
        result = utils.isValidInt(2)
        assert result is True

    def test_isValidInt_withZero(self):
        result = utils.isValidInt(0)
        assert result is True

    def test_isValidNum_withFloat(self):
        result = utils.isValidNum(3.33)
        assert result is True

    def test_isValidNum_withInt(self):
        result = utils.isValidNum(100)
        assert result is True

    def test_isValidNum_withNan(self):
        result = utils.isValidNum(math.nan)
        assert result is False

    def test_isValidNum_withNone(self):
        result = utils.isValidNum(None)
        assert result is False

    def test_isValidNum_withPi(self):
        result = utils.isValidNum(math.pi)
        assert result is True

    def test_isValidStr_withEmptyString(self):
        result = utils.isValidStr('')
        assert result is False

    def test_isValidStr_withHelloWorldString(self):
        result = utils.isValidStr('Hello, World!')
        assert result is True

    def test_isValidStr_withNewLineString(self):
        result = utils.isValidStr('\n')
        assert result is False

    def test_isValidStr_withNone(self):
        result = utils.isValidStr(None)
        assert result is False

    def test_isValidStr_withWhitespaceString(self):
        result = utils.isValidStr(' ')
        assert result is False

    def test_isValidUrl_withEmptyString(self):
        result = utils.isValidUrl('')
        assert result is False

    def test_isValidUrl_withGoogle(self):
        result = utils.isValidUrl('https://www.google.com/')
        assert result is True

        result = utils.isValidUrl('http://google.com')
        assert result is True

        result = utils.isValidUrl('https://google.com:8080/')
        assert result is True

    def test_isValidUrl_withNone(self):
        result = utils.isValidUrl(None)
        assert result is False

    def test_isValidUrl_withRandomNoise1(self):
        result = utils.isValidUrl('J)R+ALY,m`g9r>lO`+RMeb$XL.OF8np')
        assert result is False

    def test_isValidUrl_withRandomNoise2(self):
        result = utils.isValidUrl('rpt\\\'%TmN$lx!T.Gg2le)QVO4\\_UqMA8dA{=\\\'\\\"')
        assert result is False

    def test_isValidUrl_withWebsocketUrl(self):
        result = utils.isValidUrl('wss://eventsub.wss.twitch.tv/ws')
        assert result is True

    def test_isValidUrl_withWhitespaceString(self):
        result = utils.isValidUrl(' ')
        assert result is False

    def test_numToBool_withInf(self):
        result: bool | None = None

        with pytest.raises(Exception):
            result = utils.numToBool(math.inf)

        assert result is None

    def test_numToBool_withNan(self):
        result: bool | None = None

        with pytest.raises(Exception):
            result = utils.numToBool(math.nan)

        assert result is None

    def test_numToBool_withNegativeOne(self):
        result = utils.numToBool(-1)
        assert result is True

    def test_numToBool_withNegativeTwo(self):
        result = utils.numToBool(-2)
        assert result is True

    def test_numToBool_withNone(self):
        result: bool | None = None

        try:
            result = utils.numToBool(None)
        except Exception as e:
            exception = e

        assert result is None
        assert exception is not None

    def test_numToBool_withOne(self):
        result = utils.numToBool(1)
        assert result is True

    def test_numToBool_withTen(self):
        result = utils.numToBool(10)
        assert result is True

    def test_numToBool_withTwo(self):
        result = utils.numToBool(2)
        assert result is True

    def test_numToBool_withZero(self):
        result = utils.numToBool(0)
        assert result is False

    def test_removePreceedingAt_withAtCharlesString(self):
        result = utils.removePreceedingAt('@charles')
        assert result == 'charles'

    def test_removePreceedingAt_withCharlesString(self):
        result = utils.removePreceedingAt('charles')
        assert result == 'charles'

    def test_removePreceedingAt_withEmptyString(self):
        result = utils.removePreceedingAt('')
        assert result == ''

    def test_removePreceedingAt_withNone(self):
        result = utils.removePreceedingAt(None)
        assert result is None

    def test_removePreceedingAt_withWhitespaceString(self):
        result = utils.removePreceedingAt(' ')
        assert result == ' '

    def test_safeStrToInt_withEmptyString(self):
        result = utils.safeStrToInt('')
        assert result is None

    def test_safeStrToInt_withIntMaxSafeSizeString(self):
        result = utils.safeStrToInt(str(utils.getIntMaxSafeSize()))
        assert isinstance(result, int)
        assert result == utils.getIntMaxSafeSize()

    def test_safeStrToInt_withIntMinSafeSizeString(self):
        result = utils.safeStrToInt(str(utils.getIntMinSafeSize()))
        assert isinstance(result, int)
        assert result == utils.getIntMinSafeSize()

    def test_safeStrToInt_withLongMaxSafeSizeString(self):
        result = utils.safeStrToInt(str(utils.getLongMaxSafeSize()))
        assert isinstance(result, int)
        assert result == utils.getLongMaxSafeSize()

    def test_safeStrToInt_withLongMinSafeSizeString(self):
        result = utils.safeStrToInt(str(utils.getLongMinSafeSize()))
        assert isinstance(result, int)
        assert result == utils.getLongMinSafeSize()

    def test_safeStrToInt_withNegativeOneString(self):
        result = utils.safeStrToInt('-1')
        assert isinstance(result, int)
        assert result == -1

    def test_safeStrToInt_withNone(self):
        result = utils.safeStrToInt(None)
        assert result is None

    def test_safeStrToInt_withNonsenseString1(self):
        result = utils.safeStrToInt('af9-d`7u;2npmFYO4_:/')
        assert result is None

    def test_safeStrToInt_withNonsenseString2(self):
        result = utils.safeStrToInt('X4W(MdKCP($-t04;\3UT')
        assert result is None

    def test_safeStrToInt_withOneString(self):
        result = utils.safeStrToInt('1')
        assert isinstance(result, int)
        assert result == 1

    def test_safeStrToInt_withWhitespaceString(self):
        result = utils.safeStrToInt(' ')
        assert result is None

    def test_safeStrToInt_withZeroString(self):
        result = utils.safeStrToInt('0')
        assert isinstance(result, int)
        assert result == 0

    def test_splitLongStringIntoMessages_withEmptyMessage(self):
        result = utils.splitLongStringIntoMessages(
            maxMessages = 50,
            perMessageMaxSize = 50,
            message = ''
        )

        assert result is not None
        assert len(result) == 0

    def test_splitLongStringIntoMessages_withNoneMessage(self):
        result = utils.splitLongStringIntoMessages(
            maxMessages = 50,
            perMessageMaxSize = 50,
            message = None
        )

        assert result is not None
        assert len(result) == 0

    def test_splitLongStringIntoMessages_withOneSentences(self):
        result = utils.splitLongStringIntoMessages(
            maxMessages = 50,
            perMessageMaxSize = 50,
            message = 'Hello, World!'
        )

        assert result is not None
        assert len(result) == 1
        assert result[0] == 'Hello, World!'

    def test_splitLongStringIntoMessages_withThreeSentences(self):
        result = utils.splitLongStringIntoMessages(
            maxMessages = 50,
            perMessageMaxSize = 50,
            message = 'Hello, World! This is an example sentence. This should be broken up into smaller strings. This message is three strings!'
        )

        assert result is not None
        assert len(result) == 3
        assert result[0] == 'Hello, World! This is an example sentence. This'
        assert result[1] == 'should be broken up into smaller strings. This'
        assert result[2] == 'message is three strings!'

    def test_splitLongStringIntoMessages_withTwoSentences(self):
        result = utils.splitLongStringIntoMessages(
            maxMessages = 50,
            perMessageMaxSize = 50,
            message = 'Hello, World! This is an example sentence. This should be broken up into smaller strings.'
        )

        assert result is not None
        assert len(result) == 2
        assert result[0] == 'Hello, World! This is an example sentence. This'
        assert result[1] == 'should be broken up into smaller strings.'

    def test_strContainsAlphanumericCharacters_withAtJrp2234(self):
        result = utils.strContainsAlphanumericCharacters('@JRP2234')
        assert result is True

    def test_strContainsAlphanumericCharacters_withAtNumbers(self):
        result = utils.strContainsAlphanumericCharacters('@9876')
        assert result is True

    def test_strContainsAlphanumericCharacters_withDot(self):
        result = utils.strContainsAlphanumericCharacters('.')
        assert result is False

    def test_strContainsAlphanumericCharacters_withEmptyString(self):
        result = utils.strContainsAlphanumericCharacters('')
        assert result is False

    def test_strContainsAlphanumericCharacters_withHelloWorld(self):
        result = utils.strContainsAlphanumericCharacters('Hello, World!')
        assert result is True

    def test_strContainsAlphanumericCharacters_withImyt(self):
        result = utils.strContainsAlphanumericCharacters('imyt')
        assert result is True

    def test_strContainsAlphanumericCharacters_withNone(self):
        result = utils.strContainsAlphanumericCharacters(None)
        assert result is False

    def test_strContainsAlphanumericCharacters_withNumbers(self):
        result = utils.strContainsAlphanumericCharacters('01234')
        assert result is True

    def test_strContainsAlphanumericCharacters_withQuotationMarks(self):
        result = utils.strContainsAlphanumericCharacters('""')
        assert result is False

    def test_strContainsAlphanumericCharacters_withSingleAlphabetCharacter(self):
        result = utils.strContainsAlphanumericCharacters('a')
        assert result is True

    def test_strContainsAlphanumericCharacters_withSingleNumberCharacter(self):
        result = utils.strContainsAlphanumericCharacters('1')
        assert result is True

    def test_strContainsAlphanumericCharacters_withUnderscore(self):
        result = utils.strContainsAlphanumericCharacters('_')
        assert result is False

    def test_strContainsAlphanumericCharacters_withWhitespace(self):
        result = utils.strContainsAlphanumericCharacters(' ')
        assert result is False

    def test_strictStrToBool_withEmptyString(self):
        result: bool | None = None

        with pytest.raises(ValueError):
            result = utils.strictStrToBool('')

        assert result is None

    def test_strictStrToBool_withF(self):
        result = utils.strictStrToBool('f')
        assert result is False

    def test_strictStrToBool_withFalse(self):
        result = utils.strictStrToBool('false')
        assert result is False

    def test_strictStrToBool_withNewLineString(self):
        result: bool | None = None

        with pytest.raises(ValueError):
            result = utils.strictStrToBool('\n')

        assert result is None

    def test_strictStrToBool_withNone(self):
        result: bool | None = None

        with pytest.raises(ValueError):
            result = utils.strictStrToBool(None)

        assert result is None

    def test_strictStrToBool_withT(self):
        result = utils.strictStrToBool('t')
        assert result is True

    def test_strictStrToBool_withTrue(self):
        result = utils.strictStrToBool('true')
        assert result is True

    def test_strictStrToBool_withWhitespaceString(self):
        result: bool | None = None

        with pytest.raises(ValueError):
            result = utils.strictStrToBool(' ')

        assert result is None

    def test_strToBool_withEmptyString(self):
        result = utils.strToBool('')
        assert result is True

    def test_strToBool_withF(self):
        result = utils.strToBool('f')
        assert result is False

    def test_strToBool_withFalse(self):
        result = utils.strToBool('false')
        assert result is False

    def test_strToBool_withNewLineString(self):
        result = utils.strToBool('\n')
        assert result is True

    def test_strToBool_withNone(self):
        result = utils.strToBool(None)
        assert result is True

    def test_strToBool_withT(self):
        result = utils.strToBool('t')
        assert result is True

    def test_strToBool_withTrue(self):
        result = utils.strToBool('true')
        assert result is True

    def test_strToBool_withWhitespaceString(self):
        result = utils.strToBool(' ')
        assert result is True

    def test_strToBools_withEmptyList(self):
        result = utils.strsToBools(list())
        assert isinstance(result, list)
        assert len(result) == 0

    def test_strToBools_withFalse(self):
        result = utils.strsToBools([ 'false' ])
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] is False

    def test_strToBools_withMixedList(self):
        result = utils.strsToBools([ 'false', 'f', 'true', 'FALSE', 'T', 'true', 'f' ])
        assert isinstance(result, list)
        assert len(result) == 7
        assert result[0] is False
        assert result[1] is False
        assert result[2] is True
        assert result[3] is False
        assert result[4] is True
        assert result[5] is True
        assert result[6] is False

    def test_strToBools_withNone(self):
        result = utils.strsToBools(None)
        assert isinstance(result, list)
        assert len(result) == 0

    def test_strToBools_withTrue(self):
        result = utils.strsToBools([ 'true' ])
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] is True
