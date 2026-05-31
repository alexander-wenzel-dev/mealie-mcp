from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ShoppingListItemRecipeRefOut")


@_attrs_define
class ShoppingListItemRecipeRefOut:
    """
    Attributes:
        recipe_id (str):
        id (str):
        shopping_list_item_id (str):
        recipe_quantity (float | Unset):  Default: 0.0.
        recipe_scale (float | None | Unset):  Default: 1.0.
        recipe_note (None | str | Unset):
    """

    recipe_id: str
    id: str
    shopping_list_item_id: str
    recipe_quantity: float | Unset = 0.0
    recipe_scale: float | None | Unset = 1.0
    recipe_note: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_id = self.recipe_id

        id = self.id

        shopping_list_item_id = self.shopping_list_item_id

        recipe_quantity = self.recipe_quantity

        recipe_scale: float | None | Unset
        if isinstance(self.recipe_scale, Unset):
            recipe_scale = UNSET
        else:
            recipe_scale = self.recipe_scale

        recipe_note: None | str | Unset
        if isinstance(self.recipe_note, Unset):
            recipe_note = UNSET
        else:
            recipe_note = self.recipe_note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipeId": recipe_id,
                "id": id,
                "shoppingListItemId": shopping_list_item_id,
            }
        )
        if recipe_quantity is not UNSET:
            field_dict["recipeQuantity"] = recipe_quantity
        if recipe_scale is not UNSET:
            field_dict["recipeScale"] = recipe_scale
        if recipe_note is not UNSET:
            field_dict["recipeNote"] = recipe_note

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recipe_id = d.pop("recipeId")

        id = d.pop("id")

        shopping_list_item_id = d.pop("shoppingListItemId")

        recipe_quantity = d.pop("recipeQuantity", UNSET)

        def _parse_recipe_scale(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        recipe_scale = _parse_recipe_scale(d.pop("recipeScale", UNSET))

        def _parse_recipe_note(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        recipe_note = _parse_recipe_note(d.pop("recipeNote", UNSET))

        shopping_list_item_recipe_ref_out = cls(
            recipe_id=recipe_id,
            id=id,
            shopping_list_item_id=shopping_list_item_id,
            recipe_quantity=recipe_quantity,
            recipe_scale=recipe_scale,
            recipe_note=recipe_note,
        )

        shopping_list_item_recipe_ref_out.additional_properties = d
        return shopping_list_item_recipe_ref_out

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
