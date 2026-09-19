from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateIngredientFoodSubstitution")


@_attrs_define
class CreateIngredientFoodSubstitution:
    """
    Attributes:
        substitute_food_id (None | str | Unset):
        note (None | str | Unset):
    """

    substitute_food_id: str | Unset | None = UNSET
    note: str | Unset | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        substitute_food_id: str | Unset | None
        if isinstance(self.substitute_food_id, Unset):
            substitute_food_id = UNSET
        else:
            substitute_food_id = self.substitute_food_id

        note: str | Unset | None
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if substitute_food_id is not UNSET:
            field_dict["substituteFoodId"] = substitute_food_id
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_substitute_food_id(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        substitute_food_id = _parse_substitute_food_id(d.pop("substituteFoodId", UNSET))

        def _parse_note(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        note = _parse_note(d.pop("note", UNSET))

        create_ingredient_food_substitution = cls(
            substitute_food_id=substitute_food_id,
            note=note,
        )

        create_ingredient_food_substitution.additional_properties = d
        return create_ingredient_food_substitution

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
