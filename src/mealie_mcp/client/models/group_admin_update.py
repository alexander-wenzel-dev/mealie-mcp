from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_provider_settings_update import AIProviderSettingsUpdate
    from ..models.update_group_preferences import UpdateGroupPreferences


T = TypeVar("T", bound="GroupAdminUpdate")


@_attrs_define
class GroupAdminUpdate:
    """
    Attributes:
        id (str):
        name (str):
        preferences (None | Unset | UpdateGroupPreferences):
        ai_provider_settings (AIProviderSettingsUpdate | None | Unset):
    """

    id: str
    name: str
    preferences: None | Unset | UpdateGroupPreferences = UNSET
    ai_provider_settings: AIProviderSettingsUpdate | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ai_provider_settings_update import AIProviderSettingsUpdate
        from ..models.update_group_preferences import UpdateGroupPreferences

        id = self.id

        name = self.name

        preferences: dict[str, Any] | None | Unset
        if isinstance(self.preferences, Unset):
            preferences = UNSET
        elif isinstance(self.preferences, UpdateGroupPreferences):
            preferences = self.preferences.to_dict()
        else:
            preferences = self.preferences

        ai_provider_settings: dict[str, Any] | None | Unset
        if isinstance(self.ai_provider_settings, Unset):
            ai_provider_settings = UNSET
        elif isinstance(self.ai_provider_settings, AIProviderSettingsUpdate):
            ai_provider_settings = self.ai_provider_settings.to_dict()
        else:
            ai_provider_settings = self.ai_provider_settings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if preferences is not UNSET:
            field_dict["preferences"] = preferences
        if ai_provider_settings is not UNSET:
            field_dict["aiProviderSettings"] = ai_provider_settings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ai_provider_settings_update import AIProviderSettingsUpdate
        from ..models.update_group_preferences import UpdateGroupPreferences

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        def _parse_preferences(data: object) -> None | Unset | UpdateGroupPreferences:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                preferences_type_0 = UpdateGroupPreferences.from_dict(data)

                return preferences_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | Unset | UpdateGroupPreferences, data)

        preferences = _parse_preferences(d.pop("preferences", UNSET))

        def _parse_ai_provider_settings(data: object) -> AIProviderSettingsUpdate | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                ai_provider_settings_type_0 = AIProviderSettingsUpdate.from_dict(data)

                return ai_provider_settings_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(AIProviderSettingsUpdate | None | Unset, data)

        ai_provider_settings = _parse_ai_provider_settings(d.pop("aiProviderSettings", UNSET))

        group_admin_update = cls(
            id=id,
            name=name,
            preferences=preferences,
            ai_provider_settings=ai_provider_settings,
        )

        group_admin_update.additional_properties = d
        return group_admin_update

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
