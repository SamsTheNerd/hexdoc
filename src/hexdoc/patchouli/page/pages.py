from typing import Any, Self

from pydantic import model_validator

from hexdoc.core import Entity, ItemStack, ResourceLocation
from hexdoc.minecraft import LocalizedStr
from hexdoc.minecraft.assets import ItemWithTexture, Texture
from hexdoc.minecraft.recipe import CraftingRecipe

from ..text import FormatTree
from .abstract_pages import Page, PageDoubleRecipe, PageWithText, PageWithTitle


class TextPage(Page, type="patchouli:text"):
    title: LocalizedStr | None = None
    text: FormatTree


class CraftingPage(PageDoubleRecipe[CraftingRecipe], type="patchouli:crafting"):
    pass


class EmptyPage(Page, type="patchouli:empty", template_type="patchouli:page"):
    draw_filler: bool = True


class EntityPage(PageWithText, type="patchouli:entity"):
    entity: Entity
    scale: float = 1
    offset: float = 0
    rotate: bool = True
    default_rotation: float = -45
    name: LocalizedStr | None = None


class ImagePage(PageWithTitle, type="patchouli:image"):
    images: list[Texture]
    border: bool = False

    @property
    def images_with_alt(self):
        for image in self.images:
            if self.title:
                yield image, self.title
            else:
                yield image, str(image)


class LinkPage(TextPage, type="patchouli:link"):
    url: str
    link_text: LocalizedStr


class MultiblockPage(PageWithText, type="patchouli:multiblock"):
    name: LocalizedStr
    multiblock_id: ResourceLocation | None = None
    # TODO: https://vazkiimods.github.io/Patchouli/docs/patchouli-basics/multiblocks/
    # this should be a modeled class, but hex doesn't have any multiblock pages so idc
    multiblock: Any | None = None
    enable_visualize: bool = True

    @model_validator(mode="after")
    def _check_multiblock(self) -> Self:
        if self.multiblock_id is None and self.multiblock is None:
            raise ValueError(f"One of multiblock_id or multiblock must be set\n{self}")
        return self


class QuestPage(PageWithText, type="patchouli:quest"):
    trigger: ResourceLocation | None = None
    title: LocalizedStr = LocalizedStr.with_value("Objective")


class RelationsPage(PageWithText, type="patchouli:relations"):
    entries: list[ResourceLocation]
    title: LocalizedStr = LocalizedStr.with_value("Related Chapters")


class SmeltingPage(PageWithTitle, type="patchouli:smelting"):
    recipe: ItemStack
    recipe2: ItemStack | None = None


class SpotlightPage(PageWithTitle, type="patchouli:spotlight"):
    item: ItemWithTexture
    link_recipe: bool = False
