from abc import ABC, abstractmethod
from collections import abc
from enum import Enum
import typing

import pytest

from CynanBot.misc.type_check import type_check


def test_no_params() -> None:
    """ don't know why you'd do this, but it shouldn't break """

    @type_check
    def f() -> None:
        pass

    f()


def test_bad_name_kwarg() -> None:

    @type_check
    def f() -> None:
        pass

    with pytest.raises(TypeError):
        f(x=3)  # type: ignore


def test_too_many_arg() -> None:

    @type_check
    def f() -> None:
        pass

    with pytest.raises(TypeError):
        f("3")  # type: ignore


def test_int_for_float() -> None:
    """ int should be accepted when param is float """

    @type_check
    def f(x: float) -> None:
        pass

    f(42)
    f(2.2)


def test_float_for_int() -> None:
    """ float should not be accepted where int is required """

    @type_check
    def f(x: int) -> None:
        pass

    f(7)

    with pytest.raises(TypeError):
        f(9.9)  # type: ignore


def test_int_for_opt_float() -> None:

    @type_check
    def f(x: float | None) -> None:
        pass

    f(42)
    f(3.14)
    f(None)


def test_float_for_opt_int() -> None:
    """ float should not be accepted where int | None is required """

    @type_check
    def f(x: int | None) -> None:
        pass

    with pytest.raises(TypeError):
        f(9.9)  # type: ignore


def test_none_union() -> None:

    @type_check
    def f(x: str | None) -> str:
        return f"{x}"

    f("hello")
    f(None)

    with pytest.raises(TypeError):
        f(1.1)  # type: ignore


def test_none_alone() -> None:
    """ don't know why you would want to do this, but shouldn't break """

    @type_check
    def f(x: None) -> int:
        return 3

    f(None)

    with pytest.raises(TypeError):
        f([])  # type: ignore


def test_typing_generic() -> None:

    @type_check
    def f(x: typing.Iterable[str]) -> str | None:
        return "abc"

    f("abc")  # This is still a headache.
    f(frozenset({"a", "b", "c"}))
    f({"x": 3, "y": 4, "z": None})
    f(list())

    with pytest.raises(TypeError):
        # checks every item to make sure it's str
        f(["a", "b", b"c"])  # type: ignore

    with pytest.raises(TypeError):
        # iterable but not giving str
        f(b"abc")  # type: ignore


def test_abc_generic() -> None:

    @type_check
    def f(x: abc.Sequence[float]) -> str | None:
        return "abc"

    f([1.0, 2.0, 3.0])
    f(())
    f((3,))
    f(b"abc")

    with pytest.raises(TypeError):
        f("abc")  # type: ignore

    with pytest.raises(TypeError):
        f(8.3)  # type: ignore


def test_builtin_generic() -> None:

    @type_check
    def f(x: dict[str, dict[bytes, int | None]]) -> str | None:
        return "abc"

    f({})
    f({
        "a": {
            b"x": 5,
            b"y": 8,
            b"z": None
        },
        "b": {}
    })

    with pytest.raises(TypeError):
        f(3)  # type: ignore

    with pytest.raises(TypeError):
        f({"a"})  # type: ignore

    with pytest.raises(TypeError):
        f({
            "a": {
                b"x": 5,
                b"y": 8.2,  # type: ignore
                b"z": None
            },
            "b": {}
        })

    with pytest.raises(TypeError):
        f({
            "a": {
                b"x": 5,
                b"y": 8,
                "z": None  # type: ignore
            },
            "b": {}
        })


def test_non_iterable_generic() -> None:
    """ only implementations of `Iterable` and `Mapping` work """

    with pytest.raises(TypeError):
        @type_check
        def f(y: abc.Container[str]) -> typing.Literal["f"]:
            return "f"


def test_literal() -> None:
    """ This could probably be implemented. But it doesn't work for now. """

    with pytest.raises(TypeError):
        @type_check
        def f(y: typing.Literal["g"] | None = None) -> int | None:
            return 3


def test_custom_class() -> None:

    class C:
        pass

    @type_check
    def f(x: C) -> list[str]:
        return []

    f(C())

    with pytest.raises(TypeError):
        f(4)  # type: ignore


def test_enum() -> None:

    class E(Enum):
        e = 1

    @type_check
    def f(x: E) -> abc.Mapping[int, str | None]:
        return {}

    f(E.e)

    with pytest.raises(TypeError):
        f(1)  # type: ignore


def test_str_annotations() -> None:
    """ str annotations not supported """

    with pytest.raises(TypeError):
        @type_check
        def f(x: float, y: "str", z: object) -> object:
            return x


def test_second_arg() -> None:

    @type_check
    def f(x: int, y: float, z: str) -> int | None:
        return int(y)

    f(5, 5, "5")

    with pytest.raises(TypeError):
        f(5, 5j, "5")  # type: ignore


def test_method() -> None:

    class C:

        @type_check
        def f(self, x: object, y: str, z: bool | None) -> bool:
            return False

    c = C()

    c.f(c, "c", True)
    c.f(None, f"{c}", None)

    with pytest.raises(TypeError):
        c.f(None, c, False)  # type: ignore


def test_with_defaults() -> None:

    @type_check
    def f(x: str, y: object, z: int | None = None) -> dict[bool, bool]:
        return {}

    f("a", b"b")
    f("a", b"b", 3)

    with pytest.raises(TypeError):
        f(b"b", "a")  # type: ignore

    with pytest.raises(TypeError):
        f("a", 2.2, "c")  # type: ignore

    with pytest.raises(TypeError):
        f(1, b"b", 3)  # type: ignore


def test_with_mixed_arg_kwarg() -> None:

    @type_check
    def f(x: bool | None, *, y: str, z: bool = True) -> None:
        pass

    f(True, y="f")
    f(x=False, y="True", z=True)

    with pytest.raises(TypeError):
        f(True, y="f", z=8)  # type: ignore

    with pytest.raises(TypeError):
        f(x=b"False", y="8")  # type: ignore


def test_interface() -> None:
    class B(ABC):
        pass

    class C(B):
        pass

    class D:
        pass

    @type_check
    def f(b: B) -> frozenset[str]:
        return frozenset()

    c = C()
    f(c)

    d = D()
    with pytest.raises(TypeError):
        f(d)  # type: ignore


def test_interface_method() -> None:

    class B(ABC):
        @abstractmethod
        def f(self, x: bytes | None) -> int:
            """ interface method definition """

    class C(B):
        @type_check
        def f(self, x: bytes | None) -> int:
            return 0

    b: B = C()
    b.f(b"f")

    with pytest.raises(TypeError):
        b.f("f")  # type: ignore


def test_consumable_iterable() -> None:
    """ make sure the type checker doesn't consume the consumable iterable """

    def iterator() -> abc.Iterator[int]:
        yield 5

    @type_check
    def f(x: abc.Iterable[int]) -> bytearray:
        return bytearray()

    it = iterator()

    f(it)

    count = 0
    for _ in it:
        count += 1
    assert count == 1, f"{count=}"


def test_typed_dict() -> None:
    class TestTypedDict(typing.TypedDict):
        one_key: int
        other_key: list[str]

    @type_check
    def f(x: TestTypedDict) -> bool:
        return len(x) > 2

    f({
        "one_key": 4,
        "other_key": ["five"]
    })


def test_any() -> None:
    @type_check
    def f(x: typing.Any) -> str:
        return str(x)

    f(())
