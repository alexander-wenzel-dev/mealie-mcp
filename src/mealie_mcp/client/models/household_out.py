from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.household_preferences_out import HouseholdPreferencesOut
    from ..models.household_user_summary import HouseholdUserSummary
    from ..models.webhook_out import WebhookOut


T = TypeVar("T", bound="HouseholdOut")


@_attrs_define
class HouseholdOut:
    """
    Attributes:
        group_id (str):
        name (str):
        id (str):
        slug (str):
        preferences (HouseholdPreferencesOut | None):
        group (str):
        users (list[HouseholdUserSummary] | None):
        webhooks (list[WebhookOut]):
    """

    group_id: str
    name: str
    id: str
    slug: str
    preferences: HouseholdPreferencesOut | None
    group: str
    users: list[HouseholdUserSummary] | None
    webhooks: list[WebhookOut]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.household_preferences_out import HouseholdPreferencesOut  # noqa: PLC0415

        group_id = self.group_id

        name = self.name

        id = self.id

        slug = self.slug

        preferences: dict[str, Any] | None
        if isinstance(self.preferences, HouseholdPreferencesOut):
            preferences = self.preferences.to_dict()
        else:
            preferences = self.preferences

        group = self.group

        users: list[dict[str, Any]] | None
        if isinstance(self.users, list):
            users = []
            for users_type_0_item_data in self.users:
                users_type_0_item = users_type_0_item_data.to_dict()
                users.append(users_type_0_item)

        else:
            users = self.users

        webhooks = []
        for webhooks_item_data in self.webhooks:
            webhooks_item = webhooks_item_data.to_dict()
            webhooks.append(webhooks_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "groupId": group_id,
                "name": name,
                "id": id,
                "slug": slug,
                "preferences": preferences,
                "group": group,
                "users": users,
                "webhooks": webhooks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.household_preferences_out import HouseholdPreferencesOut  # noqa: PLC0415
        from ..models.household_user_summary import HouseholdUserSummary  # noqa: PLC0415
        from ..models.webhook_out import WebhookOut  # noqa: PLC0415

        d = dict(src_dict)
        group_id = d.pop("groupId")

        name = d.pop("name")

        id = d.pop("id")

        slug = d.pop("slug")

        def _parse_preferences(data: object) -> HouseholdPreferencesOut | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                preferences_type_0 = HouseholdPreferencesOut.from_dict(data)

                return preferences_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(HouseholdPreferencesOut | None, data)

        preferences = _parse_preferences(d.pop("preferences"))

        group = d.pop("group")

        def _parse_users(data: object) -> list[HouseholdUserSummary] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                users_type_0 = []
                _users_type_0 = data
                for users_type_0_item_data in _users_type_0:
                    users_type_0_item = HouseholdUserSummary.from_dict(users_type_0_item_data)

                    users_type_0.append(users_type_0_item)

                return users_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(list[HouseholdUserSummary] | None, data)

        users = _parse_users(d.pop("users"))

        webhooks = []
        _webhooks = d.pop("webhooks")
        for webhooks_item_data in _webhooks:
            webhooks_item = WebhookOut.from_dict(webhooks_item_data)

            webhooks.append(webhooks_item)

        household_out = cls(
            group_id=group_id,
            name=name,
            id=id,
            slug=slug,
            preferences=preferences,
            group=group,
            users=users,
            webhooks=webhooks,
        )

        household_out.additional_properties = d
        return household_out

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
