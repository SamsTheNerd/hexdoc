# pyright: reportPrivateUsage=false

from importlib.resources import Package
from pathlib import Path
from typing import Any, Mapping

import hexdoc
from hexdoc import HEXDOC_MODID, VERSION
from hexdoc.core import IsVersion, ModResourceLoader, ResourceLocation
from hexdoc.minecraft.recipe import (
    ingredients as minecraft_ingredients,
    recipes as minecraft_recipes,
)
from hexdoc.patchouli import Book, BookContext
from hexdoc.patchouli.page import pages as patchouli_pages
from hexdoc.plugin import (
    BookPlugin,
    BookPluginImpl,
    HookReturn,
    LoadTaggedUnionsImpl,
    ModPlugin,
    ModPluginImpl,
    hookimpl,
)
from hexdoc.utils import ContextSource, JSONDict, cast_context


class HexdocPlugin(LoadTaggedUnionsImpl, ModPluginImpl, BookPluginImpl):
    @staticmethod
    @hookimpl
    def hexdoc_mod_plugin(branch: str) -> ModPlugin:
        return HexdocModPlugin(branch=branch)

    @staticmethod
    @hookimpl
    def hexdoc_book_plugin() -> BookPlugin[Any]:
        return PatchouliBookPlugin()

    @staticmethod
    @hookimpl
    def hexdoc_load_tagged_unions() -> HookReturn[Package]:
        return [
            patchouli_pages,
            minecraft_recipes,
            minecraft_ingredients,
        ]


class HexdocModPlugin(ModPlugin):
    @property
    def modid(self):
        return HEXDOC_MODID

    @property
    def full_version(self):
        return VERSION

    @property
    def plugin_version(self):
        return VERSION

    def resource_dirs(self) -> HookReturn[Package]:
        from hexdoc._export import generated, resources

        return [generated, resources]

    def jinja_template_root(self) -> tuple[Package, str] | None:
        return hexdoc, "_templates"

    def default_rendered_templates(self) -> dict[str | Path, str]:
        return {
            "index.html": "index.html.jinja",
            "index.css": "index.css.jinja",
            "textures.css": "textures.jcss.jinja",
            "index.js": "index.js.jinja",
        }


class PatchouliBookPlugin(BookPlugin[Book]):
    @property
    def modid(self):
        return "patchouli"

    def load_book_data(
        self,
        book_id: ResourceLocation,
        loader: ModResourceLoader,
    ) -> tuple[ResourceLocation, JSONDict]:
        _, data = loader.load_resource("data", "patchouli_books", book_id / "book")

        if IsVersion("<1.20") and "extend" in data:
            book_id = ResourceLocation.model_validate(data["extend"])
            return self.load_book_data(book_id, loader)

        return book_id, data

    def is_i18n_enabled(self, book_data: Mapping[str, Any]):
        return book_data.get("i18n", False) is True

    def validate_book(
        self,
        book_data: Mapping[str, Any],
        *,
        context: ContextSource,
    ):
        book_ctx = BookContext.of(context)
        loader = ModResourceLoader.of(context)

        book = Book.model_validate(book_data, context=cast_context(context))
        book._load_categories(context, book_ctx)
        book._load_entries(context, book_ctx, loader)

        return book
