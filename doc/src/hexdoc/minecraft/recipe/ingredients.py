from typing import Any

from hexdoc.resource import ResourceLocation, TypeTaggedUnion
from hexdoc.utils import AnyContext, NoValue


class ItemIngredient(
    TypeTaggedUnion[AnyContext],
    group="hexdoc.ItemIngredient",
    type=None,
):
    pass


ItemIngredientOrList = ItemIngredient[AnyContext] | list[ItemIngredient[AnyContext]]


class MinecraftItemIdIngredient(ItemIngredient[Any], type=NoValue):
    item: ResourceLocation


class MinecraftItemTagIngredient(ItemIngredient[Any], type=NoValue):
    tag: ResourceLocation
