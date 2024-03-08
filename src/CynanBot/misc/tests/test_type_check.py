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
    """ non-builtin generics not supported (yet?) """

    with pytest.raises(TypeError):
        @type_check
        def f(x: typing.Iterable[str]) -> str | None:
            return "abc"


def test_abc_generic() -> None:
    """ non-builtin generics not supported (yet?) """

    with pytest.raises(TypeError):
        @type_check
        def f(x: abc.Iterable[str]) -> str | None:
            return "abc"


def test_builtin_generic() -> None:
    """ builtin generics also not supported (yet?) """

    with pytest.raises(TypeError):
        @type_check
        def f(x: list[str]) -> str | None:
            return "abc"


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
