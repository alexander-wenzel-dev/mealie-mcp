from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.webhook_type import WebhookType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateWebhook")


@_attrs_define
class CreateWebhook:
    """
    Attributes:
        scheduled_time (str):
        enabled (bool | Unset):  Default: True.
        name (str | Unset):  Default: ''.
        url (str | Unset):  Default: ''.
        webhook_type (WebhookType | Unset):
    """

    scheduled_time: str
    enabled: bool | Unset = True
    name: str | Unset = ""
    url: str | Unset = ""
    webhook_type: WebhookType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scheduled_time = self.scheduled_time

        enabled = self.enabled

        name = self.name

        url = self.url

        webhook_type: str | Unset = UNSET
        if not isinstance(self.webhook_type, Unset):
            webhook_type = self.webhook_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scheduledTime": scheduled_time,
            }
        )
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if name is not UNSET:
            field_dict["name"] = name
        if url is not UNSET:
            field_dict["url"] = url
        if webhook_type is not UNSET:
            field_dict["webhookType"] = webhook_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scheduled_time = d.pop("scheduledTime")

        enabled = d.pop("enabled", UNSET)

        name = d.pop("name", UNSET)

        url = d.pop("url", UNSET)

        _webhook_type = d.pop("webhookType", UNSET)
        webhook_type: WebhookType | Unset
        if isinstance(_webhook_type, Unset):
            webhook_type = UNSET
        else:
            webhook_type = WebhookType(_webhook_type)

        create_webhook = cls(
            scheduled_time=scheduled_time,
            enabled=enabled,
            name=name,
            url=url,
            webhook_type=webhook_type,
        )

        create_webhook.additional_properties = d
        return create_webhook

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
