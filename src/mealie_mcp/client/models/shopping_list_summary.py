from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.shopping_list_summary_extras_type_0 import ShoppingListSummaryExtrasType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.shopping_list_multi_purpose_label_out import ShoppingListMultiPurposeLabelOut
    from ..models.shopping_list_recipe_ref_out import ShoppingListRecipeRefOut


T = TypeVar("T", bound="ShoppingListSummary")


@_attrs_define
class ShoppingListSummary:
    """
    Attributes:
        group_id (str):
        user_id (str):
        id (str):
        household_id (str):
        recipe_references (list[ShoppingListRecipeRefOut]):
        label_settings (list[ShoppingListMultiPurposeLabelOut]):
        name (None | str | Unset):
        extras (None | ShoppingListSummaryExtrasType0 | Unset):  Default: ShoppingListSummaryExtrasType0().
        created_at (datetime.datetime | None | Unset):
        updated_at (datetime.datetime | None | Unset):
    """

    group_id: str
    user_id: str
    id: str
    household_id: str
    recipe_references: list[ShoppingListRecipeRefOut]
    label_settings: list[ShoppingListMultiPurposeLabelOut]
    name: None | str | Unset = UNSET
    extras: None | ShoppingListSummaryExtrasType0 | Unset = ShoppingListSummaryExtrasType0()
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        extras: dict[str, Any] | None | Unset
        if isinstance(self.extras, Unset):
            extras = UNSET
        elif isinstance(self.extras, ShoppingListSummaryExtrasType0):
            extras = self.extras.to_dict()
        else:
            extras = self.extras

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "groupId": group_id,
                "userId": user_id,
                "id": id,
                "householdId": household_id,
                "recipeReferences": recipe_references,
                "labelSettings": label_settings,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if extras is not UNSET:
            field_dict["extras"] = extras
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.shopping_list_multi_purpose_label_out import ShoppingListMultiPurposeLabelOut
        from ..models.shopping_list_recipe_ref_out import ShoppingListRecipeRefOut

        d = dict(src_dict)
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

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_extras(data: object) -> None | ShoppingListSummaryExtrasType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extras_type_0 = ShoppingListSummaryExtrasType0.from_dict(data)

                return extras_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | ShoppingListSummaryExtrasType0 | Unset, data)

        extras = _parse_extras(d.pop("extras", UNSET))

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = datetime.datetime.fromisoformat(data)

                return created_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("createdAt", UNSET))

        def _parse_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = datetime.datetime.fromisoformat(data)

                return updated_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updatedAt", UNSET))

        shopping_list_summary = cls(
            group_id=group_id,
            user_id=user_id,
            id=id,
            household_id=household_id,
            recipe_references=recipe_references,
            label_settings=label_settings,
            name=name,
            extras=extras,
            created_at=created_at,
            updated_at=updated_at,
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
