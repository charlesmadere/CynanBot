import math
import re
import traceback
from typing import Any, Final, Generator, Pattern

import polyleven
from frozendict import frozendict

from .triviaAnswerCheckResult import TriviaAnswerCheckResult
from .triviaAnswerCheckerInterface import TriviaAnswerCheckerInterface
from ..compilers.triviaAnswerCompilerInterface import TriviaAnswerCompilerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.multipleChoiceTriviaQuestion import MultipleChoiceTriviaQuestion
from ..questions.questionAnswerTriviaQuestion import QuestionAnswerTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.trueFalseTriviaQuestion import TrueFalseTriviaQuestion
from ..settings.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from ..triviaExceptions import BadTriviaAnswerException, UnsupportedTriviaTypeException
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TriviaAnswerChecker(TriviaAnswerCheckerInterface):

    def __init__(
        self,
        timber: TimberInterface,
        triviaAnswerCompiler: TriviaAnswerCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaAnswerCompiler, TriviaAnswerCompilerInterface):
            raise TypeError(f'triviaAnswerCompiler argument is malformed: \"{triviaAnswerCompiler}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__triviaAnswerCompiler: Final[TriviaAnswerCompilerInterface] = triviaAnswerCompiler
        self.__triviaSettingsRepository: Final[TriviaSettingsRepositoryInterface] = triviaSettingsRepository

        self.__extraWhitespacePattern: Final[Pattern] = re.compile(r'\s{2,}', re.IGNORECASE)

        self.__irregularNouns: Final[frozendict[str, frozenset[str]]] = frozendict({
            'addendum': frozenset({ 'addenda', 'addendums' }),
            'alumna': frozenset({ 'alumnae' }),
            'bacterium': frozenset({ 'bacteria' }),
            'child': frozenset({ 'children' }),
            'deer': frozenset({ 'deer', 'deers' }),
            'die': frozenset({ 'dice' }),
            'fish': frozenset({ 'fish', 'fishes' }),
            'foot': frozenset({ 'feet' }),
            'goose': frozenset({ 'geese' }),
            'index': frozenset({ 'indexes', 'indices' }),
            'loaf': frozenset({ 'loaves' }),
            'man': frozenset({ 'men' }),
            'moose': frozenset({ 'moose' }),
            'mouse': frozenset({ 'mice' }),
            'person': frozenset({ 'people' }),
            'ox': frozenset({ 'ox', 'oxen' }),
            'scarf': frozenset({ 'scarfs', 'scarves' }),
            'self': frozenset({ 'selves' }),
            'tooth': frozenset({ 'teeth' }),
            'vertebra': frozenset({ 'vertebrae', 'vertebras' }),
            'wife': frozenset({ 'wives' }),
            'wolf': frozenset({ 'wolves' }),
            'woman': frozenset({ 'women' }),
        })

        self.__stopWords: Final[frozenset[str]] = frozenset({
            'i', 'me', 'my', 'myself', 'we', 'ourselves', 'you', 'he', 'him', 'his', 'she', 'they', 'them',
            'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were',
            'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the',
            'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
            'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
            'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
            'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'some',
            'such', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just',
            'dont', 'should', 'now',
        })

    async def checkAnswer(
        self,
        answer: str | None,
        triviaQuestion: AbsTriviaQuestion,
        extras: dict[str, Any] | None = None,
    ) -> TriviaAnswerCheckResult:
        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')

        if not utils.isValidStr(answer):
            return TriviaAnswerCheckResult.INVALID_INPUT

        if isinstance(triviaQuestion, MultipleChoiceTriviaQuestion):
            return await self.__checkAnswerMultipleChoice(
                answer = answer,
                triviaQuestion = triviaQuestion,
            )

        elif isinstance(triviaQuestion, QuestionAnswerTriviaQuestion):
            return await self.__checkAnswerQuestionAnswer(
                answer = answer,
                triviaQuestion = triviaQuestion,
                extras = extras,
            )

        elif isinstance(triviaQuestion, TrueFalseTriviaQuestion):
            return await self.__checkAnswerTrueFalse(
                answer = answer,
                triviaQuestion = triviaQuestion,
            )

        else:
            raise UnsupportedTriviaTypeException(f'Unsupported TriviaType: \"{triviaQuestion.triviaType}\"')

    async def __checkAnswerMultipleChoice(
        self,
        answer: str | None,
        triviaQuestion: MultipleChoiceTriviaQuestion
    ) -> TriviaAnswerCheckResult:
        if not isinstance(triviaQuestion, MultipleChoiceTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif triviaQuestion.triviaType is not TriviaQuestionType.MULTIPLE_CHOICE:
            raise ValueError(f'TriviaType is not {TriviaQuestionType.MULTIPLE_CHOICE}: \"{triviaQuestion.triviaType}\"')

        answerIndex: int | None = None

        try:
            answerIndex = await self.__triviaAnswerCompiler.compileMultipleChoiceAnswer(answer)
        except BadTriviaAnswerException as e:
            self.__timber.log('TriviaAnswerChecker', f'Unable to convert multiple choice answer to ordinal: ({answer=}): {e}', e, traceback.format_exc())
            return TriviaAnswerCheckResult.INVALID_INPUT

        if not utils.isValidInt(answerIndex):
            # this should be impossible at this point, but let's just check anyway
            self.__timber.log('TriviaAnswerChecker', f'Unable to convert multiple choice answer to ordinal: ({answer=}) ({answerIndex=})')
            return TriviaAnswerCheckResult.INVALID_INPUT

        if answerIndex < 0 or answerIndex >= triviaQuestion.responseCount:
            # Checks for a scenario where the user guessed an answer outside the range
            # of actual responses. For example, the user might have guessed F, but the
            # question only had up to D.
            self.__timber.log('TriviaAnswerChecker', f'Multiple choice answer ordinal is outside the range of actual answer ordinals: ({answer=}) ({answerIndex=}) ({triviaQuestion.responseCount=})')
            return TriviaAnswerCheckResult.INVALID_INPUT

        if answerIndex in triviaQuestion.indexesWithCorrectAnswers.keys():
            return TriviaAnswerCheckResult.CORRECT
        else:
            return TriviaAnswerCheckResult.INCORRECT

    async def __checkAnswerQuestionAnswer(
        self,
        answer: str | None,
        triviaQuestion: QuestionAnswerTriviaQuestion,
        extras: dict[str, Any] | None = None,
    ) -> TriviaAnswerCheckResult:
        if not isinstance(triviaQuestion, QuestionAnswerTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif triviaQuestion.triviaType is not TriviaQuestionType.QUESTION_ANSWER:
            raise ValueError(f'TriviaType is not {TriviaQuestionType.QUESTION_ANSWER}: \"{triviaQuestion.triviaType}\"')

        # prevent potential for insane answer lengths
        maxPhraseGuessLength = await self.__triviaSettingsRepository.getMaxPhraseGuessLength()
        if utils.isValidStr(answer) and len(answer) > maxPhraseGuessLength:
            answer = answer[0:maxPhraseGuessLength].strip()

        compiledUserAnswers = await self.__triviaAnswerCompiler.compileTextAnswersList(
            answers = [ answer ],
            allWords = triviaQuestion.allWords,
            expandParentheses = False,
        )

        if not all(utils.isValidStr(cleanedAnswer) for cleanedAnswer in compiledUserAnswers):
            return TriviaAnswerCheckResult.INCORRECT

        compiledCorrectAnswers = triviaQuestion.compiledCorrectAnswers
        self.__timber.log('TriviaAnswerChecker', f'In depth question/answer debug information — ({answer=}) ({compiledUserAnswers=}) ({triviaQuestion.correctAnswers=}) ({compiledCorrectAnswers=}) ({extras=})')

        for compiledCorrectAnswer in compiledCorrectAnswers:
            for compiledUserAnswer in compiledUserAnswers:
                expandedUserAnswers = await self.__triviaAnswerCompiler.expandNumerals(compiledUserAnswer)

                for expandedUserAnswer in expandedUserAnswers:
                    if expandedUserAnswer == compiledCorrectAnswer:
                        return TriviaAnswerCheckResult.CORRECT

                    guessWords = self.__extraWhitespacePattern.sub(' ', expandedUserAnswer).split(' ')
                    answerWords = self.__extraWhitespacePattern.sub(' ', compiledCorrectAnswer).split(' ')
                    minWords = min(len(guessWords), len(answerWords))

                    for gWords in self.__mergeWords(guessWords, minWords):
                        for aWords in self.__mergeWords(answerWords, minWords):
                            # This expansion of all() is required because you can't perform list comprehension on async
                            #   generators yet. :(
                            valid = True
                            for i in range(len(gWords)):
                                if not await self.__compareWords(gWords[i], aWords[i]):
                                    valid = False
                                    break
                            if valid:
                                return TriviaAnswerCheckResult.CORRECT

        return TriviaAnswerCheckResult.INCORRECT

    async def __checkAnswerTrueFalse(
        self,
        answer: str | None,
        triviaQuestion: TrueFalseTriviaQuestion
    ) -> TriviaAnswerCheckResult:
        if not isinstance(triviaQuestion, TrueFalseTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif triviaQuestion.triviaType is not TriviaQuestionType.TRUE_FALSE:
            raise ValueError(f'TriviaType is not {TriviaQuestionType.TRUE_FALSE}: \"{triviaQuestion.triviaType}\"')

        answerBool: bool | None = None

        try:
            answerBool = await self.__triviaAnswerCompiler.compileBoolAnswer(answer)
        except BadTriviaAnswerException as e:
            self.__timber.log('TriviaAnswerChecker', f'Unable to convert true false answer to bool: ({answer=}): {e}', e, traceback.format_exc())
            return TriviaAnswerCheckResult.INVALID_INPUT

        if answerBool == triviaQuestion.correctAnswer:
            return TriviaAnswerCheckResult.CORRECT
        else:
            return TriviaAnswerCheckResult.INCORRECT

    # generates all possible groupings of the given words such that the resulting word count is target_length
    # example: words = ["a", "b", "c", "d"], target_length = 2
    #          generates ["abc", "d"], ["ab", "cd"], ["a", "bcd"]
    def __mergeWords(
        self,
        wordList: list[str],
        targetLength: int,
    ) -> Generator[list[str], None, None]:
        if targetLength == 1:
            yield [''.join(wordList)]
        elif len(wordList) <= targetLength:
            yield wordList
        else:
            for i in range(len(wordList) - targetLength + 1):
                for w in self.__mergeWords(wordList[i + 1:], targetLength - 1):
                    yield [''.join(wordList[0:i + 1])] + w

    # compare two individual words, returns true if any valid variants match between the two words
    async def __compareWords(
        self,
        word1: str,
        word2: str,
    ) -> bool:
        thresholdGrowthRate = await self.__triviaSettingsRepository.getLevenshteinThresholdGrowthRate()

        for w1 in self.__genVariantPossibilities(word1):
            if not utils.isValidStr(w1):
                continue

            for w2 in self.__genVariantPossibilities(word2):
                if not utils.isValidStr(w2):
                    continue

                # calculate threshold based on shorter word length
                threshold = math.floor(min(len(w1), len(w2)) / thresholdGrowthRate)
                distance = polyleven.levenshtein(w1, w2, threshold + 1)
                if distance <= threshold:
                    return True

        return False

    def __genVariantPossibilities(self, word: str) -> Generator[str, None, None]:
        yield word

        # don't preprocess stopwords
        if word in self.__stopWords:
            return

        # pluralizations
        if any(word.endswith(s) for s in { 'ss', 'sh', 'ch', 'x', 'z', 's', 'o' }):
            yield word + 'es'
        if word[-1] in 'sz':
            yield word + word[-1] + 'es'
        elif word.endswith('f'):
            yield word[:-1] + 'ves'
        elif word.endswith('fe'):
            yield word[:-2] + 'ves'
        elif word[-1] == 'y' and len(word) > 1 and word[-2] not in 'aeiou':
            yield word[:-1] + 'ies'
        elif word.endswith('us'):
            yield word[:-2] + 'i'
        elif word.endswith('is'):
            yield word[:-2] + 'es'
        elif word.endswith('on') or word.endswith('um'):
            yield word[:-2] + 'a'
        elif word.endswith('ism'):
            yield word[:-3]
        if word[-1] != 's':
            yield word + 's'

        if word in self.__irregularNouns:
            for irregularNoun in self.__irregularNouns[word]:
                yield irregularNoun

        # titles
        if word == 'atty':
            yield 'attorney'
        if word == 'do':
            yield 'doctor of osteopathy'
        if word == 'dr':
            yield 'doctor'
        if word == 'esq':
            yield 'esquire'
        if word == 'jr':
            yield 'junior'
        if word == 'md':
            yield 'doctor of medicine'
        if word == 'mr':
            yield 'mister'
        if word == 'mrs':
            yield 'missus'
        if word == 'ms':
            yield 'miss'
        if word == 'np':
            yield 'nurse practitioner'
        if word == 'pa':
            yield 'physician assistant'
        if word == 'phd':
            yield 'philosophiae doctor'
        if word == 'sr':
            yield 'senior'
        if word == 'st':
            yield 'saint'

        # common names and nicknames
        if word == 'trey':
            yield '3rd'
        if word in { 'ivy', 'iv' }:
            yield '4th'
        if word in { 'quince', 'quint' }:
            yield '5th'
        if word in { 'erin', 'ron', 'ronnie' }:
            yield 'aaron'
        if word in { 'ab', 'abe', 'eb', 'ebbie' }:
            yield 'abel'
        if word in { 'a.b.', 'ab', 'biah' }:
            yield 'abiah'
            yield 'abijah'
        if word in { 'biel', 'ab' }:
            yield 'abiel'
        if word in { 'abby', 'nabby', 'gail' }:
            yield 'abigail'
        if word == 'ab':
            yield 'abner'
        if word in { 'abe', 'abram' }:
            yield 'abraham'
        if word in { 'ada', 'addy', 'dell', 'delia', 'lena' }:
            yield 'adaline'
            yield 'adeline'
        if word in { 'ad', 'ade' }:
            yield 'adam'
        if word in { 'addy', 'adele', 'dell', 'della', 'heidi' }:
            yield 'adelaide'
        if word in { 'adele', 'addy', 'dell', 'delphia', 'philly' }:
            yield 'adelphia'
        if word in { 'aggy', 'inez', 'nessa' }:
            yield 'agatha'
            yield 'agnes'
        if word in { 'allie', 'lena' }:
            yield 'aileen'
        if word in { 'al', 'alan', 'allan', 'alen', 'allen', 'lonson' }:
            yield 'alan'
            yield 'alanson'
            yield 'allen'
        if word in { 'allie', 'bert', 'bertie' }:
            yield 'alberta'
        if word in { 'alberta', 'bert', 'berta', 'bertie', 'del', 'delbert', 'elbert' }:
            yield 'albert'
            yield 'adelbert'
        if word in { 'al', 'rich', 'richie' }:
            yield 'aldrich'
        if word in { 'alex', 'al', 'eleck', 'sandy' }:
            yield 'alexander'
        if word in { 'alex', 'alla', 'sandy' }:
            yield 'alexandra'
        if word in { 'al', 'fred' }:
            yield 'alfred'
        if word in { 'alfy', 'freda', 'freddy', 'frieda' }:
            yield 'alfreda'
        if word in { 'allie', 'elsie', 'lisa' }:
            yield 'alice'
            yield 'alicia'
        if word in { 'allie', 'mandy' }:
            yield 'almena'
        if word in { 'al', 'lon', 'lonzo' }:
            yield 'alonzo'
        if word == 'al':
            yield 'alvin'
        if word in { 'manda', 'mandy' }:
            yield 'amanda'
        if word in { 'emily', 'mel', 'millie', 'amy' }:
            yield 'amelia'
        if word in { 'am', 'brose' }:
            yield 'ambrose'
        if word == 'am':
            yield 'amos'
        if word in { 'ander', 'andersen', 'andy', 'sonny' }:
            yield 'anderson'
        if word in { 'andy', 'drew' }:
            yield 'andrew'
        if word in { 'annette', 'annie', 'antoinette', 'nan', 'nanny', 'nana', 'nancy' }:
            yield 'ann'
            yield 'anne'
        if word in { 'ann', 'tony', 'netta' }:
            yield 'antoinette'
            yield 'antonia'
        if word in { 'ara', 'arry', 'belle', 'bella' }:
            yield 'arabella'
            yield 'arabelle'
        if word == 'archie':
            yield 'archibald'
        if word == 'arnie':
            yield 'arnold'
        if word in { 'art', 'artie' }:
            yield 'arthur'
        if word in { 'august', 'austin', 'gus', 'gussie' }:
            yield 'augustine'
            yield 'augustus'
        if word in { 'bab', 'babs', 'barby', 'bobbie' }:
            yield 'barbara'
        if word in { 'barney', 'barnie', 'barns' }:
            yield 'barnabas'
        if word in { 'bart', 'bartel', 'bat', 'mees', 'meus' }:
            yield 'bartholomew'
        if word in { 'bea', 'trisha', 'trix', 'trixie' }:
            yield 'beatrice'
        if word in { 'ben', 'benjy', 'bennie', 'benny', 'jamie' }:
            yield 'benjamin'
        if word in { 'ben', 'bernie' }:
            yield 'bernard'
        if word in { 'bert', 'bertie', 'birdie' }:
            yield 'bertha'
        if word in { 'bert', 'bertie' }:
            yield 'bertram'
        if word in { 'billie', 'billy' }:
            yield 'bill'
        if word == 'brad':
            yield 'bradford'
        if word in { 'cal', 'cale' }:
            yield 'caleb'
        if word in { 'cathleen', 'katherine', 'kathleen', 'kathy' }:
            yield 'catherine'
        if word in { 'caeser', 'ceasar', 'ceaser' }:
            yield 'caesar'
        if word in { 'carl', 'chad', 'charlie', 'charly', 'chuck', 'chucky' }:
            yield 'charles'
        if word in { 'char', 'lottie', 'lotta', 'sherry' }:
            yield 'charlotte'
        if word == 'chet':
            yield 'chester'
        if word in { 'chris', 'christ', 'cris', 'kit', 'kris' }:
            yield 'christian'
            yield 'christopher'
        if word in { 'claire', 'clare' }:
            yield 'clair'
            yield 'clarence'
        if word == 'claudie':
            yield 'claude'
        if word == 'clem':
            yield 'clement'
        if word in { 'clif', 'cliff', 'cliffy', 'ford' }:
            yield 'clifford'
        if word in { 'con', 'connie', 'cornie', 'neel' }:
            yield 'cornelius'
        if word == 'cy':
            yield 'cyrus'
        if word in { 'dan', 'danny' }:
            yield 'daniel'
        if word in { 'dave', 'davey', 'day' }:
            yield 'david'
        if word in { 'debbie', 'debby', 'debora', 'devorah' }:
            yield 'deborah'
        if word == 'delanor':
            yield 'delano'
        if word == 'denny':
            yield 'dennis'
        if word in { 'dom', 'nick' }:
            yield 'dominic'
        if word in { 'don', 'donny' }:
            yield 'donald'
        if word == 'doug':
            yield 'douglas'
        if word in { 'ed', 'edd', 'eddie', 'eddward', 'eddy', 'ned', 'ted', 'teddy' }:
            yield 'edward'
            yield 'edwin'
        if word in { 'elli', 'ellie', 'lee', 'lie' }:
            yield 'eli'
        if word in { 'eli', 'lige', 'lish' }:
            yield 'elijah'
        if word in { 'eli', 'lish' }:
            yield 'elisha'
        if word in { 'eliza', 'bess', 'bessie', 'beth', 'betsy', 'betty', 'lib', 'libby', 'liz', 'liza', 'lisa', 'liz', 'lizzie' }:
            yield 'elizabeth'
        if word in { 'eli', 'elliot', 'lee' }:
            yield 'elliot'
        if word in { 'manuel', 'manny', 'man' }:
            yield 'emmanuel'
        if word == 'em':
            yield 'emory'
        if word in { 'eph', 'ephie', 'ephy' }:
            yield 'ephraim'
        if word == 'gene':
            yield 'eugene'
        if word in { 'aron', 'aaron', 'aaryn', 'eryn' }:
            yield 'erin'
        if word in { 'ez', 'ezzy' }:
            yield 'ezra'
        if word in { 'lix', 'lixie' }:
            yield 'felix'
        if word == 'fdr':
            yield 'franklin roosevelt'
            yield 'franklin delano roosevelt'
        if word in { 'fred', 'frankie', 'fran', 'frannie' }:
            yield 'ferdinand'
        if word in { 'fran', 'frances', 'frank', 'frankie' }:
            yield 'francis'
            yield 'franklin'
        if word in { 'fred', 'freddy', 'fritz', 'rick', 'derick' }:
            yield 'frederick'
        if word == 'gabe':
            yield 'gabriel'
        if word in { 'goerge', 'geordie', 'georgie' }:
            yield 'george'
        if word == 'gw':
            yield 'george washington'
        if word in { 'gerry', 'jerry' }:
            yield 'gerald'
        if word in { 'gil', 'bert', 'bertie' }:
            yield 'gilbert'
        if word in { 'gordie', 'gordo' }:
            yield 'gordon'
        if word in { 'greg', 'gregg' }:
            yield 'gregory'
        if word in { 'hal', 'harry' }:
            yield 'harold'
        if word in { 'ella', 'ellen', 'ellie', 'lena' }:
            yield 'helen'
            yield 'helene'
        if word in { 'hal', 'hank', 'harry' }:
            yield 'henry'
        if word in { 'herb', 'bert', 'herbie', 'bertie' }:
            yield 'herbert'
        if word in { 'herm', 'hermie' }:
            yield 'herman'
        if word in { 'hop', 'hopp' }:
            yield 'hopkins'
        if word == 'race':
            yield 'horace'
        if word in { 'hugh', 'bert', 'hub' }:
            yield 'hubert'
        if word in { 'hughie', 'hew' }:
            yield 'hugh'
        if word in { 'igg', 'iggy', 'nace', 'nate', 'natius' }:
            yield 'ignatius'
        if word in { 'ike', 'isac', 'zeke' }:
            yield 'isaac'
        if word in { 'sy', 'zay' }:
            yield 'isaiah'
        if word in { 'jakob', 'jake', 'jay', 'coby' }:
            yield 'jacob'
        if word in { 'jim', 'jimmy', 'jamie' }:
            yield 'james'
        if word == 'jarvie':
            yield 'jarvis'
        if word in { 'jace', 'jay' }:
            yield 'jason'
        if word in { 'jed', 'jeddo', 'dyah' }:
            yield 'jedediah'
        if word in { 'jerry', 'jeremy' }:
            yield 'jeremiah'
        if word in { 'jen', 'jenn', 'jenny' }:
            yield 'jennifer'
        if word in { 'jess', 'jesse', 'jessika', 'jessy' }:
            yield 'jessica'
        if word == 'jfk':
            yield 'john fitzgerald kennedy'
            yield 'john kennedy'
        if word in { 'jo', 'joe', 'joey', 'josef', 'joseph', 'josephine','joey', 'josey' }:
            yield 'joe'
            yield 'joel'
            yield 'joseph'
        if word in { 'jack', 'jock', 'jon', 'jhon', 'johnny', 'jhonny', 'jonny' }:
            yield 'john'
            yield 'johnathan'
        if word in { 'jos', 'joshua' }:
            yield 'josh'
        if word in { 'josh', 'jos' }:
            yield 'joshua'
        if word in { 'si', 'siah' }:
            yield 'josiah'
        if word in { 'jude', 'judy' }:
            yield 'judah'
        if word in { 'jule', 'jules' }:
            yield 'julian'
        if word in { 'ken', 'kenny', 'kendall', 'kendrick' }:
            yield 'kenneth'
        if word in { 'larry', 'lawrie' }:
            yield 'lawrence'
        if word in { 'leo', 'leon', 'len', 'lenny', 'lineau' }:
            yield 'leonard'
        if word in { 'leo', 'polde' }:
            yield 'leopold'
        if word == 'roy':
            yield 'leroy'
        if word in { 'lou', 'louie', 'lewis' }:
            yield 'louis'
            yield 'lewis'
        if word in { 'mal', 'ky', 'chi' }:
            yield 'malachi'
        if word in { 'mannie', 'manny', 'manu' }:
            yield 'manuel'
        if word in { 'marta', 'marty', 'mat', 'mattie', 'patsy', 'patty' }:
            yield 'martha'
            yield 'martin'
        if word in { 'molly', 'polly', 'mae', 'mamie', 'mitzi' }:
            yield 'mary'
        if word in { 'matt', 'matty' }:
            yield 'matthew'
        if word in { 'linda', 'lindy', 'mel', 'mindy' }:
            yield 'melinda'
        if word in { 'lisa', 'lissa', 'mel', 'milly', 'missy' }:
            yield 'melissa'
        if word in { 'micheal', 'mike' }:
            yield 'michael'
        if word in { 'milt', 'miltie' }:
            yield 'milton'
        if word in { 'mose', 'moss' }:
            yield 'moses'
        if word in { 'nat', 'nate', 'nathan', 'natty', 'than' }:
            yield 'nathaniel'
        if word in { 'claas', 'claes', 'nicolas', 'nick', 'nicky', 'klaus' }:
            yield 'nicholas'
        if word in { 'noa', 'noe' }:
            yield 'noah'
        if word in { 'olie', 'ollie', 'noll' }:
            yield 'oliver'
        if word in { 'ossy', 'ozzie', 'ozzy', 'waldo' }:
            yield 'oswald'
            yield 'oscar'
        if word in { 'paddy', 'pat', 'pate', 'patsy', 'peter' }:
            yield 'patrick'
        if word in { 'paulie', 'pol' }:
            yield 'paul'
        if word == 'perry':
            yield 'pelegrine'
        if word in { 'pate', 'pete', 'petey' }:
            yield 'peter'
        if word in { 'filip', 'fillip', 'fillipe', 'phil', 'phili', 'philli', 'philip' }:
            yield 'phillip'
        if word in { 'scott', 'scotty', 'pres' }:
            yield 'prescott'
        if word == 'ralph':
            yield 'raphael'
        if word == 'rafe':
            yield 'ralph'
        if word in { 'ray', 'raymie' 'remy' }:
            yield 'raymond'
        if word in { 'reba', 'becca', 'becky', 'beck' }:
            yield 'rebecca'
        if word in { 'rube' }:
            yield 'reuben'
        if word in { 'dick', 'rich', 'rick', 'rickey', 'rickie', 'ricky' }:
            yield 'richard'
        if word in { 'rfk' }:
            yield 'robert francis kennedy'
            yield 'robert kennedy'
        if word in { 'bob', 'bobby', 'rob', 'robb', 'robbie', 'robby', 'roberto', 'robin', 'rupert' }:
            yield 'robert'
        if word in { 'ron', 'ronaldo', 'ronnie' }:
            yield 'ronald'
        if word in { 'sam', 'sammy' }:
            yield 'samuel'
        if word in { 'sadie', 'sally', 'sara' }:
            yield 'sarah'
        if word == 'sol':
            yield 'saul'
        if word in { 'bastian', 'seb', 'sebby', 'bast' }:
            yield 'sebastian'
        if word in { 'si', 'sy', 'sylas' }:
            yield 'silas'
        if word in { 'sol', 'solly' 'sully' }:
            yield 'solomon'
        if word in { 'steph', 'stephan', 'steven', 'stevenson', 'stevie' }:
            yield 'steve'
            yield 'stephen'
            yield 'steven'
        if word in { 'si', 'sly', 'sy', 'syl', 'vester', 'vet', 'vessie' }:
            yield 'sylvester'
        if word in { 'terry' }:
            yield 'terence'
        if word in { 'theo', 'ted', 'teddy' }:
            yield 'theodore'
        if word in { 'terry', 'tess', 'tessie', 'tessa', 'thirza', 'thursa', 'tracy' }:
            yield 'theresa'
        if word in { 'tim', 'timmy' }:
            yield 'timothy'
        if word in { 'thom', 'tom', 'tommy', 'tony' }:
            yield 'thomas'
        if word == 'toby':
            yield 'tobias'
        if word in { 'anthony', 'toni' }:
            yield 'tony'
        if word == 'ulie':
            yield 'ulysses'
        if word in { 'nessa', 'essa', 'vanna' }:
            yield 'vanessa'
        if word in { 'franky', 'frony', 'ron', 'ronna', 'ronnie', 'vonnie' }:
            yield 'veronica'
        if word in { 'vic', 'vicky', 'vickie' }:
            yield 'victoria'
            yield 'vic'
        if word in { 'vin', 'vince', 'vinny' }:
            yield 'vincent'
        if word in { 'walt', 'wally' }:
            yield 'walter'
        if word in { 'will', 'willie', 'fred', 'willy' }:
            yield 'wilfred'
            yield 'wilbur'
        if word in { 'william', 'willie', 'willy', 'billy', 'bill', 'bell', 'bela' }:
            yield 'will'
            yield 'william'
            yield 'bill'
        if word in { 'winnie', 'winny' }:
            yield 'winifred'
        if word in { 'zach', 'zachy' }:
            yield 'zachariah'
        if word == 'zeb':
            yield 'zebedee'
        if word in { 'diah', 'dyer', 'zed' }:
            yield 'zedediah'
        if word == 'zeke':
            yield 'ezekiel'

        # geographical features/streets
        if word in { 'aly', 'ally' }:
            yield 'alley'
        if word in { 'anx', 'annex', 'annx' }:
            yield 'anex'
        if word == 'arc':
            yield 'arcade'
        if word in { 'av', 'ave', 'avn' }:
            yield 'avenue'
        if word == 'bch':
            yield 'beach'
        if word in { 'blvd', 'boul' }:
            yield 'boulevard'
        if word in { 'br', 'brnch' }:
            yield 'branch'
        if word == 'brg':
            yield 'bridge'
        if word == 'brk':
            yield 'brook'
        if word == 'byu':
            yield 'bayou'
        if word in { 'canyn', 'cnyn' }:
            yield 'canyon'
        if word == 'cswy':
            yield 'causeway'
        if word in { 'cen', 'cntr', 'ctr' }:
            yield 'center'
        if word in { 'cir', 'cir', 'circl', 'crcl' }:
            yield 'circle'
        if word == 'clb':
            yield 'club'
        if word == 'cty':
            yield 'city'
        if word in { 'ct', 'cts', 'crt', 'crts' }:
            yield 'court'
            yield 'courts'
        if word == 'cv':
            yield 'cove'
        if word == 'crk':
            yield 'creek'
        if word == 'dr':
            yield 'drive'
        if word == 'est':
            yield 'estate'
        if word == 'fld':
            yield 'field'
        if word == 'frd':
            yield 'ford'
        if word in { 'frt', 'ft' }:
            yield 'fort'
        if word == 'gdn':
            yield 'garden'
        if word == 'glf':
            yield 'gulf'
        if word == 'grn':
            yield 'green'
        if word == 'grv':
            yield 'grove'
        if word == 'hvn':
            yield 'haven'
        if word in { 'ht', 'hgt', 'hts' }:
            yield 'height'
        if word in { 'hiwy', 'hiway', 'hway', 'hwy' }:
            yield 'highway'
        if word in { 'is', 'isl', 'isle' }:
            yield 'island'
        if word in { 'ldg', 'ldge' }:
            yield 'lodge'
        if word == 'lk':
            yield 'lake'
        if word == 'ln':
            yield 'lane'
        if word == 'mdw':
            yield 'meadow'
        if word == 'mnr':
            yield 'manor'
        if word == 'mt':
            yield 'mount'
            yield 'mountain'
        if word == 'mtwy':
            yield 'motorway'
        if word == 'orch':
            yield 'orchard'
        if word in { 'pkwy', 'pkway', 'pky' }:
            yield 'parkway'
        if word == 'pl':
            yield 'place'
        if word == 'px':
            yield 'post exchange'
        if word == 'rd':
            yield 'road'
        if word in { 'riv', 'rvr', 'rivr' }:
            yield 'river'
        if word == 'rd':
            yield 'road'
        if word == 'sq':
            yield 'square'
        if word in { 'st', 'str', 'strt' }:
            yield 'street'
        if word == 'stn':
            yield 'station'
        if word == 'vlg':
            yield 'village'
        if word == 'vw':
            yield 'view'
        if word in { 'crssng', 'xing' }:
            yield 'crossing'

        # countries, languages, and specific places
        if word == 'asl':
            yield 'american sign language'
        if word == 'antigua':
            yield 'antigua and barbuda'
        if word == 'arctic':
            yield 'arctic ocean'
        if word == 'atlantic':
            yield 'atlantic ocean'
        if word == 'bosnia':
            yield 'bosnia and herzegovina'
        if word == 'burma':
            yield 'myanmar'
        if word == 'cape verde':
            yield 'cabo verde'
        if word == 'car':
            yield 'central african republic'
        if word in { 'czechia republic', 'czech republic' }:
            yield 'czechia'
        if word == 'dr':
            yield 'dominican republic'
        if word == 'drc':
            yield 'democratic republic of congo'
            yield 'democratic republic of the congo'
        if word in { 'en', 'eng' }:
            yield 'english'
        if word in { 'euro', 'eu' }:
            yield 'europe'
            yield 'european union'
        if word == 'gb':
            yield 'great britain'
        if word == 'holland':
            yield 'netherlands'
        if word == 'indian':
            yield 'indian ocean'
        if word == 'ivory coast':
            yield 'cote d ivoire'
            yield 'cote divoire'
        if word in { 'ja', 'jap', 'japon', 'jp', 'jpn', 'nihon', 'nippon' }:
            yield 'japan'
        if word == 'kr':
            yield 'korea'
        if word in { 'macedonia', 'n macedonia' }:
            yield 'macedonia'
            yield 'north macedonia'
        if word == 'mx':
            yield 'mexico'
        if word == 'myanmar':
            yield 'burma'
        if word == 'new guinea':
            yield 'papua new guinea'
        if word in { 'ny', 'new york city', 'nyc' }:
            yield 'new york'
        if word == 'pacific':
            yield 'pacific ocean'
        if word in { 'palestine state', 'palestinian', 'palestinian state', 'west bank', 'w bank' }:
            yield 'palestine'
        if word == 'pr':
            yield 'puerto rico'
        if word in { 'rep', 'repr' }:
            yield 'representative'
        if word == 'sen':
            yield 'senator'
        if word == 'swaziland':
            yield 'eswatini'
        if word in { 'timor', 'east timor' }:
            yield 'timor leste'
        if word == 'turkiye':
            yield 'turkey'
        if word == 'uae':
            yield 'united arab emirates'
        if word == 'uk':
            yield 'united kingdom'
        if word == 'un':
            yield 'united nations'
        if word in { 'america', 'us', 'usa' }:
            yield 'america'
            yield 'united states'
            yield 'united states america'
            yield 'united states of america'
        if word in { 'russia', 'russian', 'soviet', 'soviets', 'ussr' }:
            yield 'russia'
            yield 'soviet union'

        # government organizations
        if word == 'cia':
            yield 'central intelligence agency'
        if word in { 'dem', 'democratic', 'democratic party', 'dnc', 'democratic national convention', 'liberal' }:
            yield 'democrat'
        if word == 'fbi':
            yield 'federal bureau of investigation'
        if word in { 'fedex', 'fed ex' }:
            yield 'federal express'
        if word in { 'conservative', 'gop', 'grand old party', 'republican party', 'rnc', 'republican national convention' }:
            yield 'republican'
        if word == 'irs':
            yield 'internal revenue service'
        if word == 'mi6':
            yield 'secret intelligence service'
        if word == 'nsa':
            yield 'natural security agency'
        if word in { 'post', 'usps' }:
            yield 'mail'
            yield 'post'
            yield 'post office'
            yield 'postal service'
            yield 'united states postal service'
        if word == 'sec':
            yield 'securities and exchange commission'
        if word == 'tsa':
            yield 'transportation security administration'
        if word == 'ups':
            yield 'united parcel service'

        # currencies
        if word == 'eur':
            yield 'euro'
        if word == 'jpy':
            yield 'japanese yen'
            yield 'yen'
        if word == 'sek':
            yield 'krona'
            yield 'swedish krona'
        if word == 'usd':
            yield 'dollar'
            yield 'united states dollar'

        # sports
        if word == 'asl':
            yield 'american soccer league'
        if word == 'cfl':
            yield 'canadian football league'
        if word == 'fifa':
            yield 'federation internationale de football association'
        if word == 'ko':
            yield 'knock out'
        if word == 'mlb':
            yield 'major league baseball'
        if word == 'mls':
            yield 'major league soccer'
        if word == 'nba':
            yield 'national basketball association'
        if word == 'nfl':
            yield 'national football league'
        if word in { 'nhl', 'wnhl' }:
            yield 'national hockey league'

        # directions
        if word in { 'n', 'north', 'northerly', 'northern' }:
            yield 'north'
        if word in { 's', 'south', 'southerly', 'southern' }:
            yield 'south'
        if word in { 'e', 'east', 'easterly', 'eastern' }:
            yield 'east'
        if word in { 'w', 'west', 'westerly', 'western' }:
            yield 'west'
        if word in { 'nw', 'northwest', 'northwestern' }:
            yield 'northwest'
        if word in { 'ne', 'northeast', 'northeastern' }:
            yield 'northeast'
        if word in { 'sw', 'southwest', 'southwestern' }:
            yield 'southwest'
        if word in { 'se', 'southeast', 'southeastern' }:
            yield 'southeast'
        if word in { 'l', 'left', 'lft' }:
            yield 'left'
        if word in { 'r', 'right', 'rite' }:
            yield 'right'

        # corporation things
        if word == 'asst':
            yield 'assistant'
        if word == 'ceo':
            yield 'chief executive officer'
        if word == 'coo':
            yield 'chief operating officer'
        if word == 'corp':
            yield 'corporation'
        if word == 'inc':
            yield 'incorporated'
        if word == 'llc':
            yield 'limited liability company'
        if word == 'ltd':
            yield 'limited'
        if word == 'vp':
            yield 'vice president'

        # weird latin things
        if word == 'cv':
            yield 'curriculum vitae'
        if word == 'et al':
            yield 'et alia'
        if word == 'etc':
            yield 'et cetera'
        if word == 'eg':
            yield 'example gratia'
            yield 'exempli gratia'
        if word == 'ie':
            yield 'id est'
            yield 'in other words'
        if word == 'ps':
            yield 'postscript'
            yield 'postscriptum'
        if word == 'sic':
            yield 'sic erat scriptum'

        # technology
        if word == 'cd':
            yield 'compact disc'
        if word == 'cmyk':
            yield 'cyan magenta yellow black'
        if word in { 'comp', 'laptop', 'pc' }:
            yield 'computer'
        if word == 'cpu':
            yield 'central processing unit'
            yield 'processor'
        if word == 'ddr':
            yield 'data delivery rate'
        if word == 'disk':
            yield 'disc'
        if word == 'dns':
            yield 'domain name system'
        if word in { 'dp', 'dip' }:
            yield 'density independent pixel'
        if word == 'dpi':
            yield 'dots per inch'
        if word == 'dvd':
            yield 'digital versatile disc'
            yield 'digital video disc'
        if word == 'ff':
            yield 'firefox'
        if word == 'float':
            yield 'floating point'
        if word == 'fps':
            yield 'frames per second'
        if word == 'ftp':
            yield 'file transfer protocol'
        if word in { 'goog', 'googl' }:
            yield 'google'
        if word == 'gps':
            yield 'global positioning system'
        if word == 'gpu':
            yield 'graphics processing unit'
        if word == 'hd':
            yield 'high definition'
        if word in { 'hd', 'hdd' }:
            yield 'hard disk drive'
            yield 'hard drive'
        if word in { 'http', 'https' }:
            yield 'hypertext transfer protocol'
            yield 'hypertext transfer protocol secure'
        if word == 'ie':
            yield 'internet explorer'
        if word == 'int':
            yield 'integer'
        if word == 'ip':
            yield 'internet protocol'
        if word in { 'ms', 'msft' }:
            yield 'microsoft'
        if word in { 'net', 'network' }:
            yield 'internet'
        if word == 'op':
            yield 'operand'
            yield 'operation'
        if word == 'os':
            yield 'operating system'
        if word == 'pc':
            yield 'personal computer'
        if word == 'ppi':
            yield 'pixels per inch'
        if word == 'pt':
            yield 'point'
        if word in { 'px', 'pxl' }:
            yield 'pixel'
            yield 'pixels'
        if word == 'ram':
            yield 'random access memory'
        if word == 'rgb':
            yield 'red green blue'
        if word == 'rgbs':
            yield 'red green blue sync'
        if word == 'sd':
            yield 'standard definition'
        if word == 'sec':
            yield 'security'
        if word == 'sftp':
            yield 'secure file transfer protocol'
        if word == 'sp':
            yield 'scaleable pixels'
            yield 'scale independent pixels'
        if word == 'ssd':
            yield 'solid state drive'
        if word == 'txt':
            yield 'text'
        if word == 'uri':
            yield 'uniform resource identifier'
        if word == 'url':
            yield 'uniform resource locator'
        if word == 'vhs':
            yield 'video home system'
        if word == 'www':
            yield 'internet'
            yield 'web'
            yield 'world wide web'

        # units and measurements (imperial and metric)
        if word == 'atm':
            yield 'atmospheres'
        if word == 'bin':
            yield 'binary'
        if word == 'bps':
            yield 'bits per second'
        if word in { 'c', 'centigrade' }:
            yield 'celsius'
        if word == 'cg':
            yield 'centigram'
        if word == 'cl':
            yield 'centiliter'
        if word == 'cm':
            yield 'centimeter'
        if word == 'cpm':
            yield 'cost per thousand'
        if word == 'dl':
            yield 'deciliter'
        if word == 'dm':
            yield 'decimeter'
        if word == 'eb':
            yield 'exabyte'
        if word == 'f':
            yield 'fahrenheit'
        if word == 'fps':
            yield 'feet per second'
        if word == 'ft':
            yield 'feet'
            yield 'foot'
        if word == 'g':
            yield 'gallon'
            yield 'gram'
        if word == 'gb':
            yield 'gigabyte'
        if word == 'gph':
            yield 'gallons per hour'
        if word == 'gw':
            yield 'gigawatt'
        if word == 'hg':
            yield 'hectogram'
        if word == 'hm':
            yield 'hectometer'
        if word == 'hr':
            yield 'hour'
        if word == 'in':
            yield 'inch'
            yield 'inches'
        if word == 'k':
            yield 'kelvin'
        if word == 'kb':
            yield 'kilobyte'
        if word == 'kg':
            yield 'kilogram'
        if word == 'kl':
            yield 'kiloliter'
            yield 'kiloliters'
        if word == 'km':
            yield 'kilometer'
            yield 'kilometers'
        if word == 'kph':
            yield 'kilometers per hour'
        if word == 'kw':
            yield 'kilowatt'
        if word == 'kwh':
            yield 'kilowatt hours'
        if word == 'l':
            yield 'liter'
            yield 'liters'
        if word == 'lat':
            yield 'latitude'
        if word in { 'lb', 'lbs' }:
            yield 'pound'
            yield 'pounds'
        if word in { 'lon', 'long' }:
            yield 'longitude'
        if word == 'm':
            yield 'meter'
            yield 'minute'
        if word == 'max':
            yield 'maximum'
        if word == 'mb':
            yield 'megabyte'
            yield 'megabytes'
        if word == 'mg':
            yield 'milligram'
            yield 'milligrams'
        if word == 'mi':
            yield 'mile'
            yield 'miles'
        if word == 'min':
            yield 'minimum'
            yield 'minute'
            yield 'minutes'
        if word == 'ml':
            yield 'milliliter'
        if word == 'mm':
            yield 'millimeter'
        if word == 'mpg':
            yield 'miles per gallon'
        if word == 'mph':
            yield 'miles per hour'
        if word == 'mps':
            yield 'meters per second'
        if word == 'nmi':
            yield 'nautical miles'
        if word == 'oz':
            yield 'ounce'
            yield 'ounces'
        if word == 'pb':
            yield 'petabyte'
            yield 'petabytes'
        if word == 's':
            yield 'second'
        if word == 'tb':
            yield 'terabyte'
            yield 'terabytes'
        if word in { 'tbs', 'tbsp' }:
            yield 'tablespoon'
            yield 'tablespoons'
        if word == 'tsp':
            yield 'teaspoon'
            yield 'teaspoons'
        if word == 'w':
            yield 'watt'
            yield 'wattage'
        if word in { 'yd', 'yds', 'yrd', 'yrds' }:
            yield 'yard'

        # british english vs american english spellings
        if word == 'aluminium':
            yield 'aluminum'
        if word == 'analogue':
            yield 'analog'
        if word == 'analyse':
            yield 'analyze'
        if word == 'armour':
            yield 'armor'
        if word == 'catalogue':
            yield 'catalog'
        if word == 'colour':
            yield 'color'
        if word == 'defence':
            yield 'defense'
        if word == 'dialogue':
            yield 'dialog'
        if word == 'flavour':
            yield 'flavor'
        if word == 'flouride':
            yield 'fluoride'
        if word == 'labour':
            yield 'labor'
        if word == 'licence':
            yield 'license'
        if word == 'neighbour':
            yield 'neighbor'
        if word == 'offence':
            yield 'offense'
        if word == 'travelled':
            yield 'traveled'
        if word == 'traveller':
            yield 'traveler'
        if word == 'travelling':
            yield 'traveling'

        # days of the week
        if word == 'mon':
            yield 'monday'
        if word in { 'tue', 'tues' }:
            yield 'tuesday'
        if word in { 'wed', 'weds' }:
            yield 'wednesday'
        if word in { 'thrs', 'thur', 'thurs' }:
            yield 'thursday'
        if word == 'fri':
            yield 'friday'
        if word == 'sat':
            yield 'saturday'
        if word == 'sun':
            yield 'sunday'
        if word == 'holiday':
            yield 'day'

        # months of the year
        if word == 'jan':
            yield 'january'
        if word == 'feb':
            yield 'february'
        if word == 'mar':
            yield 'march'
        if word == 'apr':
            yield 'april'
        if word == 'jun':
            yield 'june'
        if word in { 'jul', 'jly' }:
            yield 'july'
        if word == 'aug':
            yield 'august'
        if word in { 'sep', 'sept' }:
            yield 'september'
        if word == 'nov':
            yield 'november'
        if word == 'dec':
            yield 'december'

        # commonly misspelled words
        if word in { 'absense', 'abcense', 'abcence' }:
            yield 'absence'
        if word == 'accidently':
            yield 'accidentally'
        if word in { 'accomodate', 'acommodate', 'accommadate' }:
            yield 'accommodate'
        if word in { 'acheive', 'acheeve' }:
            yield 'achieve'
        if word in { 'amatuer', 'amature' }:
            yield 'amateur'
        if word == 'anice':
            yield 'anise'
        if word == 'aquire':
            yield 'acquire'
        if word == 'aquit':
            yield 'acquit'
        if word == 'athiest':
            yield 'atheist'
        if word == 'basicly':
            yield 'basically'
        if word in { 'brocolli', 'broccolli' }:
            yield 'broccoli'
        if word == 'calender':
            yield 'calendar'
        if word in { 'cemetary', 'cematery', 'cematary' }:
            yield 'cemetery'
        if word in { 'colum', 'columm' }:
            yield 'column'
        if word in { 'comittee', 'commitee' }:
            yield 'committee'
        if word == 'concensus':
            yield 'consensus'
        if word in { 'definate', 'definately' }:
            yield 'definite'
            yield 'definitely'
        if word in { 'enterpreneur', 'entrepeneur', 'entreperneur', 'entreprenur' }:
            yield 'entrepreneur'
        if word in { 'gage', 'guage' }:
            yield 'gauge'
        if word in { 'garauntee', 'gaurantee' }:
            yield 'guarantee'
        if word == 'heigth':
            yield 'height'
        if word in { 'itinary', 'itinery' }:
            yield 'itinerary'
        if word == 'layed':
            yield 'laid'
        if word in { 'manoover', 'menoover', 'meneuver' }:
            yield 'maneuver'
        if word == 'mispell':
            yield 'misspell'
        if word in { 'ocassion', 'occassion' }:
            yield 'occasion'
        if word in { 'plagarism', 'plagarize' }:
            yield 'plagiarism'
            yield 'plagiarize'
        if word == 'publically':
            yield 'publicly'
        if word == 'recieve':
            yield 'receive'
        if word in { 'separate', 'seprate', 'seperet' }:
            yield 'separate'
        if word in { 'temperture', 'tempreture', 'temprature', 'temparature' }:
            yield 'temperature'
        if word in { 'tommorow', 'tommorrow' }:
            yield 'tomorrow'
        if word == 'untill':
            yield 'until'
        if word in { 'vaccum', 'vaccuum', 'vaccuumm' }:
            yield 'vacuum'
        if word == 'weigth':
            yield 'weight'
        if word == 'withold':
            yield 'withhold'
        if word in { 'zuccini', 'zuchinni', 'zuccinni' }:
            yield 'zucchini'

        # cutesy alternative spellings
        if word == 'alt':
            yield 'alternative'
        if word == 'hi':
            yield 'high'
        if word == 'lil':
            yield 'little'
        if word == 'lite':
            yield 'light'
        if word == 'lo':
            yield 'low'
        if word == 'mid':
            yield 'middle'
        if word in { 'ad', 'an', 'n', '&', '+' }:
            yield 'and'
        if word in { 'pow', 'powr', 'pwr' }:
            yield 'power'

        # other
        if word == 'ac':
            yield 'air condition'
            yield 'air conditioner'
            yield 'air conditioning'
            yield 'alternating current'
        if word == 'accel':
            yield 'accelerate'
            yield 'acceleration'
        if word == 'alright':
            yield 'all right'
        if word == 'anime':
            yield 'animated'
            yield 'animation'
        if word == 'auto':
            yield 'automate'
            yield 'automated'
            yield 'automatic'
        if word == 'bday':
            yield 'birthday'
        if word == 'bunny':
            yield 'rabbit'
        if word in { 'cmd', 'com', 'comm' }:
            yield 'command'
            yield 'commander'
        if word == 'cnn':
            yield 'cable news network'
        if word == 'ctrl':
            yield 'control'
        if word == 'dad':
            yield 'father'
        if word == 'decel':
            yield 'decelerate'
            yield 'deceleration'
        if word == 'dna':
            yield 'deoxyribonucleic acid'
        if word == 'est':
            yield 'establish'
            yield 'established'
            yield 'estimate'
        if word == 'capital':
            yield 'capitol'
        if word == 'co':
            yield 'commanding officer'
        if word in { 'csar', 'tsar', 'tzar' }:
            yield 'czar'
        if word == 'dc':
            yield 'direct current'
        if word == 'deg':
            yield 'degrees'
        if word in { 'dep', 'dpt', 'dept' }:
            yield 'department'
        if word == 'drop':
            yield 'droplet'
        if word == 'espn':
            yield 'entertainment and sports programming network'
        if word == 'est':
            yield 'estimate'
            yield 'estimated'
            yield 'established'
        if word == 'eta':
            yield 'estimated time of arrival'
        if word == 'fi':
            yield 'fiction'
        if word == 'fl':
            yield 'floor'
        if word == 'fridge':
            yield 'refrigerator'
        if word == 'ft':
            yield 'feature'
            yield 'featuring'
        if word == 'fyi':
            yield 'for your information'
        if word == 'gen':
            yield 'generate'
            yield 'generation'
            yield 'generator'
        if word == 'grey':
            yield 'gray'
        if word == 'lang':
            yield 'language'
        if word == 'mom':
            yield 'mother'
        if word == 'no':
            yield 'number'
        if word == 'ocd':
            yield 'obsessive compulsive disorder'
        if word == 'parcel':
            yield 'delivery'
            yield 'mail'
            yield 'package'
        if word in { 'cell', 'mobile', 'phone', 'tel' }:
            yield 'telephone'
        if word == 'pkmn':
            yield 'pokemon'
        if word == 'poli':
            yield 'politic'
            yield 'political'
            yield 'politician'
        if word in { 'precedent', 'presedent' }:
            yield 'president'
        if word == 'raised':
            yield 'risen'
            yield 'rose'
        if word == 'rna':
            yield 'ribonucleic acid'
        if word == 'sci':
            yield 'science'
        if word == 'scifi':
            yield 'science fiction'
        if word in { 'temp', 'tmp' }:
            yield 'temperature'
            yield 'temporary'
        if word == 'tv':
            yield 'television'
        if word == 'vs':
            yield 'versus'
        if word in { 'married', 'wed', 'wedd', 'wedding' }:
            yield 'marriage'
        if word == 'wr':
            yield 'world record'
        if word == 'ww':
            yield 'world war'
        if word in { 'wwi', 'ww1', 'first world war' }:
            yield 'world war 1'
        if word in { 'wwii', 'ww2', 'second world war' }:
            yield 'world war 2'
        if word == 'xmas':
            yield 'christmas'
