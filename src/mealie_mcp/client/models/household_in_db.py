from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.household_user_summary import HouseholdUserSummary
    from ..models.read_household_preferences import ReadHouseholdPreferences
    from ..models.read_webhook import ReadWebhook


T = TypeVar("T", bound="HouseholdInDB")


@_attrs_define
class HouseholdInDB:
    """
    Attributes:
        group_id (str):
        name (str):
        id (str):
        slug (str):
        group (str):
        preferences (None | ReadHouseholdPreferences | Unset):
        users (list[HouseholdUserSummary] | None | Unset):
        webhooks (list[ReadWebhook] | Unset):
    """

    group_id: str
    name: str
    id: str
    slug: str
    group: str
    preferences: None | ReadHouseholdPreferences | Unset = UNSET
    users: list[HouseholdUserSummary] | None | Unset = UNSET
    webhooks: list[ReadWebhook] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.read_household_preferences import ReadHouseholdPreferences

        group_id = self.group_id

        name = self.name

        id = self.id

        slug = self.slug

        group = self.group

        preferences: dict[str, Any] | None | Unset
        if isinstance(self.preferences, Unset):
            preferences = UNSET
        elif isinstance(self.preferences, ReadHouseholdPreferences):
            preferences = self.preferences.to_dict()
        else:
            preferences = self.preferences

        users: list[dict[str, Any]] | None | Unset
        if isinstance(self.users, Unset):
            users = UNSET
        elif isinstance(self.users, list):
            users = []
            for users_type_0_item_data in self.users:
                users_type_0_item = users_type_0_item_data.to_dict()
                users.append(users_type_0_item)

        else:
            users = self.users

        webhooks: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.webhooks, Unset):
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
                "group": group,
            }
        )
        if preferences is not UNSET:
            field_dict["preferences"] = preferences
        if users is not UNSET:
            field_dict["users"] = users
        if webhooks is not UNSET:
            field_dict["webhooks"] = webhooks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.household_user_summary import HouseholdUserSummary
        from ..models.read_household_preferences import ReadHouseholdPreferences
        from ..models.read_webhook import ReadWebhook

        d = dict(src_dict)
        group_id = d.pop("groupId")

        name = d.pop("name")

        id = d.pop("id")

        slug = d.pop("slug")

        group = d.pop("group")

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

        def _parse_users(data: object) -> list[HouseholdUserSummary] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
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
            return cast(list[HouseholdUserSummary] | None | Unset, data)

        users = _parse_users(d.pop("users", UNSET))

        _webhooks = d.pop("webhooks", UNSET)
        webhooks: list[ReadWebhook] | Unset = UNSET
        if _webhooks is not UNSET:
            webhooks = []
            for webhooks_item_data in _webhooks:
                webhooks_item = ReadWebhook.from_dict(webhooks_item_data)

                webhooks.append(webhooks_item)

        household_in_db = cls(
            group_id=group_id,
            name=name,
            id=id,
            slug=slug,
            group=group,
            preferences=preferences,
            users=users,
            webhooks=webhooks,
        )

        household_in_db.additional_properties = d
        return household_in_db

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
