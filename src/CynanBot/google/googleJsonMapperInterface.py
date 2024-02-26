from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from CynanBot.google.googleTranslateTextGlossaryConfig import \
    GoogleTranslateTextGlossaryConfig
from CynanBot.google.googleTranslateTextResponse import \
    GoogleTranslateTextResponse
from CynanBot.google.googleTranslation import GoogleTranslation


class GoogleJsonMapperInterface(ABC):

    @abstractmethod
    async def parseTranslateTextGlossaryConfig(
        self,
        jsonContents: Optional[Dict[str, Any]]
    ) -> Optional[GoogleTranslateTextGlossaryConfig]:
        pass

    @abstractmethod
    async def parseTranslateTextResponse(
        self,
        jsonContents: Optional[Dict[str, Any]]
    ) -> Optional[GoogleTranslateTextResponse]:
        pass

    @abstractmethod
    async def parseTranslation(
        self,
        jsonContents: Optional[Dict[str, Any]]
    ) -> Optional[GoogleTranslation]:
        pass
