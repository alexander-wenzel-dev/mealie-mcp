from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ai_provider_settings_out import AIProviderSettingsOut
    from ..models.category_out import CategoryOut
    from ..models.group_household_summary import GroupHouseholdSummary
    from ..models.group_preferences_out import GroupPreferencesOut
    from ..models.user_summary import UserSummary
    from ..models.webhook_out import WebhookOut


T = TypeVar("T", bound="GroupOut")


@_attrs_define
class GroupOut:
    """
    Attributes:
        name (str):
        id (str):
        slug (str):
        categories (list[CategoryOut] | None):
        webhooks (list[WebhookOut]):
        households (list[GroupHouseholdSummary] | None):
        users (list[UserSummary] | None):
        preferences (GroupPreferencesOut | None):
        ai_provider_settings (AIProviderSettingsOut | None):
    """

    name: str
    id: str
    slug: str
    categories: list[CategoryOut] | None
    webhooks: list[WebhookOut]
    households: list[GroupHouseholdSummary] | None
    users: list[UserSummary] | None
    preferences: GroupPreferencesOut | None
    ai_provider_settings: AIProviderSettingsOut | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ai_provider_settings_out import AIProviderSettingsOut  # noqa: PLC0415
        from ..models.group_preferences_out import GroupPreferencesOut  # noqa: PLC0415

        name = self.name

        id = self.id

        slug = self.slug

        categories: list[dict[str, Any]] | None
        if isinstance(self.categories, list):
            categories = []
            for categories_type_0_item_data in self.categories:
                categories_type_0_item = categories_type_0_item_data.to_dict()
                categories.append(categories_type_0_item)

        else:
            categories = self.categories

        webhooks = []
        for webhooks_item_data in self.webhooks:
            webhooks_item = webhooks_item_data.to_dict()
            webhooks.append(webhooks_item)

        households: list[dict[str, Any]] | None
        if isinstance(self.households, list):
            households = []
            for households_type_0_item_data in self.households:
                households_type_0_item = households_type_0_item_data.to_dict()
                households.append(households_type_0_item)

        else:
            households = self.households

        users: list[dict[str, Any]] | None
        if isinstance(self.users, list):
            users = []
            for users_type_0_item_data in self.users:
                users_type_0_item = users_type_0_item_data.to_dict()
                users.append(users_type_0_item)

        else:
            users = self.users

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
                "categories": categories,
                "webhooks": webhooks,
                "households": households,
                "users": users,
                "preferences": preferences,
                "aiProviderSettings": ai_provider_settings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ai_provider_settings_out import AIProviderSettingsOut  # noqa: PLC0415
        from ..models.category_out import CategoryOut  # noqa: PLC0415
        from ..models.group_household_summary import GroupHouseholdSummary  # noqa: PLC0415
        from ..models.group_preferences_out import GroupPreferencesOut  # noqa: PLC0415
        from ..models.user_summary import UserSummary  # noqa: PLC0415
        from ..models.webhook_out import WebhookOut  # noqa: PLC0415

        d = dict(src_dict)
        name = d.pop("name")

        id = d.pop("id")

        slug = d.pop("slug")

        def _parse_categories(data: object) -> list[CategoryOut] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                categories_type_0 = []
                _categories_type_0 = data
                for categories_type_0_item_data in _categories_type_0:
                    categories_type_0_item = CategoryOut.from_dict(categories_type_0_item_data)

                    categories_type_0.append(categories_type_0_item)

                return categories_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(list[CategoryOut] | None, data)

        categories = _parse_categories(d.pop("categories"))

        webhooks = []
        _webhooks = d.pop("webhooks")
        for webhooks_item_data in _webhooks:
            webhooks_item = WebhookOut.from_dict(webhooks_item_data)

            webhooks.append(webhooks_item)

        def _parse_households(data: object) -> list[GroupHouseholdSummary] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                households_type_0 = []
                _households_type_0 = data
                for households_type_0_item_data in _households_type_0:
                    households_type_0_item = GroupHouseholdSummary.from_dict(
                        households_type_0_item_data
                    )

                    households_type_0.append(households_type_0_item)

                return households_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(list[GroupHouseholdSummary] | None, data)

        households = _parse_households(d.pop("households"))

        def _parse_users(data: object) -> list[UserSummary] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                users_type_0 = []
                _users_type_0 = data
                for users_type_0_item_data in _users_type_0:
                    users_type_0_item = UserSummary.from_dict(users_type_0_item_data)

                    users_type_0.append(users_type_0_item)

                return users_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(list[UserSummary] | None, data)

        users = _parse_users(d.pop("users"))

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

        group_out = cls(
            name=name,
            id=id,
            slug=slug,
            categories=categories,
            webhooks=webhooks,
            households=households,
            users=users,
            preferences=preferences,
            ai_provider_settings=ai_provider_settings,
        )

        group_out.additional_properties = d
        return group_out

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
