import logging
import typing
from collections.abc import Iterable, Iterator, Mapping
from inspect import signature
from types import GenericAlias, UnionType
from typing import Any, Callable, NoReturn, ParamSpec, TypeGuard, TypeVar

_Checkable = type | UnionType | GenericAlias | None


def _is_generic_alias(obj: object) -> TypeGuard[GenericAlias]:
    """
    `typing._GenericAlias` is undocumented, so it could break with Python update.

    It doesn't have everything that `types.GenericAlias` has, but it has what we need.
    """
    # TypeGuard could change to PEP 742 when available
    return isinstance(obj, GenericAlias) or isinstance(obj, getattr(typing, "_GenericAlias"))


def validate_typeddict[T](obj: dict[str, Any] | Any, t_dict: type[T], value_name: str = "unknown") -> TypeGuard[T]:
    # TODO: assert t_dict is a TypedDict - I'm not sure of a good way to do this.
    # I thought of `assert TypedDict in t_dict.__orig_bases__`
    # but that doesn't work if the `TypedDict` came from `typing_extensions`
    if not isinstance(obj, Mapping):
        return False
    for name, type_ in t_dict.__annotations__.items():
        required = True
        if repr(type_).startswith("typing.NotRequired"):  # maybe not the best way
            required = False
            type_ = type_.__args__[0]

        if required and name not in obj:
            return False

        sentinel = object()
        value = obj.get(name, sentinel)
        if value is not sentinel:
            try:
                _check_type(value_name, type_, value)
            except TypeError:
                return False
    return True


def _check_type(name: str, expected_type: _Checkable, value: object) -> None:
    """ raises TypeError if `value` is not `expected_type` """

    def error() -> NoReturn:
        raise TypeError(f"MALFORMED!! teh thingz!!!!1 oh, noes! guwuDesk {name=} {value=} {expected_type=}")

    if expected_type is None:
        if value is not None:
            error()
    elif expected_type is typing.Any:
        pass
    elif isinstance(expected_type, type):
        if expected_type is float:
            if not isinstance(value, (float, int)):
                error()
        else:
            try:  # I don't know a better way to find out if `expected_type` is `TypedDict`
                isinstance_result = isinstance(value, expected_type)
            except TypeError:
                isinstance_result = validate_typeddict(value, expected_type, name)
            if not isinstance_result:
                error()
    elif _is_generic_alias(expected_type):
        if not isinstance(value, expected_type.__origin__):
            error()
        type_vars = expected_type.__args__
        if len(type_vars) == 1:
            assert isinstance(value, Iterable), f"not iterable {name=} {value=} {expected_type=}"
            # if this is an Iterator, we don't want to check the values inside, because it can consume them
            if not isinstance(value, Iterator):
                for each_value in value:
                    _check_type(f"item in {name}", type_vars[0], each_value)
        else:
            assert len(type_vars) == 2, f"{name=} {value=} {expected_type=}"
            assert isinstance(value, Mapping), f"not mapping {name=} {value=} {expected_type=}"
            for key in value:
                each_value = value[key]
                _check_type(f"key in {name}", type_vars[0], key)
                _check_type(f"value in {name}", type_vars[1], each_value)
    else:
        # assert_type(expected_type, UnionType)  # need pep 742 for _is_generic_alias
        assert isinstance(expected_type, UnionType)
        found_valid = False
        for u_type in expected_type.__args__:
            got_type_error = False
            try:
                _check_type(name, u_type, value)
            except TypeError:
                got_type_error = True
            if not got_type_error:
                found_valid = True
                break
        if not found_valid:
            error()


_names_that_dont_need_annotations = frozenset([
    "return", "self"
])


def _is_checkable(annotations: dict[str, object]) -> TypeGuard[dict[str, _Checkable]]:
    """
    raise TypeError if there's some annotation that can't be checked

    return True otherwise (never returns False)
    """

    def individual(name: str, ann: object) -> TypeGuard[_Checkable]:
        if ann is None:
            return True
        if isinstance(ann, str):
            # I've heard some libraries use eval for this.
            # It could get tricky.
            # Let's see how often it comes up.
            logging.warning(f"str annotation found {ann=}")
        if isinstance(ann, type):
            # recursion base case
            return True
        if isinstance(ann, UnionType) and all(individual(name, a) for a in ann.__args__):
            return True
        if _is_generic_alias(ann):
            if len(ann.__args__) == 1:  # 1 type var
                if (
                    isinstance(ann.__origin__, type) and
                    issubclass(ann.__origin__, Iterable) and
                    individual(f"type var of {name}", ann.__args__[0])
                ):
                    return True
            elif len(ann.__args__) == 2:  # 2 type vars
                if (
                    isinstance(ann.__origin__, type) and
                    issubclass(ann.__origin__, Mapping) and
                    individual(f"key type of {name}", ann.__args__[0]) and
                    individual(f"value type of {name}", ann.__args__[1])
                ):
                    return True
            # fall through to raise
        raise TypeError(f"uncheckable annotation {name=} {ann=} {type(ann)=}")

    return all(
        individual(name, ann)
        for name, ann in annotations.items()
        if name not in _names_that_dont_need_annotations
    )


_P = ParamSpec('_P')
_RT = TypeVar("_RT")


def type_check(func: Callable[_P, _RT]) -> Callable[_P, _RT]:
    """ apply run-time type checking to the parameters of this function """

    annotations = func.__annotations__
    assert _is_checkable(annotations)
    sig = signature(func)
    params = sig.parameters

    # make sure all parameters have a type annotation
    for param_name in params:
        if param_name not in annotations and param_name not in _names_that_dont_need_annotations:
            raise TypeError(f"{param_name=} missing type annotation")

    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _RT:

        # positional arguments
        for param_name, param_value in zip(params, args):
            if param_name not in annotations:
                assert param_name == "self", f"samusConf {param_name=}"
                continue
            param_type = annotations[param_name]
            _check_type(param_name, param_type, param_value)

        # keyword arguments
        for param_name, param_value in kwargs.items():
            if param_name not in params:
                # let it go through - will get normal "no argument named" error
                continue
            param_type = annotations[param_name]
            _check_type(param_name, param_type, param_value)

        result = func(*args, **kwargs)
        return result

    return wrapper
