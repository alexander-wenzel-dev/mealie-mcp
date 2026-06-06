from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.shopping_list_item_out_output import ShoppingListItemOutOutput


T = TypeVar("T", bound="ShoppingListItemsCollectionOut")


@_attrs_define
class ShoppingListItemsCollectionOut:
    """Container for bulk shopping list item changes

    Attributes:
        created_items (list[ShoppingListItemOutOutput] | Unset):
        updated_items (list[ShoppingListItemOutOutput] | Unset):
        deleted_items (list[ShoppingListItemOutOutput] | Unset):
    """

    created_items: list[ShoppingListItemOutOutput] | Unset = UNSET
    updated_items: list[ShoppingListItemOutOutput] | Unset = UNSET
    deleted_items: list[ShoppingListItemOutOutput] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_items: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.created_items, Unset):
            created_items = []
            for created_items_item_data in self.created_items:
                created_items_item = created_items_item_data.to_dict()
                created_items.append(created_items_item)

        updated_items: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.updated_items, Unset):
            updated_items = []
            for updated_items_item_data in self.updated_items:
                updated_items_item = updated_items_item_data.to_dict()
                updated_items.append(updated_items_item)

        deleted_items: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.deleted_items, Unset):
            deleted_items = []
            for deleted_items_item_data in self.deleted_items:
                deleted_items_item = deleted_items_item_data.to_dict()
                deleted_items.append(deleted_items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_items is not UNSET:
            field_dict["createdItems"] = created_items
        if updated_items is not UNSET:
            field_dict["updatedItems"] = updated_items
        if deleted_items is not UNSET:
            field_dict["deletedItems"] = deleted_items

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.shopping_list_item_out_output import ShoppingListItemOutOutput

        d = dict(src_dict)
        _created_items = d.pop("createdItems", UNSET)
        created_items: list[ShoppingListItemOutOutput] | Unset = UNSET
        if _created_items is not UNSET:
            created_items = []
            for created_items_item_data in _created_items:
                created_items_item = ShoppingListItemOutOutput.from_dict(created_items_item_data)

                created_items.append(created_items_item)

        _updated_items = d.pop("updatedItems", UNSET)
        updated_items: list[ShoppingListItemOutOutput] | Unset = UNSET
        if _updated_items is not UNSET:
            updated_items = []
            for updated_items_item_data in _updated_items:
                updated_items_item = ShoppingListItemOutOutput.from_dict(updated_items_item_data)

                updated_items.append(updated_items_item)

        _deleted_items = d.pop("deletedItems", UNSET)
        deleted_items: list[ShoppingListItemOutOutput] | Unset = UNSET
        if _deleted_items is not UNSET:
            deleted_items = []
            for deleted_items_item_data in _deleted_items:
                deleted_items_item = ShoppingListItemOutOutput.from_dict(deleted_items_item_data)

                deleted_items.append(deleted_items_item)

        shopping_list_items_collection_out = cls(
            created_items=created_items,
            updated_items=updated_items,
            deleted_items=deleted_items,
        )

        shopping_list_items_collection_out.additional_properties = d
        return shopping_list_items_collection_out

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
