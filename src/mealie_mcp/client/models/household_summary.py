from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.read_household_preferences import ReadHouseholdPreferences


T = TypeVar("T", bound="HouseholdSummary")


@_attrs_define
class HouseholdSummary:
    """
    Attributes:
        group_id (str):
        name (str):
        id (str):
        slug (str):
        preferences (None | ReadHouseholdPreferences | Unset):
    """

    group_id: str
    name: str
    id: str
    slug: str
    preferences: None | ReadHouseholdPreferences | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.read_household_preferences import ReadHouseholdPreferences

        group_id = self.group_id

        name = self.name

        id = self.id

        slug = self.slug

        preferences: dict[str, Any] | None | Unset
        if isinstance(self.preferences, Unset):
            preferences = UNSET
        elif isinstance(self.preferences, ReadHouseholdPreferences):
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
                "slug": slug,
            }
        )
        if preferences is not UNSET:
            field_dict["preferences"] = preferences

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.read_household_preferences import ReadHouseholdPreferences

        d = dict(src_dict)
        group_id = d.pop("groupId")

        name = d.pop("name")

        id = d.pop("id")

        slug = d.pop("slug")

        def _parse_preferences(data: object) -> None | ReadHouseholdPreferences | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                preferences_type_0 = ReadHouseholdPreferences.from_dict(data)

                return preferences_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | ReadHouseholdPreferences | Unset, data)

        preferences = _parse_preferences(d.pop("preferences", UNSET))

        household_summary = cls(
            group_id=group_id,
            name=name,
            id=id,
            slug=slug,
            preferences=preferences,
        )

        household_summary.additional_properties = d
        return household_summary

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
