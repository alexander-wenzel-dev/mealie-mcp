from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ingredient_food_summary import IngredientFoodSummary


T = TypeVar("T", bound="IngredientFoodSubstitution")


@_attrs_define
class IngredientFoodSubstitution:
    """
    Attributes:
        substitute_food_id (None | str | Unset):
        note (None | str | Unset):
        substitute_food (IngredientFoodSummary | None | Unset):
    """

    substitute_food_id: str | Unset | None = UNSET
    note: str | Unset | None = UNSET
    substitute_food: IngredientFoodSummary | Unset | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ingredient_food_summary import IngredientFoodSummary  # noqa: PLC0415

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

        substitute_food: dict[str, Any] | Unset | None
        if isinstance(self.substitute_food, Unset):
            substitute_food = UNSET
        elif isinstance(self.substitute_food, IngredientFoodSummary):
            substitute_food = self.substitute_food.to_dict()
        else:
            substitute_food = self.substitute_food

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if substitute_food_id is not UNSET:
            field_dict["substituteFoodId"] = substitute_food_id
        if note is not UNSET:
            field_dict["note"] = note
        if substitute_food is not UNSET:
            field_dict["substituteFood"] = substitute_food

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_food_summary import IngredientFoodSummary  # noqa: PLC0415

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

        def _parse_substitute_food(data: object) -> IngredientFoodSummary | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                substitute_food_type_0 = IngredientFoodSummary.from_dict(data)

                return substitute_food_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(IngredientFoodSummary | None | Unset, data)

        substitute_food = _parse_substitute_food(d.pop("substituteFood", UNSET))

        ingredient_food_substitution = cls(
            substitute_food_id=substitute_food_id,
            note=note,
            substitute_food=substitute_food,
        )

        ingredient_food_substitution.additional_properties = d
        return ingredient_food_substitution

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
