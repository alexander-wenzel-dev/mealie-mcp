from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ingredient_food_output import IngredientFoodOutput
    from ..models.ingredient_food_summary import IngredientFoodSummary


T = TypeVar("T", bound="RecipeSuggestionSubstitutedFood")


@_attrs_define
class RecipeSuggestionSubstitutedFood:
    """A food the recipe calls for that the user doesn't have, and the one covering it.

    Attributes:
        food (IngredientFoodOutput):
        substitute_food (IngredientFoodSummary): A trimmed projection of a food, with nothing on it that can recurse.

            Substitutions reference this rather than the full IngredientFood, which would make
            Pydantic walk food -> substitutions -> food forever and generate an equally circular
            TypeScript type.
    """

    food: IngredientFoodOutput
    substitute_food: IngredientFoodSummary
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        food = self.food.to_dict()

        substitute_food = self.substitute_food.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "food": food,
                "substituteFood": substitute_food,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_food_output import IngredientFoodOutput  # noqa: PLC0415
        from ..models.ingredient_food_summary import IngredientFoodSummary  # noqa: PLC0415

        d = dict(src_dict)
        food = IngredientFoodOutput.from_dict(d.pop("food"))

        substitute_food = IngredientFoodSummary.from_dict(d.pop("substituteFood"))

        recipe_suggestion_substituted_food = cls(
            food=food,
            substitute_food=substitute_food,
        )

        recipe_suggestion_substituted_food.additional_properties = d
        return recipe_suggestion_substituted_food

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
