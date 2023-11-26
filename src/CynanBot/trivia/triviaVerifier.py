from typing import Optional

import misc.utils as utils
from timber.timberInterface import TimberInterface
from trivia.absTriviaQuestion import AbsTriviaQuestion
from trivia.triviaBanHelperInterface import TriviaBanHelperInterface
from trivia.triviaContentCode import TriviaContentCode
from trivia.triviaContentScannerInterface import TriviaContentScannerInterface
from trivia.triviaFetchOptions import TriviaFetchOptions
from trivia.triviaHistoryRepositoryInterface import \
    TriviaHistoryRepositoryInterface
from trivia.triviaType import TriviaType
from trivia.triviaVerifierInterface import TriviaVerifierInterface


class TriviaVerifier(TriviaVerifierInterface):

    def __init__(
        self,
        timber: TimberInterface,
        triviaBanHelper: TriviaBanHelperInterface,
        triviaContentScanner: TriviaContentScannerInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaBanHelper, TriviaBanHelperInterface):
            raise ValueError(f'triviaBanHelper argument is malformed: \"{triviaBanHelper}\"')
        elif not isinstance(triviaContentScanner, TriviaContentScannerInterface):
            raise ValueError(f'triviaContentScanner argument is malformed: \"{triviaContentScanner}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface):
            raise ValueError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')

        self.__timber: TimberInterface = timber
        self.__triviaBanHelper: TriviaBanHelperInterface = triviaBanHelper
        self.__triviaContentScanner: TriviaContentScannerInterface = triviaContentScanner
        self.__triviaHistoryRepository: TriviaHistoryRepositoryInterface = triviaHistoryRepository

    async def checkContent(
        self,
        question: Optional[AbsTriviaQuestion],
        triviaFetchOptions: TriviaFetchOptions
    ) -> TriviaContentCode:
        if question is None:
            return TriviaContentCode.IS_NONE

        if not isinstance(question, AbsTriviaQuestion):
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise ValueError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

        if not triviaFetchOptions.areQuestionAnswerTriviaQuestionsEnabled() and question.getTriviaType() is TriviaType.QUESTION_ANSWER:
            self.__timber.log('TriviaVerifier', f'The given TriviaType is illegal: {question.getTriviaType()} (triviaFetchOptions: {triviaFetchOptions})')
            return TriviaContentCode.ILLEGAL_TRIVIA_TYPE
        elif triviaFetchOptions.requireQuestionAnswerTriviaQuestion() and question.getTriviaType() is not TriviaType.QUESTION_ANSWER:
            self.__timber.log('TriviaVerifier', f'The given TriviaType is illegal: {question.getTriviaType()} (triviaFetchOptions: {triviaFetchOptions})')
            return TriviaContentCode.ILLEGAL_TRIVIA_TYPE

        if await self.__triviaBanHelper.isBanned(
            triviaId = question.getTriviaId(),
            triviaSource = question.getTriviaSource()
        ):
            return TriviaContentCode.IS_BANNED

        contentScannerCode = await self.__triviaContentScanner.verify(question)
        if contentScannerCode is not TriviaContentCode.OK:
            return contentScannerCode

        return TriviaContentCode.OK

    async def checkHistory(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        triviaFetchOptions: TriviaFetchOptions
    ) -> TriviaContentCode:
        if not isinstance(question, AbsTriviaQuestion):
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        elif not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise ValueError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

        contentCode = await self.__triviaHistoryRepository.verify(
            question = question, 
            emote = emote,
            twitchChannel = triviaFetchOptions.getTwitchChannel()
        )

        if contentCode is not TriviaContentCode.OK:
            return contentCode

        return TriviaContentCode.OK
