from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_household_preferences import UpdateHouseholdPreferences


T = TypeVar("T", bound="UpdateHouseholdAdmin")


@_attrs_define
class UpdateHouseholdAdmin:
    """
    Attributes:
        group_id (str):
        name (str):
        id (str):
        preferences (None | Unset | UpdateHouseholdPreferences):
    """

    group_id: str
    name: str
    id: str
    preferences: None | Unset | UpdateHouseholdPreferences = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.update_household_preferences import UpdateHouseholdPreferences

        group_id = self.group_id

        name = self.name

        id = self.id

        preferences: dict[str, Any] | None | Unset
        if isinstance(self.preferences, Unset):
            preferences = UNSET
        elif isinstance(self.preferences, UpdateHouseholdPreferences):
            preferences = self.preferences.to_dict()
        else:
            preferences = self.preferences

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "groupId": group_id,
                "name": name,
                "id": id,
            }
        )
        if preferences is not UNSET:
            field_dict["preferences"] = preferences

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_household_preferences import UpdateHouseholdPreferences

        d = dict(src_dict)
        group_id = d.pop("groupId")

        name = d.pop("name")

        id = d.pop("id")

        def _parse_preferences(data: object) -> None | Unset | UpdateHouseholdPreferences:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                preferences_type_0 = UpdateHouseholdPreferences.from_dict(data)

                return preferences_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | Unset | UpdateHouseholdPreferences, data)

        preferences = _parse_preferences(d.pop("preferences", UNSET))

        update_household_admin = cls(
            group_id=group_id,
            name=name,
            id=id,
            preferences=preferences,
        )

        update_household_admin.additional_properties = d
        return update_household_admin

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
