
"""Phase markers for CRSS critical / non-critical sections.

These decorators are semantic markers only. They do not alter runtime behavior.
Tooling can use them for reporting and checks.
"""


from functools import wraps
from typing import Any, Callable, TypeVar, cast


F = TypeVar("F", bound=Callable[..., Any])


def critical_phase(func: F) -> F:
    """Mark a function as belonging to a Strict-A @critical phase.

    This decorator must not change runtime semantics.
    It is used purely as a marker for tools and reviewers.
    """  # noqa: D401

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)
    return cast(F, wrapper)


def non_critical_phase(func: F) -> F:
    """Mark a function as belonging to a non-critical phase.

    This decorator is also semantics-preserving and serves only as a marker.
    """  # noqa: D401

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)
    return cast(F, wrapper)
