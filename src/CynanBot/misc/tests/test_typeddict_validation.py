from typing import Any, NotRequired, TypedDict, assert_type

from CynanBot.misc.type_check import validate_typeddict


def test_simple_positive() -> None:
    class TestType(TypedDict):
        a: int

    x = {"a": 3}

    assert validate_typeddict(x, TestType)
    assert_type(x, TestType)  # This tests the TypeGuard with the type checker.


def test_simple_negative() -> None:
    class TestType(TypedDict):
        a: int

    x = {"b": 3}

    assert not validate_typeddict(x, TestType)


def test_extra_keys_ok() -> None:
    class TestType(TypedDict):
        a: int

    x = {
        "a": 2,
        "b": "3"
    }

    assert validate_typeddict(x, TestType)


def test_wrong_value_type() -> None:
    class TestType(TypedDict):
        a: int

    x = {
        "a": "2",  # This type should fail validation.
        "b": "3"
    }

    assert not validate_typeddict(x, TestType)


def test_list_value() -> None:
    class TestType(TypedDict):
        a: list[float]

    x = {
        "a": [2, 3.1, 4],
        "b": "3"
    }

    assert validate_typeddict(x, TestType)


def test_list_value_negative() -> None:
    class TestType(TypedDict):
        a: list[float]

    x = {
        "a": [2, 3, "4"],  # This type should fail validation.
        "b": "3"
    }

    assert not validate_typeddict(x, TestType)


def test_not_required() -> None:
    class TestType(TypedDict):
        a: bool
        b: NotRequired[str]

    x = {
        "a": False
    }

    y = {
        "a": False,
        "b": "3"
    }

    assert validate_typeddict(x, TestType)
    assert validate_typeddict(y, TestType)


def test_not_required_wrong_type() -> None:
    class TestType(TypedDict):
        a: bool
        b: NotRequired[str]

    x = {
        "a": False,
        "b": 3  # This type should fail validation.
    }

    assert not validate_typeddict(x, TestType)


def test_nested_typeddict() -> None:
    class TestTypeA(TypedDict):
        b: dict[str, Any]
        c: int

    class TestTypeB(TypedDict):
        a: TestTypeA
        g: bool
        h: str

    x = {
        "a": {
            "b": {
                "j": 5,
            },
            "c": 42,
        },
        "g": True,
        "h": "H!!!!",
    }

    assert validate_typeddict(x, TestTypeB)


def test_nested_typeddict_negative() -> None:
    class TestTypeA(TypedDict):
        b: dict[str, Any]
        c: int

    class TestTypeB(TypedDict):
        a: TestTypeA
        g: bool
        h: str

    x = {
        "a": {
            "b": {
                "j": 5,
            },
            "c": 42.5,  # This type should fail validation.
        },
        "g": True,
        "h": "H!!!!",
    }

    assert not validate_typeddict(x, TestTypeB)


def test_list_of_json_objects() -> None:
    class TestTypeA(TypedDict):
        b: dict[str, Any]
        c: int

    class TestTypeB(TypedDict):
        a: list[TestTypeA]
        g: bool
        h: str

    x = {
        "a": [
            {
                "b": {
                    "j": 5,
                },
                "c": 42,
            },
            {
                "b": {
                    "k": 5,
                },
                "c": 43,
            },
        ],
        "g": True,
        "h": "H!!!!",
    }

    assert validate_typeddict(x, TestTypeB)


def test_list_of_json_objects_negative() -> None:
    class TestTypeA(TypedDict):
        b: dict[str, Any]
        c: int

    class TestTypeB(TypedDict):
        a: list[TestTypeA]
        g: bool
        h: str

    x = {
        "a": [
            {
                "b": {
                    "j": 5,
                },
                "c": 42,
            },
            {
                "b": True,  # This type should fail validation.
                "c": 43,
            },
        ],
        "g": True,
        "h": "H????",
    }

    assert not validate_typeddict(x, TestTypeB)
