from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ingredient_food_output import IngredientFoodOutput
    from ..models.recipe_summary import RecipeSummary
    from ..models.recipe_tool import RecipeTool


T = TypeVar("T", bound="RecipeSuggestionResponseItem")


@_attrs_define
class RecipeSuggestionResponseItem:
    """
    Attributes:
        recipe (RecipeSummary):
        missing_foods (list[IngredientFoodOutput]):
        missing_tools (list[RecipeTool]):
    """

    recipe: RecipeSummary
    missing_foods: list[IngredientFoodOutput]
    missing_tools: list[RecipeTool]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe = self.recipe.to_dict()

        missing_foods = []
        for missing_foods_item_data in self.missing_foods:
            missing_foods_item = missing_foods_item_data.to_dict()
            missing_foods.append(missing_foods_item)

        missing_tools = []
        for missing_tools_item_data in self.missing_tools:
            missing_tools_item = missing_tools_item_data.to_dict()
            missing_tools.append(missing_tools_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipe": recipe,
                "missingFoods": missing_foods,
                "missingTools": missing_tools,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_food_output import IngredientFoodOutput
        from ..models.recipe_summary import RecipeSummary
        from ..models.recipe_tool import RecipeTool

        d = dict(src_dict)
        recipe = RecipeSummary.from_dict(d.pop("recipe"))

        missing_foods = []
        _missing_foods = d.pop("missingFoods")
        for missing_foods_item_data in _missing_foods:
            missing_foods_item = IngredientFoodOutput.from_dict(missing_foods_item_data)

            missing_foods.append(missing_foods_item)

        missing_tools = []
        _missing_tools = d.pop("missingTools")
        for missing_tools_item_data in _missing_tools:
            missing_tools_item = RecipeTool.from_dict(missing_tools_item_data)

            missing_tools.append(missing_tools_item)

        recipe_suggestion_response_item = cls(
            recipe=recipe,
            missing_foods=missing_foods,
            missing_tools=missing_tools,
        )

        recipe_suggestion_response_item.additional_properties = d
        return recipe_suggestion_response_item

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
