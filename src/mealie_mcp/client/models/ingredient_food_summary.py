from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IngredientFoodSummary")


@_attrs_define
class IngredientFoodSummary:
    """A trimmed projection of a food, with nothing on it that can recurse.

    Substitutions reference this rather than the full IngredientFood, which would make
    Pydantic walk food -> substitutions -> food forever and generate an equally circular
    TypeScript type.

        Attributes:
            id (str):
            name (str):
            plural_name (None | str | Unset):
    """

    id: str
    name: str
    plural_name: str | Unset | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        plural_name: str | Unset | None
        if isinstance(self.plural_name, Unset):
            plural_name = UNSET
        else:
            plural_name = self.plural_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if plural_name is not UNSET:
            field_dict["pluralName"] = plural_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        def _parse_plural_name(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        plural_name = _parse_plural_name(d.pop("pluralName", UNSET))

        ingredient_food_summary = cls(
            id=id,
            name=name,
            plural_name=plural_name,
        )

        ingredient_food_summary.additional_properties = d
        return ingredient_food_summary

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
