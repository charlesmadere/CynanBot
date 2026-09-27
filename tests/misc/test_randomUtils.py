import math
import re
from typing import Final, Pattern

from src.misc.randomUtils import RandomUtils
from src.misc.randomUtilsInterface import RandomUtilsInterface


class TestRandomUtils:

    randomUtils: Final[RandomUtilsInterface] = RandomUtils()

    uuidRegEx: Final[Pattern] = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)

    def test_bool(self):
        for _ in range(100):
            randomBool = self.randomUtils.bool()
            assert isinstance(randomBool, bool)

    def test_float(self):
        for _ in range(100):
            randomFloat = self.randomUtils.float()
            assert isinstance(randomFloat, float)
            assert math.isfinite(randomFloat)
            assert randomFloat >= float(0)
            assert randomFloat <= float(1)

    def test_sanity(self):
        assert self.randomUtils is not None
        assert isinstance(self.randomUtils, RandomUtils)
        assert isinstance(self.randomUtils, RandomUtilsInterface)

    def test_uuid(self):
        for _ in range(100):
            randomUuid = self.randomUtils.uuid()
            assert isinstance(randomUuid, str)
            assert not randomUuid.isspace()
            assert len(randomUuid) > 0
            assert self.uuidRegEx.fullmatch(randomUuid) is not None
