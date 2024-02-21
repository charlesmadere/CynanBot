import html
import re
from typing import Collection, Dict, List, Optional, Pattern, Set

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.compilers.triviaQuestionCompilerInterface import \
    TriviaQuestionCompilerInterface


class TriviaQuestionCompiler(TriviaQuestionCompilerInterface):

    """_summary_

    This class is used for improving human readability of trivia question strings. The
    output from this class is NOT intended to be used for the actual processing/evaluating
    part of trivia questions.
    """

    def __init__(self, timber: TimberInterface):
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"

        self.__timber: TimberInterface = timber

        self.__ellipsisRegEx: Pattern = re.compile(r'(\.){3,}', re.IGNORECASE)
        self.__newLineRegEx: Pattern = re.compile(r'(\n)+', re.IGNORECASE)
        self.__tagRemovalRegEx: Pattern = re.compile(r'[<\[]\/?\w+[>\]]', re.IGNORECASE)
        self.__underscoreRegEx: Pattern = re.compile(r'_{2,}', re.IGNORECASE)
        self.__weirdEllipsisRegEx: Pattern = re.compile(r'\.\s\.\s\.', re.IGNORECASE)
        self.__whiteSpaceRegEx: Pattern = re.compile(r'\s{2,}', re.IGNORECASE)

        self.__textReplacements: Dict[str, Optional[str]] = {
            'the ukraine': 'Ukraine',
        }

    async def compileCategory(
        self,
        category: Optional[str],
        htmlUnescape: bool = False
    ) -> str:
        assert category is None or isinstance(category, str), f"malformed {category=}"
        if not utils.isValidBool(htmlUnescape):
            raise ValueError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')

        return await self.__compileText(
            text = category,
            htmlUnescape = htmlUnescape
        )

    async def compileQuestion(
        self,
        question: Optional[str],
        htmlUnescape: bool = False
    ) -> str:
        assert question is None or isinstance(question, str), f"malformed {question=}"
        if not utils.isValidBool(htmlUnescape):
            raise ValueError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')

        return await self.__compileText(
            text = question,
            htmlUnescape = htmlUnescape
        )

    async def compileResponse(
        self,
        response: Optional[str],
        htmlUnescape: bool = False
    ) -> str:
        assert response is None or isinstance(response, str), f"malformed {response=}"
        if not utils.isValidBool(htmlUnescape):
            raise ValueError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')

        return await self.__compileText(
            text = response,
            htmlUnescape = htmlUnescape
        )

    async def compileResponses(
        self,
        responses: Optional[Collection[Optional[str]]],
        htmlUnescape: bool = False
    ) -> List[str]:
        if not utils.isValidBool(htmlUnescape):
            raise ValueError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')

        if not utils.hasItems(responses):
            return list()

        compiledResponses: Set[str] = set()

        for response in responses:
            compiledResponse = await self.compileResponse(
                response = response,
                htmlUnescape = htmlUnescape
            )

            if utils.isValidStr(compiledResponse):
                compiledResponses.add(compiledResponse)

        return list(compiledResponses)

    async def __compileText(
        self,
        text: Optional[str],
        htmlUnescape: bool
    ) -> str:
        assert text is None or isinstance(text, str), f"malformed {text=}"
        if not utils.isValidBool(htmlUnescape):
            raise ValueError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')

        if not utils.isValidStr(text):
            return ''

        text = text.strip()

        # replaces all "dot dot dot" sequences with the ellipsis character: "…"
        text = self.__ellipsisRegEx.sub('…', text).strip()

        # replaces all "dot space dot space dot" sequences with the ellipsis character
        text = self.__weirdEllipsisRegEx.sub('…', text).strip()

        # replaces all new line characters with 1 space
        text = self.__newLineRegEx.sub(' ', text).strip()

        # removes HTML tag-like junk
        text = self.__tagRemovalRegEx.sub('', text).strip()

        # replaces sequences of underscores (2 or more) with 3 underscores
        text = self.__underscoreRegEx.sub('___', text).strip()

        # replaces sequences of whitespace (2 or more) with 1 space
        text = self.__whiteSpaceRegEx.sub(' ', text).strip()

        if htmlUnescape:
            text = html.unescape(text).strip()

        replacement = self.__textReplacements.get(text.lower(), None)

        if utils.isValidStr(replacement):
            self.__timber.log('TriviaQuestionCompiler', f'Found replacement text for \"{text}\": \"{replacement}\"')
            return replacement
        elif utils.isValidStr(text):
            return text
        else:
            return ''
