# Copyright (c) 2024-2026, Daily
# SPDX-License-Identifier: BSD 2-Clause License

import sitecustomize

# Existing imports
import importlib
import importlib.util
import os
import sys
import asyncio
from importlib.metadata import version as lib_version
from loguru import logger


# -------------------------------------------------------------------
# Version fallback – protect against missing package metadata
# -------------------------------------------------------------------
try:
    __version__ = lib_version("pipecat-ai")
except Exception:
    __version__ = "0.0.0"

# -------------------------------------------------------------------
# Optional wait_for2 import for Python < 3.12
# -------------------------------------------------------------------
if sys.version_info < (3, 12):
    try:
        import wait_for2
        # Replace asyncio.wait_for with the backported implementation.
        asyncio.wait_for = wait_for2.wait_for
    except ImportError:
        # wait_for2 not installed – continue without the patch.
        pass

# -------------------------------------------------------------------
# StrEnum fallback for Python < 3.11 – injected into the stdlib enum module
# -------------------------------------------------------------------
_enum = importlib.import_module('enum')
if not hasattr(_enum, 'StrEnum'):
    class StrEnum(str, _enum.Enum):
        """Fallback StrEnum for older Python versions.

        Behaves like ``enum.StrEnum`` introduced in Python 3.11. Members are
        both ``str`` and ``Enum`` instances, enabling direct string comparison
        without accessing ``.value``.
        """
        pass
    _enum.StrEnum = StrEnum

# -------------------------------------------------------------------
# Version banner and legacy flow check (unchanged from upstream)
# -------------------------------------------------------------------
def _should_log_version_banner() -> bool:
    """Whether to emit the import-time version banner.

    The banner is a handy startup marker for bots and interactive use, but it's
    just noise for the ``pipecat`` / ``pc`` CLI — it even corrupts ``--help``
    output — so suppress it there.
    """
    program = os.path.splitext(os.path.basename(sys.argv[0] or ""))[0]
    return program not in ("pipecat", "pc")

def _warn_if_standalone_flows_installed() -> None:
    """Flag the deprecated standalone ``pipecat-ai-flows`` package if it is also installed.

    Pipecat Flows now ships inside ``pipecat-ai`` as ``pipecat.flows``. Older
    ``pipecat-ai-flows`` releases allow ``pipecat-ai<2``, so they can end up
    installed next to a Pipecat that already includes Flows — a redundant, easily
    confused setup. The check lives here, in the top-level package init that runs
    on any ``pipecat`` import, rather than in ``pipecat.flows`` – so it also fires
    for apps still importing the standalone ``pipecat_flows`` (which pulls in core
    Pipecat but never ``pipecat.flows``). Detection uses ``find_spec`` to avoid
    importing the standalone package.
    """
    try:
        installed = importlib.util.find_spec("pipecat_flows") is not None
    except (ImportError, ValueError):
        installed = False
    if installed:
        logger.error(
            "The separate `pipecat-ai-flows` package is installed alongside a version "
            "of Pipecat that already includes Pipecat Flows as `pipecat.flows`. You do "
            "not need both — uninstall `pipecat-ai-flows` and import Flows from "
            "`pipecat.flows`."
        )

if _should_log_version_banner():
    logger.info(f"ᓚᘏᗢ Pipecat {__version__} (Python {sys.version}) ᓚᘏᗢ")
    _warn_if_standalone_flows_installed()

def version() -> str:
    """Returns the Pipecat version."""
    return __version__
