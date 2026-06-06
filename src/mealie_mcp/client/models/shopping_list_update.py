from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.shopping_list_update_extras_type_0 import ShoppingListUpdateExtrasType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.shopping_list_item_out import ShoppingListItemOut


T = TypeVar("T", bound="ShoppingListUpdate")


@_attrs_define
class ShoppingListUpdate:
    """
    Attributes:
        group_id (str):
        user_id (str):
        id (str):
        name (None | str | Unset):
        extras (None | ShoppingListUpdateExtrasType0 | Unset):  Default: ShoppingListUpdateExtrasType0().
        created_at (datetime.datetime | None | Unset):
        update_at (datetime.datetime | None | Unset):
        list_items (list[ShoppingListItemOut] | Unset):
    """

    group_id: str
    user_id: str
    id: str
    name: None | str | Unset = UNSET
    extras: None | ShoppingListUpdateExtrasType0 | Unset = ShoppingListUpdateExtrasType0()
    created_at: datetime.datetime | None | Unset = UNSET
    update_at: datetime.datetime | None | Unset = UNSET
    list_items: list[ShoppingListItemOut] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        group_id = self.group_id

        user_id = self.user_id

        id = self.id

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        extras: dict[str, Any] | None | Unset
        if isinstance(self.extras, Unset):
            extras = UNSET
        elif isinstance(self.extras, ShoppingListUpdateExtrasType0):
            extras = self.extras.to_dict()
        else:
            extras = self.extras

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        update_at: None | str | Unset
        if isinstance(self.update_at, Unset):
            update_at = UNSET
        elif isinstance(self.update_at, datetime.datetime):
            update_at = self.update_at.isoformat()
        else:
            update_at = self.update_at

        list_items: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.list_items, Unset):
            list_items = []
            for list_items_item_data in self.list_items:
                list_items_item = list_items_item_data.to_dict()
                list_items.append(list_items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "groupId": group_id,
                "userId": user_id,
                "id": id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if extras is not UNSET:
            field_dict["extras"] = extras
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if update_at is not UNSET:
            field_dict["update_at"] = update_at
        if list_items is not UNSET:
            field_dict["listItems"] = list_items

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.shopping_list_item_out import ShoppingListItemOut

        d = dict(src_dict)
        group_id = d.pop("groupId")

        user_id = d.pop("userId")

        id = d.pop("id")

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_extras(data: object) -> None | ShoppingListUpdateExtrasType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extras_type_0 = ShoppingListUpdateExtrasType0.from_dict(data)

                return extras_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | ShoppingListUpdateExtrasType0 | Unset, data)

        extras = _parse_extras(d.pop("extras", UNSET))

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = datetime.datetime.fromisoformat(data)

                return created_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("createdAt", UNSET))

        def _parse_update_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                update_at_type_0 = datetime.datetime.fromisoformat(data)

                return update_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None | Unset, data)

        update_at = _parse_update_at(d.pop("update_at", UNSET))

        _list_items = d.pop("listItems", UNSET)
        list_items: list[ShoppingListItemOut] | Unset = UNSET
        if _list_items is not UNSET:
            list_items = []
            for list_items_item_data in _list_items:
                list_items_item = ShoppingListItemOut.from_dict(list_items_item_data)

                list_items.append(list_items_item)

        shopping_list_update = cls(
            group_id=group_id,
            user_id=user_id,
            id=id,
            name=name,
            extras=extras,
            created_at=created_at,
            update_at=update_at,
            list_items=list_items,
        )

        shopping_list_update.additional_properties = d
        return shopping_list_update

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
