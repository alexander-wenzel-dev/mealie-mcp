from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.recipe_ingredient import RecipeIngredient


T = TypeVar("T", bound="ShoppingListAddRecipeParams")


@_attrs_define
class ShoppingListAddRecipeParams:
    """
    Attributes:
        recipe_increment_quantity (float | Unset):  Default: 1.0.
        recipe_ingredients (list[RecipeIngredient] | None | Unset):
    """

    recipe_increment_quantity: float | Unset = 1.0
    recipe_ingredients: list[RecipeIngredient] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_increment_quantity = self.recipe_increment_quantity

        recipe_ingredients: list[dict[str, Any]] | None | Unset
        if isinstance(self.recipe_ingredients, Unset):
            recipe_ingredients = UNSET
        elif isinstance(self.recipe_ingredients, list):
            recipe_ingredients = []
            for recipe_ingredients_type_0_item_data in self.recipe_ingredients:
                recipe_ingredients_type_0_item = recipe_ingredients_type_0_item_data.to_dict()
                recipe_ingredients.append(recipe_ingredients_type_0_item)

        else:
            recipe_ingredients = self.recipe_ingredients

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if recipe_increment_quantity is not UNSET:
            field_dict["recipeIncrementQuantity"] = recipe_increment_quantity
        if recipe_ingredients is not UNSET:
            field_dict["recipeIngredients"] = recipe_ingredients

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recipe_ingredient import RecipeIngredient

        d = dict(src_dict)
        recipe_increment_quantity = d.pop("recipeIncrementQuantity", UNSET)

        def _parse_recipe_ingredients(data: object) -> list[RecipeIngredient] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                recipe_ingredients_type_0 = []
                _recipe_ingredients_type_0 = data
                for recipe_ingredients_type_0_item_data in _recipe_ingredients_type_0:
                    recipe_ingredients_type_0_item = RecipeIngredient.from_dict(
                        recipe_ingredients_type_0_item_data
                    )

                    recipe_ingredients_type_0.append(recipe_ingredients_type_0_item)

                return recipe_ingredients_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(list[RecipeIngredient] | None | Unset, data)

        recipe_ingredients = _parse_recipe_ingredients(d.pop("recipeIngredients", UNSET))

        shopping_list_add_recipe_params = cls(
            recipe_increment_quantity=recipe_increment_quantity,
            recipe_ingredients=recipe_ingredients,
        )

        shopping_list_add_recipe_params.additional_properties = d
        return shopping_list_add_recipe_params

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
