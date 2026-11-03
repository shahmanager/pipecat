import enum as _std_enum

# Re-export the standard Enum
Enum = _std_enum.Enum

# Provide a StrEnum fallback for Python versions < 3.11
try:
    StrEnum = _std_enum.StrEnum  # type: ignore[attr-defined]
except AttributeError:  # pragma: no cover
    class StrEnum(str, _std_enum.Enum):
        """Fallback StrEnum for older Python versions.

        Behaves like the built‑in ``enum.StrEnum`` introduced in Python 3.11.
        Members are instances of ``str`` and ``Enum`` so they can be compared
        directly to strings without accessing ``.value``.
        """
        pass
