__all__ = [
    "BookPlugin",
    "BookPluginImpl",
    "HEXDOC_PROJECT_NAME",
    "HookReturn",
    "LoadTaggedUnionsImpl",
    "ModPlugin",
    "ModPluginImpl",
    "ModPluginImplWithProps",
    "ModPluginWithBook",
    "PluginManager",
    "PluginNotFoundError",
    "UpdateContextImpl",
    "UpdateTemplateArgsImpl",
    "ValidateFormatTreeImpl",
    "VersionedModPlugin",
    "hookimpl",
]

import pluggy

from .book_plugin import BookPlugin
from .manager import (
    PluginManager,
    PluginNotFoundError,
)
from .mod_plugin import (
    ModPlugin,
    ModPluginWithBook,
    VersionedModPlugin,
)
from .specs import (
    HEXDOC_PROJECT_NAME,
    BookPluginImpl,
    LoadTaggedUnionsImpl,
    ModPluginImpl,
    ModPluginImplWithProps,
    UpdateContextImpl,
    UpdateTemplateArgsImpl,
    ValidateFormatTreeImpl,
)
from .types import HookReturn

hookimpl = pluggy.HookimplMarker(HEXDOC_PROJECT_NAME)
"""Decorator for marking functions as hook implementations."""
