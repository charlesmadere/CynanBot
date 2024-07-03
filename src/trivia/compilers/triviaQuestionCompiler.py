import html
import re
from typing import Collection, Pattern

from ...timber.timberInterface import TimberInterface
from .triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from ...misc import utils as utils


class TriviaQuestionCompiler(TriviaQuestionCompilerInterface):

    """_summary_

    This class is used for improving human readability of trivia question strings. The
    output from this class is NOT intended to be used for the actual processing/evaluating
    part of trivia questions.
    """

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

        self.__ellipsisRegEx: Pattern = re.compile(r'(\.){3,}', re.IGNORECASE)
        self.__newLineRegEx: Pattern = re.compile(r'(\n)+', re.IGNORECASE)
        self.__tagRemovalRegEx: Pattern = re.compile(r'[<\[]\/?\w+[>\]]', re.IGNORECASE)
        self.__underscoreRegEx: Pattern = re.compile(r'_{2,}', re.IGNORECASE)
        self.__weirdEllipsisRegEx: Pattern = re.compile(r'\.\s\.\s\.', re.IGNORECASE)
        self.__whiteSpaceRegEx: Pattern = re.compile(r'\s{2,}', re.IGNORECASE)

        self.__textReplacements: dict[str, str | None] = {
            'the ukraine': 'Ukraine',
        }

    async def compileCategory(
        self,
        category: str | None,
        htmlUnescape: bool = False
    ) -> str:
        if category is not None and not isinstance(category, str):
            raise TypeError(f'category argument is malformed: \"{category}\"')
        elif not utils.isValidBool(htmlUnescape):
            raise TypeError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')

        return await self.__compileText(
            text = category,
            htmlUnescape = htmlUnescape
        )

    async def compileQuestion(
        self,
        question: str | None,
        htmlUnescape: bool = False
    ) -> str:
        if question is not None and not isinstance(question, str):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidBool(htmlUnescape):
            raise TypeError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')

        return await self.__compileText(
            text = question,
            htmlUnescape = htmlUnescape
        )

    async def compileResponse(
        self,
        response: str | None,
        htmlUnescape: bool = False
    ) -> str:
        if response is not None and not isinstance(response, str):
            raise TypeError(f'response argument is malformed: \"{response}\"')
        elif not utils.isValidBool(htmlUnescape):
            raise TypeError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')

        return await self.__compileText(
            text = response,
            htmlUnescape = htmlUnescape
        )

    async def compileResponses(
        self,
        responses: Collection[str | None] | None,
        htmlUnescape: bool = False
    ) -> list[str]:
        if responses is not None and not isinstance(responses, Collection):
            raise TypeError(f'responses argument is malformed: \"{responses}\"')
        elif not utils.isValidBool(htmlUnescape):
            raise TypeError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')

        if responses is None or len(responses) == 0:
            return list()

        compiledResponses: set[str] = set()

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
        text: str | None,
        htmlUnescape: bool
    ) -> str:
        if text is not None and not isinstance(text, str):
            raise TypeError(f'text argument is malformed: \"{text}\"')
        elif not utils.isValidBool(htmlUnescape):
            raise TypeError(f'htmlUnescape argument is malformed: \"{htmlUnescape}\"')

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
