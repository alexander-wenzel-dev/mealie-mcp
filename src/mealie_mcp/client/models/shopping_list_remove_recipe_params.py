from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ShoppingListRemoveRecipeParams")


@_attrs_define
class ShoppingListRemoveRecipeParams:
    """
    Attributes:
        recipe_decrement_quantity (float | Unset):  Default: 1.0.
    """

    recipe_decrement_quantity: float | Unset = 1.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_decrement_quantity = self.recipe_decrement_quantity

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if recipe_decrement_quantity is not UNSET:
            field_dict["recipeDecrementQuantity"] = recipe_decrement_quantity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recipe_decrement_quantity = d.pop("recipeDecrementQuantity", UNSET)

        shopping_list_remove_recipe_params = cls(
            recipe_decrement_quantity=recipe_decrement_quantity,
        )

        shopping_list_remove_recipe_params.additional_properties = d
        return shopping_list_remove_recipe_params

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
