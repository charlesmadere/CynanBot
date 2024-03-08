import logging
from types import UnionType
from typing import Callable, NoReturn, ParamSpec, TypeGuard, TypeVar, assert_type
from inspect import signature

_Checkable = type | UnionType | None

# TODO: implement generics
# uncheckable annotation name='x' ann=collections.abc.Iterable[str] type(ann)=<class 'types.GenericAlias'>
# (shows same "collections.abc" for typing.Iterable)


def _check_type(name: str, expected_type: _Checkable, value: object) -> None:
    """ raises TypeError if `value` is not `expected_type` """

    def error() -> NoReturn:
        raise TypeError(f"MALFORMED!! teh thingz!!!!1 oh, noes! guwuDesk {name=} {value=} {expected_type=}")

    if expected_type is None:
        if value is not None:
            error()
    elif isinstance(expected_type, type):
        if expected_type is float:
            if not isinstance(value, (float, int)):
                error()
        else:
            if not isinstance(value, expected_type):
                error()
    else:
        assert_type(expected_type, UnionType)
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
    raise RuntimeError if there's some annotation that can't be checked

    return True otherwise (never returns False)
    """

    def _individual(name: str, ann: object) -> TypeGuard[_Checkable]:
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
        if isinstance(ann, UnionType) and all(_individual(name, a) for a in ann.__args__):
            return True
        raise TypeError(f"uncheckable annotation {name=} {ann=} {type(ann)=}")

    return all(
        _individual(name, ann)
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
