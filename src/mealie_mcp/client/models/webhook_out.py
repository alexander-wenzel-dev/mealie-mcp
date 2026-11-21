from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.webhook_type import WebhookType

T = TypeVar("T", bound="WebhookOut")


@_attrs_define
class WebhookOut:
    """
    Attributes:
        enabled (bool):  Default: True.
        name (str):  Default: ''.
        url (str):  Default: ''.
        webhook_type (WebhookType):
        scheduled_time (str):
        group_id (str):
        household_id (str):
        id (str):
    """

    webhook_type: WebhookType
    scheduled_time: str
    group_id: str
    household_id: str
    id: str
    enabled: bool = True
    name: str = ""
    url: str = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        name = self.name

        url = self.url

        webhook_type = self.webhook_type.value

        scheduled_time = self.scheduled_time

        group_id = self.group_id

        household_id = self.household_id

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "name": name,
                "url": url,
                "webhookType": webhook_type,
                "scheduledTime": scheduled_time,
                "groupId": group_id,
                "householdId": household_id,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        name = d.pop("name")

        url = d.pop("url")

        webhook_type = WebhookType(d.pop("webhookType"))

        scheduled_time = d.pop("scheduledTime")

        group_id = d.pop("groupId")

        household_id = d.pop("householdId")

        id = d.pop("id")

        webhook_out = cls(
            enabled=enabled,
            name=name,
            url=url,
            webhook_type=webhook_type,
            scheduled_time=scheduled_time,
            group_id=group_id,
            household_id=household_id,
            id=id,
        )

        webhook_out.additional_properties = d
        return webhook_out

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
