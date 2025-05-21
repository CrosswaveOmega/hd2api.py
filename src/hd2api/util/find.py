from operator import attrgetter
from typing import Any, Iterable, Optional


def get_item(target: Iterable, /, **attrs: Any) -> Optional[Any]:
    """
    Look for the first item in iterable that matches the traits in attrs.

    Usage:
        get_item(target, attr1=value1, attr2=value2, ...)

    Parameters:
        target: An iterable collection of items to search through.
        attrs: Keyword arguments representing attribute-value pairs to match.

    Returns:
        The first item in the target that matches the specified attributes, or None if no match is found.
    """

    def matches(obj: Any) -> bool:
        return all(
            attrgetter(attr.replace("__", "."))(obj) == value
            for attr, value in attrs.items()
        )

    for element in target:
        if matches(element):
            return element
    return None
