from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_provider_settings_out import AIProviderSettingsOut
    from ..models.read_group_preferences import ReadGroupPreferences


T = TypeVar("T", bound="GroupSummary")


@_attrs_define
class GroupSummary:
    """
    Attributes:
        name (str):
        id (str):
        slug (str):
        preferences (None | ReadGroupPreferences | Unset):
        ai_provider_settings (AIProviderSettingsOut | None | Unset):
    """

    name: str
    id: str
    slug: str
    preferences: None | ReadGroupPreferences | Unset = UNSET
    ai_provider_settings: AIProviderSettingsOut | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ai_provider_settings_out import AIProviderSettingsOut
        from ..models.read_group_preferences import ReadGroupPreferences

        name = self.name

        id = self.id

        slug = self.slug

        preferences: dict[str, Any] | None | Unset
        if isinstance(self.preferences, Unset):
            preferences = UNSET
        elif isinstance(self.preferences, ReadGroupPreferences):
            preferences = self.preferences.to_dict()
        else:
            preferences = self.preferences

        ai_provider_settings: dict[str, Any] | None | Unset
        if isinstance(self.ai_provider_settings, Unset):
            ai_provider_settings = UNSET
        elif isinstance(self.ai_provider_settings, AIProviderSettingsOut):
            ai_provider_settings = self.ai_provider_settings.to_dict()
        else:
            ai_provider_settings = self.ai_provider_settings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "id": id,
                "slug": slug,
            }
        )
        if preferences is not UNSET:
            field_dict["preferences"] = preferences
        if ai_provider_settings is not UNSET:
            field_dict["aiProviderSettings"] = ai_provider_settings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ai_provider_settings_out import AIProviderSettingsOut
        from ..models.read_group_preferences import ReadGroupPreferences

        d = dict(src_dict)
        name = d.pop("name")

        id = d.pop("id")

        slug = d.pop("slug")

        def _parse_preferences(data: object) -> None | ReadGroupPreferences | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                preferences_type_0 = ReadGroupPreferences.from_dict(data)

                return preferences_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | ReadGroupPreferences | Unset, data)

        preferences = _parse_preferences(d.pop("preferences", UNSET))

        def _parse_ai_provider_settings(data: object) -> AIProviderSettingsOut | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                ai_provider_settings_type_0 = AIProviderSettingsOut.from_dict(data)

                return ai_provider_settings_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(AIProviderSettingsOut | None | Unset, data)

        ai_provider_settings = _parse_ai_provider_settings(d.pop("aiProviderSettings", UNSET))

        group_summary = cls(
            name=name,
            id=id,
            slug=slug,
            preferences=preferences,
            ai_provider_settings=ai_provider_settings,
        )

        group_summary.additional_properties = d
        return group_summary

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
