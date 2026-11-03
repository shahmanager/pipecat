import importlib

# Ensure a compatible StrEnum exists on the stdlib ``enum`` module for Python < 3.11.
_enum = importlib.import_module('enum')
if not hasattr(_enum, 'StrEnum'):
    class StrEnum(str, _enum.Enum):
        """Fallback StrEnum for older Python versions.

        Behaves like ``enum.StrEnum`` introduced in Python 3.11. Members are both
        ``str`` and ``Enum`` instances, allowing direct string comparison without
        accessing ``.value``.
        """
        pass
    _enum.StrEnum = StrEnum

# Provide ``Self`` typing alias for Python < 3.11.
import typing
if not hasattr(typing, 'Self'):
    typing.Self = typing.TypeVar('Self')

