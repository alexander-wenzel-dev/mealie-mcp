from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IngredientConfidence")


@_attrs_define
class IngredientConfidence:
    """
    Attributes:
        average (float | None | Unset):
        comment (float | None | Unset):
        name (float | None | Unset):
        unit (float | None | Unset):
        quantity (float | None | Unset):
        food (float | None | Unset):
    """

    average: float | None | Unset = UNSET
    comment: float | None | Unset = UNSET
    name: float | None | Unset = UNSET
    unit: float | None | Unset = UNSET
    quantity: float | None | Unset = UNSET
    food: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        average: float | None | Unset
        if isinstance(self.average, Unset):
            average = UNSET
        else:
            average = self.average

        comment: float | None | Unset
        if isinstance(self.comment, Unset):
            comment = UNSET
        else:
            comment = self.comment

        name: float | None | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        unit: float | None | Unset
        if isinstance(self.unit, Unset):
            unit = UNSET
        else:
            unit = self.unit

        quantity: float | None | Unset
        if isinstance(self.quantity, Unset):
            quantity = UNSET
        else:
            quantity = self.quantity

        food: float | None | Unset
        if isinstance(self.food, Unset):
            food = UNSET
        else:
            food = self.food

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if average is not UNSET:
            field_dict["average"] = average
        if comment is not UNSET:
            field_dict["comment"] = comment
        if name is not UNSET:
            field_dict["name"] = name
        if unit is not UNSET:
            field_dict["unit"] = unit
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if food is not UNSET:
            field_dict["food"] = food

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_average(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        average = _parse_average(d.pop("average", UNSET))

        def _parse_comment(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        comment = _parse_comment(d.pop("comment", UNSET))

        def _parse_name(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_unit(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        def _parse_quantity(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        quantity = _parse_quantity(d.pop("quantity", UNSET))

        def _parse_food(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        food = _parse_food(d.pop("food", UNSET))

        ingredient_confidence = cls(
            average=average,
            comment=comment,
            name=name,
            unit=unit,
            quantity=quantity,
            food=food,
        )

        ingredient_confidence.additional_properties = d
        return ingredient_confidence

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
