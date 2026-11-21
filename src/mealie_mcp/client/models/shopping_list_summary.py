from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.shopping_list_multi_purpose_label_out import ShoppingListMultiPurposeLabelOut
    from ..models.shopping_list_recipe_ref_out import ShoppingListRecipeRefOut
    from ..models.shopping_list_summary_extras_type_0 import ShoppingListSummaryExtrasType0


T = TypeVar("T", bound="ShoppingListSummary")


@_attrs_define
class ShoppingListSummary:
    """
    Attributes:
        name (None | str):
        extras (None | ShoppingListSummaryExtrasType0):
        created_at (datetime.datetime | None):
        updated_at (datetime.datetime | None):
        group_id (str):
        user_id (str):
        id (str):
        household_id (str):
        recipe_references (list[ShoppingListRecipeRefOut]):
        label_settings (list[ShoppingListMultiPurposeLabelOut]):
    """

    name: str | None
    extras: ShoppingListSummaryExtrasType0 | None
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    group_id: str
    user_id: str
    id: str
    household_id: str
    recipe_references: list[ShoppingListRecipeRefOut]
    label_settings: list[ShoppingListMultiPurposeLabelOut]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.shopping_list_summary_extras_type_0 import ShoppingListSummaryExtrasType0  # noqa: PLC0415

        name: str | None
        name = self.name

        extras: dict[str, Any] | None
        if isinstance(self.extras, ShoppingListSummaryExtrasType0):
            extras = self.extras.to_dict()
        else:
            extras = self.extras

        created_at: str | None
        if isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: str | None
        if isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        group_id = self.group_id

        user_id = self.user_id

        id = self.id

        household_id = self.household_id

        recipe_references = []
        for recipe_references_item_data in self.recipe_references:
            recipe_references_item = recipe_references_item_data.to_dict()
            recipe_references.append(recipe_references_item)

        label_settings = []
        for label_settings_item_data in self.label_settings:
            label_settings_item = label_settings_item_data.to_dict()
            label_settings.append(label_settings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "extras": extras,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "groupId": group_id,
                "userId": user_id,
                "id": id,
                "householdId": household_id,
                "recipeReferences": recipe_references,
                "labelSettings": label_settings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.shopping_list_multi_purpose_label_out import ShoppingListMultiPurposeLabelOut  # noqa: PLC0415
        from ..models.shopping_list_recipe_ref_out import ShoppingListRecipeRefOut  # noqa: PLC0415
        from ..models.shopping_list_summary_extras_type_0 import ShoppingListSummaryExtrasType0  # noqa: PLC0415

        d = dict(src_dict)

        def _parse_name(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        name = _parse_name(d.pop("name"))

        def _parse_extras(data: object) -> ShoppingListSummaryExtrasType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extras_type_0 = ShoppingListSummaryExtrasType0.from_dict(data)

                return extras_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | ShoppingListSummaryExtrasType0, data)

        extras = _parse_extras(d.pop("extras"))

        def _parse_created_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = datetime.datetime.fromisoformat(data)

                return created_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None, data)

        created_at = _parse_created_at(d.pop("createdAt"))

        def _parse_updated_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = datetime.datetime.fromisoformat(data)

                return updated_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None, data)

        updated_at = _parse_updated_at(d.pop("updatedAt"))

        group_id = d.pop("groupId")

        user_id = d.pop("userId")

        id = d.pop("id")

        household_id = d.pop("householdId")

        recipe_references = []
        _recipe_references = d.pop("recipeReferences")
        for recipe_references_item_data in _recipe_references:
            recipe_references_item = ShoppingListRecipeRefOut.from_dict(recipe_references_item_data)

            recipe_references.append(recipe_references_item)

        label_settings = []
        _label_settings = d.pop("labelSettings")
        for label_settings_item_data in _label_settings:
            label_settings_item = ShoppingListMultiPurposeLabelOut.from_dict(
                label_settings_item_data
            )

            label_settings.append(label_settings_item)

        shopping_list_summary = cls(
            name=name,
            extras=extras,
            created_at=created_at,
            updated_at=updated_at,
            group_id=group_id,
            user_id=user_id,
            id=id,
            household_id=household_id,
            recipe_references=recipe_references,
            label_settings=label_settings,
        )

        shopping_list_summary.additional_properties = d
        return shopping_list_summary

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
