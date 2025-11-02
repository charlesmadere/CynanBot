import pytest

from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.trivia.compilers.triviaAnswerCompiler import TriviaAnswerCompiler
from src.trivia.compilers.triviaAnswerCompilerInterface import TriviaAnswerCompilerInterface
from src.trivia.triviaExceptions import BadTriviaAnswerException


class TestTriviaAnswerCompiler:

    timber: TimberInterface = TimberStub()

    compiler: TriviaAnswerCompilerInterface = TriviaAnswerCompiler(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_compileBoolAnswer_withEmptyString(self):
        result: bool | None = None

        with pytest.raises(BadTriviaAnswerException):
            result = await self.compiler.compileBoolAnswer('')

        assert result is None

    @pytest.mark.asyncio
    async def test_compileBoolAnswer_withF(self):
        result = await self.compiler.compileBoolAnswer('f')
        assert result is False

    @pytest.mark.asyncio
    async def test_compileBoolAnswer_withFalse(self):
        result = await self.compiler.compileBoolAnswer('false')
        assert result is False

    @pytest.mark.asyncio
    async def test_compileBoolAnswer_withFalseAndWeirdUnicodeJunkBehindIt(self):
        result = await self.compiler.compileBoolAnswer('false\U000e0000')
        assert result is False

        result = await self.compiler.compileBoolAnswer('false \U000e0000')
        assert result is False

    @pytest.mark.asyncio
    async def test_compileBoolAnswer_withNewLineString(self):
        result: bool | None = None

        with pytest.raises(BadTriviaAnswerException):
            result = await self.compiler.compileBoolAnswer('\n')

        assert result is None

    @pytest.mark.asyncio
    async def test_compileBoolAnswer_withNone(self):
        result: bool | None = None

        with pytest.raises(BadTriviaAnswerException):
            result = await self.compiler.compileBoolAnswer(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_compileBoolAnswer_withWhitespaceString(self):
        result: bool | None = None

        with pytest.raises(BadTriviaAnswerException):
            result = await self.compiler.compileBoolAnswer(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_compileBoolAnswer_withT(self):
        result = await self.compiler.compileBoolAnswer('t')
        assert result is True

    @pytest.mark.asyncio
    async def test_compileBoolAnswer_withTrue(self):
        result = await self.compiler.compileBoolAnswer('true')
        assert result is True

    @pytest.mark.asyncio
    async def test_compileBoolAnswer_withTrueAndWeirdUnicodeJunkBehindIt(self):
        result = await self.compiler.compileBoolAnswer('true\U000e0000')
        assert result is True

        result = await self.compiler.compileBoolAnswer('true \U000e0000')
        assert result is True

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withA(self):
        result = await self.compiler.compileMultipleChoiceAnswer('A')
        assert result == 0

        result = await self.compiler.compileMultipleChoiceAnswer('a')
        assert result == 0

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withB(self):
        result = await self.compiler.compileMultipleChoiceAnswer('B')
        assert result == 1

        result = await self.compiler.compileMultipleChoiceAnswer('b')
        assert result == 1

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withBracedA(self):
        result = await self.compiler.compileMultipleChoiceAnswer('[A]')
        assert result == 0

        result = await self.compiler.compileMultipleChoiceAnswer('[a]')
        assert result == 0

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withBracedB(self):
        result = await self.compiler.compileMultipleChoiceAnswer('[B]')
        assert result == 1

        result = await self.compiler.compileMultipleChoiceAnswer('[b]')
        assert result == 1

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withBracedDigit(self):
        result: int | None = None

        with pytest.raises(Exception):
            result = await self.compiler.compileMultipleChoiceAnswer('[1]')

        assert result is None

        with pytest.raises(Exception):
            result = await self.compiler.compileMultipleChoiceAnswer('[0]')

        assert result is None

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withBracedWord(self):
        result: int | None = None

        with pytest.raises(Exception):
            result = await self.compiler.compileMultipleChoiceAnswer('[hello]')

        assert result is None

        with pytest.raises(Exception):
            result = await self.compiler.compileMultipleChoiceAnswer('[world]')

        assert result is None

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withC(self):
        result = await self.compiler.compileMultipleChoiceAnswer('C')
        assert result == 2

        result = await self.compiler.compileMultipleChoiceAnswer('c')
        assert result == 2

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withD(self):
        result = await self.compiler.compileMultipleChoiceAnswer('D')
        assert result == 3

        result = await self.compiler.compileMultipleChoiceAnswer('d')
        assert result == 3

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withDAndWeirdUnicodeJunkBehindIt(self):
        result = await self.compiler.compileMultipleChoiceAnswer('D\U000e0000')
        assert result == 3

        result = await self.compiler.compileMultipleChoiceAnswer('D \U000e0000')
        assert result == 3

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withDigit(self):
        result: int | None = None

        with pytest.raises(BadTriviaAnswerException):
            result = await self.compiler.compileMultipleChoiceAnswer('0')

        assert result is None

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withE(self):
        result = await self.compiler.compileMultipleChoiceAnswer('E')
        assert result == 4

        result = await self.compiler.compileMultipleChoiceAnswer('e')
        assert result == 4

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withEmptyBraces(self):
        result: int | None = None

        with pytest.raises(Exception):
            result = await self.compiler.compileMultipleChoiceAnswer('[]')

        assert result is None

        with pytest.raises(Exception):
            result = await self.compiler.compileMultipleChoiceAnswer('[]')

        assert result is None

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withF(self):
        result = await self.compiler.compileMultipleChoiceAnswer('F')
        assert result == 5

        result = await self.compiler.compileMultipleChoiceAnswer('f')
        assert result == 5

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withEmptyString(self):
        result: int | None = None

        with pytest.raises(BadTriviaAnswerException):
            result = await self.compiler.compileMultipleChoiceAnswer('')

        assert result is None

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withNone(self):
        result: int | None = None

        with pytest.raises(BadTriviaAnswerException):
            result = await self.compiler.compileMultipleChoiceAnswer(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withSymbol(self):
        result: int | None = None

        with pytest.raises(BadTriviaAnswerException):
            result = await self.compiler.compileMultipleChoiceAnswer('=')

        assert result is None

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withWhitespaceString(self):
        result: int | None = None

        with pytest.raises(BadTriviaAnswerException):
            result = await self.compiler.compileMultipleChoiceAnswer(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_compileMultipleChoiceAnswer_withZ(self):
        result = await self.compiler.compileMultipleChoiceAnswer('Z')
        assert result == 25

        result = await self.compiler.compileMultipleChoiceAnswer('z')
        assert result == 25

    @pytest.mark.asyncio
    async def test_compileTextAnswer_withAmpersand(self):
        result = await self.compiler.compileTextAnswer('Between the Buried & Me')
        assert result == 'between the buried and me'

    @pytest.mark.asyncio
    async def test_compileTextAnswer_withEmptyString(self):
        result = await self.compiler.compileTextAnswer('')
        assert result == ''

    @pytest.mark.asyncio
    async def test_compileTextAnswer_withHdDvd(self):
        result = await self.compiler.compileTextAnswer('HD-DVD')
        assert result == 'hd-dvd'

    @pytest.mark.asyncio
    async def test_compileTextAnswer_withHelloWorld(self):
        result = await self.compiler.compileTextAnswer('Hello, World!')
        assert result == 'hello world'

    @pytest.mark.asyncio
    async def test_compileTextAnswer_withNewLines(self):
        result = await self.compiler.compileTextAnswer('\nDream Theater\nOctavarium\n')
        assert result == 'dream theater octavarium'

    @pytest.mark.asyncio
    async def test_compileTextAnswer_withNone(self):
        result = await self.compiler.compileTextAnswer(None)
        assert result == ''

    @pytest.mark.asyncio
    async def test_compileTextAnswer_withPrefixA(self):
        result = await self.compiler.compileTextAnswer('A View from the Top of the World')
        assert result == 'view from the top of the world'

    @pytest.mark.asyncio
    async def test_compileTextAnswer_withPrefixAn(self):
        result = await self.compiler.compileTextAnswer('An Orange')
        assert result == 'orange'

    @pytest.mark.asyncio
    async def test_compileTextAnswer_withSaintNicholas(self):
        result = await self.compiler.compileTextAnswer('Saint Nicholas')
        assert result == 'saint nicholas'

    @pytest.mark.asyncio
    async def test_compileTextAnswer_withSirPeter(self):
        result = await self.compiler.compileTextAnswer('Sir Peter')
        assert result == 'sir peter'

    @pytest.mark.asyncio
    async def test_compileTextAnswer_withToRun(self):
        result = await self.compiler.compileTextAnswer('to run')
        assert result == 'run'

    @pytest.mark.asyncio
    async def test_compileTextAnswer_withUnderscoreWords(self):
        result = await self.compiler.compileTextAnswer('de_dust')
        assert result == 'de_dust'

    @pytest.mark.asyncio
    async def test_compileTextAnswer_withWhitespaceString(self):
        result = await self.compiler.compileTextAnswer(' ')
        assert result == ''

    @pytest.mark.asyncio
    async def test_compileTextAnswer_withZero(self):
        result = await self.compiler.compileTextAnswer('zero')
        assert result == 'zero'

    @pytest.mark.asyncio
    async def test_compileTextAnswer_with0(self):
        result = await self.compiler.compileTextAnswer('0')
        assert result == '0'

    @pytest.mark.asyncio
    async def test_compileTextAnswer_with1Second(self):
        result = await self.compiler.compileTextAnswer('1 second')
        assert result == '1 second'

    @pytest.mark.asyncio
    async def test_compileTextAnswer_with6MonthsOld(self):
        result = await self.compiler.compileTextAnswer('6 months old')
        assert result == '6 months old'

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withDuplicateWords(self):
        result = await self.compiler.compileTextAnswersList(['hello', 'Hello', 'HELLO', 'world', 'World', 'World!'])
        assert result is not None
        assert len(result) == 2
        assert 'hello' in result
        assert 'world' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withEddieVanHalen(self):
        result = await self.compiler.compileTextAnswersList(['(Eddie) Van Halen'])
        assert isinstance(result, list)
        assert len(result) == 2
        assert 'eddie van halen' in result
        assert 'van halen' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withEmptyList(self):
        result = await self.compiler.compileTextAnswersList(list())
        assert isinstance(result, list)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withGarfieldTheCat(self):
        result = await self.compiler.compileTextAnswersList(['Garfield the cat'])
        assert isinstance(result, list)
        assert len(result) == 2
        assert 'garfield the cat' in result
        assert 'garfield cat' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withGeorgeSchultz(self):
        result = await self.compiler.compileTextAnswersList(['George P. Schultz'])
        assert isinstance(result, list)
        assert len(result) == 2
        assert 'george p schultz' in result
        assert 'george schultz' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withGroanGrown(self):
        result = await self.compiler.compileTextAnswersList(['groan/grown'])
        assert isinstance(result, list)
        assert len(result) == 3
        assert 'groangrown' in result
        assert 'groan' in result
        assert 'grown' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withHash(self):
        result = await self.compiler.compileTextAnswersList(['mambo #5'])
        assert isinstance(result, list)
        assert len(result) == 2
        assert 'mambo number 5' in result
        assert 'mambo 5' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withHdDvd(self):
        result = await self.compiler.compileTextAnswersList(['HD-DVD'])
        assert isinstance(result, list)
        assert len(result) == 2
        assert 'hd dvd' in result
        assert 'hddvd' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withHeIsAVampire(self):
        result = await self.compiler.compileTextAnswersList(['he is a vampire'])
        assert isinstance(result, list)
        assert len(result) == 2
        assert 'he is a vampire' in result
        assert 'vampire' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withHesAVampire(self):
        result = await self.compiler.compileTextAnswersList(['he\'s a vampire'])
        assert isinstance(result, list)
        assert len(result) == 2
        assert 'hes a vampire' in result
        assert 'vampire' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withHelloWorldFoo(self):
        result = await self.compiler.compileTextAnswersList(['hello/world/foo'])
        assert isinstance(result, list)
        assert len(result) == 4
        assert 'helloworldfoo' in result
        assert 'hello' in result
        assert 'world' in result
        assert 'foo' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withHerPonytail(self):
        result = await self.compiler.compileTextAnswersList(['her ponytail'])
        assert result is not None
        assert len(result) == 2
        assert 'her ponytail' in result
        assert 'ponytail' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withHisCar(self):
        result = await self.compiler.compileTextAnswersList(['his car'])
        assert result is not None
        assert len(result) == 2
        assert 'his car' in result
        assert 'car' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withKurtVonnegutJr(self):
        result = await self.compiler.compileTextAnswersList(['(Kurt) Vonnegut (Jr.)'])
        assert result is not None
        assert len(result) == 4
        assert 'kurt vonnegut' in result
        assert 'kurt vonnegut jr' in result
        assert 'vonnegut' in result
        assert 'vonnegut jr' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withLuigiMarioJunior(self):
        result = await self.compiler.compileTextAnswersList(['Luigi M. Mario Jr.'])
        assert result is not None
        assert len(result) == 4
        assert 'luigi m mario jr' in result
        assert 'luigi m mario' in result
        assert 'luigi mario jr' in result
        assert 'luigi mario' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withMarioMarioSenior(self):
        result = await self.compiler.compileTextAnswersList(['Mario M Mario Senior'])
        assert result is not None
        assert len(result) == 4
        assert 'mario m mario senior' in result
        assert 'mario m mario' in result
        assert 'mario mario senior' in result
        assert 'mario mario' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withNone(self):
        result = await self.compiler.compileTextAnswersList(None)
        assert result is not None
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withNumberWord(self):
        result = await self.compiler.compileTextAnswersList(['three'])
        assert result is not None
        assert len(result) == 1
        assert 'three' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withNumberWords(self):
        result = await self.compiler.compileTextAnswersList(['one', 'two'])
        assert result is not None
        assert len(result) == 2
        assert 'one' in result
        assert 'two' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withOrdinalWord(self):
        result = await self.compiler.compileTextAnswersList(['third'])
        assert result is not None
        assert len(result) == 1
        assert 'third' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withOrdinalWords(self):
        result = await self.compiler.compileTextAnswersList(['first', 'second'])
        assert result is not None
        assert len(result) == 2
        assert 'first' in result
        assert 'second' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withPacificAnOcean(self):
        result = await self.compiler.compileTextAnswersList(['Pacific an ocean'])
        assert result is not None
        assert len(result) == 2
        assert 'pacific an ocean' in result
        assert 'pacific ocean' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withSparrballong(self):
        result = await self.compiler.compileTextAnswersList(['Spärrballong'])
        assert isinstance(result, list)
        assert len(result) == 1
        assert 'sparrballong' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withStephanFAustin(self):
        result = await self.compiler.compileTextAnswersList(['(Stephen F.) Austin III'])
        assert isinstance(result, list)
        assert len(result) == 8
        assert 'stephen f austin iii' in result
        assert 'stephen austin iii' in result
        assert 'stephen f austin' in result
        assert 'stephen austin' in result
        assert 'f austin iii' in result
        assert 'austin iii' in result
        assert 'f austin' in result
        assert 'austin' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withTheirHouse(self):
        result = await self.compiler.compileTextAnswersList(['their house'])
        assert result is not None
        assert len(result) == 2
        assert 'their house' in result
        assert 'house' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withTheyAreFriends(self):
        result = await self.compiler.compileTextAnswersList(['they are friends'])
        assert result is not None
        assert len(result) == 2
        assert 'they are friends' in result
        assert 'friends' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withTheyreFriends(self):
        result = await self.compiler.compileTextAnswersList(['they\'re friends'])
        assert result is not None
        assert len(result) == 2
        assert 'theyre friends' in result
        assert 'friends' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withUsDollar1(self):
        result = await self.compiler.compileTextAnswersList(['$12,456.70'])
        assert result is not None
        assert len(result) == 2
        assert '1245670 usd' in result
        assert '1245670' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withUsDollar2(self):
        result = await self.compiler.compileTextAnswersList(['$123 USD'])
        assert result is not None
        assert len(result) == 2
        assert '123 usd' in result
        assert '123' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withUsDollar3(self):
        result = await self.compiler.compileTextAnswersList(['$1 US'])
        assert result is not None
        assert len(result) == 2
        assert '1 usd' in result
        assert '1' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withUsDollar4(self):
        result = await self.compiler.compileTextAnswersList(['$1000000000.55 USD'])
        assert result is not None
        assert len(result) == 2
        assert '100000000055 usd' in result
        assert '100000000055' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withWalMart(self):
        result = await self.compiler.compileTextAnswersList(['Wal-Mart'])
        assert result is not None
        assert len(result) == 2
        assert 'wal mart' in result
        assert 'walmart' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withYourName(self):
        result = await self.compiler.compileTextAnswersList(['your name'])
        assert result is not None
        assert len(result) == 2
        assert 'your name' in result
        assert 'name' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_withZero(self):
        result = await self.compiler.compileTextAnswersList(['zero'])
        assert result is not None
        assert len(result) == 1
        assert 'zero' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_with0Hours(self):
        result = await self.compiler.compileTextAnswersList(['0 hours'])
        assert result is not None
        assert len(result) == 2
        assert '0 hours' in result
        assert '0' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_with2DividedBy3(self):
        result = await self.compiler.compileTextAnswersList(['2/3'])
        assert isinstance(result, list)
        assert len(result) == 1
        assert '2/3' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_with3MonthsOld(self):
        result = await self.compiler.compileTextAnswersList(['3 months old'])
        assert result is not None
        assert len(result) == 3
        assert '3 months old' in result
        assert '3 months' in result
        assert '3' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_with1Year(self):
        result = await self.compiler.compileTextAnswersList(['1 year'])
        assert result is not None
        assert len(result) == 2
        assert '1 year' in result
        assert '1' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_with1YearOld(self):
        result = await self.compiler.compileTextAnswersList(['1 year old'])
        assert result is not None
        assert len(result) == 3
        assert '1 year old' in result
        assert '1 year' in result
        assert '1' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_with5Years(self):
        result = await self.compiler.compileTextAnswersList(['5 years'])
        assert result is not None
        assert len(result) == 2
        assert '5 years' in result
        assert '5' in result

    @pytest.mark.asyncio
    async def test_compileTextAnswersList_with50YearsOld(self):
        result = await self.compiler.compileTextAnswersList(['50 years old'])
        assert isinstance(result, list)
        assert len(result) == 3
        assert '50 years old' in result
        assert '50 years' in result
        assert '50' in result

    @pytest.mark.asyncio
    async def test_expandNumerals_withRomanNumerals(self):
        result = await self.compiler.expandNumerals('XIV')
        assert result is not None
        assert len(result) == 4
        assert 'fourteen' in result  # cardinal, year
        assert 'fourteenth' in result  # ordinal
        assert 'the fourteenth' in result  # ordinal preceded by 'the'
        assert 'xiv' in result

    @pytest.mark.asyncio
    async def test_expandNumerals_withSimpleDigit1(self):
        result = await self.compiler.expandNumerals('3')
        assert result is not None
        assert len(result) == 3
        assert 'three' in result  # cardinal, year, individual digits
        assert 'third' in result  # ordinal
        assert 'the third' in result  # ordinal preceded by 'the'

    @pytest.mark.asyncio
    async def test_expandNumerals_withSimpleDigit2(self):
        result = await self.compiler.expandNumerals('50')
        assert isinstance(result, list)
        assert len(result) == 4
        assert 'fifty' in result # cardinal, year, individual digits
        assert 'five zero' in result # cardinal, year, individual digits
        assert 'fiftieth' in result # ordinal
        assert 'the fiftieth' in result # ordinal preceded by 'the'

    @pytest.mark.asyncio
    async def test_expandNumerals_withYear1(self):
        result = await self.compiler.expandNumerals('1234')
        assert isinstance(result, list)
        assert len(result) == 5
        assert 'one thousand two hundred and thirty four' in result # cardinal
        assert 'one thousand two hundred and thirty fourth' in result # ordinal
        assert 'the one thousand two hundred and thirty fourth' in result # ordinal preceded by 'the'
        assert 'twelve thirty four' in result # year
        assert 'one two three four' in result # individual digits

    def test_sanity(self):
        assert self.compiler is not None
        assert isinstance(self.compiler, TriviaAnswerCompiler)
        assert isinstance(self.compiler, TriviaAnswerCompilerInterface)
