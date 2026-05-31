from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.group_event_notifier_options import GroupEventNotifierOptions


T = TypeVar("T", bound="GroupEventNotifierUpdate")


@_attrs_define
class GroupEventNotifierUpdate:
    """
    Attributes:
        name (str):
        group_id (str):
        household_id (str):
        id (str):
        apprise_url (None | str | Unset):
        enabled (bool | Unset):  Default: True.
        options (GroupEventNotifierOptions | Unset): These events are in-sync with the EventTypes found in the
            EventBusService.
            If you modify this, make sure to update the EventBusService as well.
    """

    name: str
    group_id: str
    household_id: str
    id: str
    apprise_url: None | str | Unset = UNSET
    enabled: bool | Unset = True
    options: GroupEventNotifierOptions | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        group_id = self.group_id

        household_id = self.household_id

        id = self.id

        apprise_url: None | str | Unset
        if isinstance(self.apprise_url, Unset):
            apprise_url = UNSET
        else:
            apprise_url = self.apprise_url

        enabled = self.enabled

        options: dict[str, Any] | Unset = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "groupId": group_id,
                "householdId": household_id,
                "id": id,
            }
        )
        if apprise_url is not UNSET:
            field_dict["appriseUrl"] = apprise_url
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.group_event_notifier_options import GroupEventNotifierOptions

        d = dict(src_dict)
        name = d.pop("name")

        group_id = d.pop("groupId")

        household_id = d.pop("householdId")

        id = d.pop("id")

        def _parse_apprise_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        apprise_url = _parse_apprise_url(d.pop("appriseUrl", UNSET))

        enabled = d.pop("enabled", UNSET)

        _options = d.pop("options", UNSET)
        options: GroupEventNotifierOptions | Unset
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = GroupEventNotifierOptions.from_dict(_options)

        group_event_notifier_update = cls(
            name=name,
            group_id=group_id,
            household_id=household_id,
            id=id,
            apprise_url=apprise_url,
            enabled=enabled,
            options=options,
        )

        group_event_notifier_update.additional_properties = d
        return group_event_notifier_update

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
