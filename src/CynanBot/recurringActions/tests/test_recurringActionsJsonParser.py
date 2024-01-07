import json
from typing import Dict

import pytest

from CynanBot.language.languagesRepository import LanguagesRepository
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.recurringActions.recurringActionsJsonParser import \
    RecurringActionsJsonParser
from CynanBot.recurringActions.recurringActionsJsonParserInterface import \
    RecurringActionsJsonParserInterface
from CynanBot.recurringActions.superTriviaRecurringAction import \
    SuperTriviaRecurringAction


class TestRecurringActionsJsonParser():

    languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()

    parser: RecurringActionsJsonParserInterface = RecurringActionsJsonParser(
        languagesRepository = languagesRepository
    )

    @pytest.mark.asyncio
    async def test_toJson_withSuperTriviaAction(self):
        action = SuperTriviaRecurringAction(
            enabled = True,
            twitchChannel = 'smCharles'
        )

        jsonString = await self.parser.toJson(action)
        assert isinstance(jsonString, str)
        assert len(jsonString) != 0
        assert not jsonString.isspace()

        jsonObject = json.loads(jsonString)
        assert isinstance(jsonObject, Dict)
        assert len(jsonObject) == 0
