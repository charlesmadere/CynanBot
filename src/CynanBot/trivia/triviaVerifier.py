from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.banned.triviaBanHelperInterface import \
    TriviaBanHelperInterface
from CynanBot.trivia.content.triviaContentCode import TriviaContentCode
from CynanBot.trivia.content.triviaContentScannerInterface import \
    TriviaContentScannerInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaHistoryRepositoryInterface import \
    TriviaHistoryRepositoryInterface
from CynanBot.trivia.triviaVerifierInterface import TriviaVerifierInterface


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

        if not triviaFetchOptions.areQuestionAnswerTriviaQuestionsEnabled() and question.getTriviaType() is TriviaQuestionType.QUESTION_ANSWER:
            self.__timber.log('TriviaVerifier', f'The given TriviaType is illegal: {question.getTriviaType()} (triviaFetchOptions: {triviaFetchOptions})')
            return TriviaContentCode.ILLEGAL_TRIVIA_TYPE
        elif triviaFetchOptions.requireQuestionAnswerTriviaQuestion() and question.getTriviaType() is not TriviaQuestionType.QUESTION_ANSWER:
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
