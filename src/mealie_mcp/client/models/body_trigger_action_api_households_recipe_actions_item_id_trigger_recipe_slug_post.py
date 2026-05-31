from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BodyTriggerActionApiHouseholdsRecipeActionsItemIdTriggerRecipeSlugPost")


@_attrs_define
class BodyTriggerActionApiHouseholdsRecipeActionsItemIdTriggerRecipeSlugPost:
    """
    Attributes:
        recipe_scale (float | Unset):  Default: 1.0.
    """

    recipe_scale: float | Unset = 1.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_scale = self.recipe_scale

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if recipe_scale is not UNSET:
            field_dict["recipe_scale"] = recipe_scale

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recipe_scale = d.pop("recipe_scale", UNSET)

        body_trigger_action_api_households_recipe_actions_item_id_trigger_recipe_slug_post = cls(
            recipe_scale=recipe_scale,
        )

        body_trigger_action_api_households_recipe_actions_item_id_trigger_recipe_slug_post.additional_properties = d
        return body_trigger_action_api_households_recipe_actions_item_id_trigger_recipe_slug_post

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
