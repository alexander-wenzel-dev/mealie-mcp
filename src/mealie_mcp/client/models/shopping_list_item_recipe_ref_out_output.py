from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ShoppingListItemRecipeRefOutOutput")


@_attrs_define
class ShoppingListItemRecipeRefOutOutput:
    """
    Attributes:
        recipe_id (str):
        recipe_quantity (float):  Default: 0.0.
        recipe_scale (float | None):  Default: 1.0.
        recipe_note (None | str):
        id (str):
        shopping_list_item_id (str):
    """

    recipe_id: str
    recipe_note: str | None
    id: str
    shopping_list_item_id: str
    recipe_quantity: float = 0.0
    recipe_scale: float | None = 1.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_id = self.recipe_id

        recipe_quantity = self.recipe_quantity

        recipe_scale: float | None
        recipe_scale = self.recipe_scale

        recipe_note: str | None
        recipe_note = self.recipe_note

        id = self.id

        shopping_list_item_id = self.shopping_list_item_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipeId": recipe_id,
                "recipeQuantity": recipe_quantity,
                "recipeScale": recipe_scale,
                "recipeNote": recipe_note,
                "id": id,
                "shoppingListItemId": shopping_list_item_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recipe_id = d.pop("recipeId")

        recipe_quantity = d.pop("recipeQuantity")

        def _parse_recipe_scale(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        recipe_scale = _parse_recipe_scale(d.pop("recipeScale"))

        def _parse_recipe_note(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        recipe_note = _parse_recipe_note(d.pop("recipeNote"))

        id = d.pop("id")

        shopping_list_item_id = d.pop("shoppingListItemId")

        shopping_list_item_recipe_ref_out_output = cls(
            recipe_id=recipe_id,
            recipe_quantity=recipe_quantity,
            recipe_scale=recipe_scale,
            recipe_note=recipe_note,
            id=id,
            shopping_list_item_id=shopping_list_item_id,
        )

        shopping_list_item_recipe_ref_out_output.additional_properties = d
        return shopping_list_item_recipe_ref_out_output

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
