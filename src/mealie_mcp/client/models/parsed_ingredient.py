from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ingredient_confidence import IngredientConfidence
    from ..models.recipe_ingredient_output import RecipeIngredientOutput


T = TypeVar("T", bound="ParsedIngredient")


@_attrs_define
class ParsedIngredient:
    """
    Attributes:
        ingredient (RecipeIngredientOutput):
        input_ (None | str | Unset):
        confidence (IngredientConfidence | Unset):
    """

    ingredient: RecipeIngredientOutput
    input_: None | str | Unset = UNSET
    confidence: IngredientConfidence | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ingredient = self.ingredient.to_dict()

        input_: None | str | Unset
        if isinstance(self.input_, Unset):
            input_ = UNSET
        else:
            input_ = self.input_

        confidence: dict[str, Any] | Unset = UNSET
        if not isinstance(self.confidence, Unset):
            confidence = self.confidence.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ingredient": ingredient,
            }
        )
        if input_ is not UNSET:
            field_dict["input"] = input_
        if confidence is not UNSET:
            field_dict["confidence"] = confidence

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_confidence import IngredientConfidence
        from ..models.recipe_ingredient_output import RecipeIngredientOutput

        d = dict(src_dict)
        ingredient = RecipeIngredientOutput.from_dict(d.pop("ingredient"))

        def _parse_input_(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        input_ = _parse_input_(d.pop("input", UNSET))

        _confidence = d.pop("confidence", UNSET)
        confidence: IngredientConfidence | Unset
        if isinstance(_confidence, Unset):
            confidence = UNSET
        else:
            confidence = IngredientConfidence.from_dict(_confidence)

        parsed_ingredient = cls(
            ingredient=ingredient,
            input_=input_,
            confidence=confidence,
        )

        parsed_ingredient.additional_properties = d
        return parsed_ingredient

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
