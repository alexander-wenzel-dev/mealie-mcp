from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ai_provider_settings_out import AIProviderSettingsOut
    from ..models.group_preferences_out import GroupPreferencesOut


T = TypeVar("T", bound="GroupSummary")


@_attrs_define
class GroupSummary:
    """
    Attributes:
        name (str):
        id (str):
        slug (str):
        preferences (GroupPreferencesOut | None):
        ai_provider_settings (AIProviderSettingsOut | None):
    """

    name: str
    id: str
    slug: str
    preferences: GroupPreferencesOut | None
    ai_provider_settings: AIProviderSettingsOut | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ai_provider_settings_out import AIProviderSettingsOut  # noqa: PLC0415
        from ..models.group_preferences_out import GroupPreferencesOut  # noqa: PLC0415

        name = self.name

        id = self.id

        slug = self.slug

        preferences: dict[str, Any] | None
        if isinstance(self.preferences, GroupPreferencesOut):
            preferences = self.preferences.to_dict()
        else:
            preferences = self.preferences

        ai_provider_settings: dict[str, Any] | None
        if isinstance(self.ai_provider_settings, AIProviderSettingsOut):
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
                "preferences": preferences,
                "aiProviderSettings": ai_provider_settings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ai_provider_settings_out import AIProviderSettingsOut  # noqa: PLC0415
        from ..models.group_preferences_out import GroupPreferencesOut  # noqa: PLC0415

        d = dict(src_dict)
        name = d.pop("name")

        id = d.pop("id")

        slug = d.pop("slug")

        def _parse_preferences(data: object) -> GroupPreferencesOut | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                preferences_type_0 = GroupPreferencesOut.from_dict(data)

                return preferences_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(GroupPreferencesOut | None, data)

        preferences = _parse_preferences(d.pop("preferences"))

        def _parse_ai_provider_settings(data: object) -> AIProviderSettingsOut | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                ai_provider_settings_type_0 = AIProviderSettingsOut.from_dict(data)

                return ai_provider_settings_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(AIProviderSettingsOut | None, data)

        ai_provider_settings = _parse_ai_provider_settings(d.pop("aiProviderSettings"))

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
