"""Phase markers for CRSS critical / non-critical sections."""

from functools import wraps
from typing import Callable, TypeVar, Any, cast

F = TypeVar("F", bound=Callable[..., Any])


def critical_phase(func: F) -> F:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)
    return cast(F, wrapper)


def non_critical_phase(func: F) -> F:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)
    return cast(F, wrapper)
