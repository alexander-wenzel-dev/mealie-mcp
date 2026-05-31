from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.multi_purpose_label_summary import MultiPurposeLabelSummary


T = TypeVar("T", bound="ShoppingListMultiPurposeLabelOut")


@_attrs_define
class ShoppingListMultiPurposeLabelOut:
    """
    Attributes:
        shopping_list_id (str):
        label_id (str):
        id (str):
        label (MultiPurposeLabelSummary):
        position (int | Unset):  Default: 0.
    """

    shopping_list_id: str
    label_id: str
    id: str
    label: MultiPurposeLabelSummary
    position: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        shopping_list_id = self.shopping_list_id

        label_id = self.label_id

        id = self.id

        label = self.label.to_dict()

        position = self.position

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "shoppingListId": shopping_list_id,
                "labelId": label_id,
                "id": id,
                "label": label,
            }
        )
        if position is not UNSET:
            field_dict["position"] = position

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.multi_purpose_label_summary import MultiPurposeLabelSummary

        d = dict(src_dict)
        shopping_list_id = d.pop("shoppingListId")

        label_id = d.pop("labelId")

        id = d.pop("id")

        label = MultiPurposeLabelSummary.from_dict(d.pop("label"))

        position = d.pop("position", UNSET)

        shopping_list_multi_purpose_label_out = cls(
            shopping_list_id=shopping_list_id,
            label_id=label_id,
            id=id,
            label=label,
            position=position,
        )

        shopping_list_multi_purpose_label_out.additional_properties = d
        return shopping_list_multi_purpose_label_out

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
