from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.multi_purpose_label_summary_output import MultiPurposeLabelSummaryOutput


T = TypeVar("T", bound="ShoppingListMultiPurposeLabelOut")


@_attrs_define
class ShoppingListMultiPurposeLabelOut:
    """
    Attributes:
        shopping_list_id (str):
        label_id (str):
        position (int):  Default: 0.
        id (str):
        label (MultiPurposeLabelSummaryOutput):
    """

    shopping_list_id: str
    label_id: str
    id: str
    label: MultiPurposeLabelSummaryOutput
    position: int = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        shopping_list_id = self.shopping_list_id

        label_id = self.label_id

        position = self.position

        id = self.id

        label = self.label.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "shoppingListId": shopping_list_id,
                "labelId": label_id,
                "position": position,
                "id": id,
                "label": label,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.multi_purpose_label_summary_output import MultiPurposeLabelSummaryOutput  # noqa: PLC0415

        d = dict(src_dict)
        shopping_list_id = d.pop("shoppingListId")

        label_id = d.pop("labelId")

        position = d.pop("position")

        id = d.pop("id")

        label = MultiPurposeLabelSummaryOutput.from_dict(d.pop("label"))

        shopping_list_multi_purpose_label_out = cls(
            shopping_list_id=shopping_list_id,
            label_id=label_id,
            position=position,
            id=id,
            label=label,
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
