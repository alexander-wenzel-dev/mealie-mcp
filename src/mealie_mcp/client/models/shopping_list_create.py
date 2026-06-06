from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.shopping_list_create_extras_type_0 import ShoppingListCreateExtrasType0
from ..types import UNSET, Unset

T = TypeVar("T", bound="ShoppingListCreate")


@_attrs_define
class ShoppingListCreate:
    """
    Attributes:
        name (None | str | Unset):
        extras (None | ShoppingListCreateExtrasType0 | Unset):  Default: ShoppingListCreateExtrasType0().
        created_at (datetime.datetime | None | Unset):
        update_at (datetime.datetime | None | Unset):
    """

    name: None | str | Unset = UNSET
    extras: None | ShoppingListCreateExtrasType0 | Unset = ShoppingListCreateExtrasType0()
    created_at: datetime.datetime | None | Unset = UNSET
    update_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        extras: dict[str, Any] | None | Unset
        if isinstance(self.extras, Unset):
            extras = UNSET
        elif isinstance(self.extras, ShoppingListCreateExtrasType0):
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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if extras is not UNSET:
            field_dict["extras"] = extras
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if update_at is not UNSET:
            field_dict["update_at"] = update_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_extras(data: object) -> None | ShoppingListCreateExtrasType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extras_type_0 = ShoppingListCreateExtrasType0.from_dict(data)

                return extras_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | ShoppingListCreateExtrasType0 | Unset, data)

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

        shopping_list_create = cls(
            name=name,
            extras=extras,
            created_at=created_at,
            update_at=update_at,
        )

        shopping_list_create.additional_properties = d
        return shopping_list_create

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
