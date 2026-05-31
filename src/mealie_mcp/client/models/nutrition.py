from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Nutrition")


@_attrs_define
class Nutrition:
    """
    Attributes:
        calories (None | str | Unset):
        carbohydrate_content (None | str | Unset):
        cholesterol_content (None | str | Unset):
        fat_content (None | str | Unset):
        fiber_content (None | str | Unset):
        protein_content (None | str | Unset):
        saturated_fat_content (None | str | Unset):
        sodium_content (None | str | Unset):
        sugar_content (None | str | Unset):
        trans_fat_content (None | str | Unset):
        unsaturated_fat_content (None | str | Unset):
    """

    calories: None | str | Unset = UNSET
    carbohydrate_content: None | str | Unset = UNSET
    cholesterol_content: None | str | Unset = UNSET
    fat_content: None | str | Unset = UNSET
    fiber_content: None | str | Unset = UNSET
    protein_content: None | str | Unset = UNSET
    saturated_fat_content: None | str | Unset = UNSET
    sodium_content: None | str | Unset = UNSET
    sugar_content: None | str | Unset = UNSET
    trans_fat_content: None | str | Unset = UNSET
    unsaturated_fat_content: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        calories: None | str | Unset
        if isinstance(self.calories, Unset):
            calories = UNSET
        else:
            calories = self.calories

        carbohydrate_content: None | str | Unset
        if isinstance(self.carbohydrate_content, Unset):
            carbohydrate_content = UNSET
        else:
            carbohydrate_content = self.carbohydrate_content

        cholesterol_content: None | str | Unset
        if isinstance(self.cholesterol_content, Unset):
            cholesterol_content = UNSET
        else:
            cholesterol_content = self.cholesterol_content

        fat_content: None | str | Unset
        if isinstance(self.fat_content, Unset):
            fat_content = UNSET
        else:
            fat_content = self.fat_content

        fiber_content: None | str | Unset
        if isinstance(self.fiber_content, Unset):
            fiber_content = UNSET
        else:
            fiber_content = self.fiber_content

        protein_content: None | str | Unset
        if isinstance(self.protein_content, Unset):
            protein_content = UNSET
        else:
            protein_content = self.protein_content

        saturated_fat_content: None | str | Unset
        if isinstance(self.saturated_fat_content, Unset):
            saturated_fat_content = UNSET
        else:
            saturated_fat_content = self.saturated_fat_content

        sodium_content: None | str | Unset
        if isinstance(self.sodium_content, Unset):
            sodium_content = UNSET
        else:
            sodium_content = self.sodium_content

        sugar_content: None | str | Unset
        if isinstance(self.sugar_content, Unset):
            sugar_content = UNSET
        else:
            sugar_content = self.sugar_content

        trans_fat_content: None | str | Unset
        if isinstance(self.trans_fat_content, Unset):
            trans_fat_content = UNSET
        else:
            trans_fat_content = self.trans_fat_content

        unsaturated_fat_content: None | str | Unset
        if isinstance(self.unsaturated_fat_content, Unset):
            unsaturated_fat_content = UNSET
        else:
            unsaturated_fat_content = self.unsaturated_fat_content

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if calories is not UNSET:
            field_dict["calories"] = calories
        if carbohydrate_content is not UNSET:
            field_dict["carbohydrateContent"] = carbohydrate_content
        if cholesterol_content is not UNSET:
            field_dict["cholesterolContent"] = cholesterol_content
        if fat_content is not UNSET:
            field_dict["fatContent"] = fat_content
        if fiber_content is not UNSET:
            field_dict["fiberContent"] = fiber_content
        if protein_content is not UNSET:
            field_dict["proteinContent"] = protein_content
        if saturated_fat_content is not UNSET:
            field_dict["saturatedFatContent"] = saturated_fat_content
        if sodium_content is not UNSET:
            field_dict["sodiumContent"] = sodium_content
        if sugar_content is not UNSET:
            field_dict["sugarContent"] = sugar_content
        if trans_fat_content is not UNSET:
            field_dict["transFatContent"] = trans_fat_content
        if unsaturated_fat_content is not UNSET:
            field_dict["unsaturatedFatContent"] = unsaturated_fat_content

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_calories(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        calories = _parse_calories(d.pop("calories", UNSET))

        def _parse_carbohydrate_content(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        carbohydrate_content = _parse_carbohydrate_content(d.pop("carbohydrateContent", UNSET))

        def _parse_cholesterol_content(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        cholesterol_content = _parse_cholesterol_content(d.pop("cholesterolContent", UNSET))

        def _parse_fat_content(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        fat_content = _parse_fat_content(d.pop("fatContent", UNSET))

        def _parse_fiber_content(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        fiber_content = _parse_fiber_content(d.pop("fiberContent", UNSET))

        def _parse_protein_content(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        protein_content = _parse_protein_content(d.pop("proteinContent", UNSET))

        def _parse_saturated_fat_content(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        saturated_fat_content = _parse_saturated_fat_content(d.pop("saturatedFatContent", UNSET))

        def _parse_sodium_content(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sodium_content = _parse_sodium_content(d.pop("sodiumContent", UNSET))

        def _parse_sugar_content(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sugar_content = _parse_sugar_content(d.pop("sugarContent", UNSET))

        def _parse_trans_fat_content(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        trans_fat_content = _parse_trans_fat_content(d.pop("transFatContent", UNSET))

        def _parse_unsaturated_fat_content(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unsaturated_fat_content = _parse_unsaturated_fat_content(
            d.pop("unsaturatedFatContent", UNSET)
        )

        nutrition = cls(
            calories=calories,
            carbohydrate_content=carbohydrate_content,
            cholesterol_content=cholesterol_content,
            fat_content=fat_content,
            fiber_content=fiber_content,
            protein_content=protein_content,
            saturated_fat_content=saturated_fat_content,
            sodium_content=sodium_content,
            sugar_content=sugar_content,
            trans_fat_content=trans_fat_content,
            unsaturated_fat_content=unsaturated_fat_content,
        )

        nutrition.additional_properties = d
        return nutrition

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
