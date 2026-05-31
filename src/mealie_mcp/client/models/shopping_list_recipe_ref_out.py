from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.recipe_summary import RecipeSummary


T = TypeVar("T", bound="ShoppingListRecipeRefOut")


@_attrs_define
class ShoppingListRecipeRefOut:
    """
    Attributes:
        id (str):
        shopping_list_id (str):
        recipe_id (str):
        recipe_quantity (float):
        recipe (RecipeSummary):
    """

    id: str
    shopping_list_id: str
    recipe_id: str
    recipe_quantity: float
    recipe: RecipeSummary
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        shopping_list_id = self.shopping_list_id

        recipe_id = self.recipe_id

        recipe_quantity = self.recipe_quantity

        recipe = self.recipe.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "shoppingListId": shopping_list_id,
                "recipeId": recipe_id,
                "recipeQuantity": recipe_quantity,
                "recipe": recipe,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recipe_summary import RecipeSummary

        d = dict(src_dict)
        id = d.pop("id")

        shopping_list_id = d.pop("shoppingListId")

        recipe_id = d.pop("recipeId")

        recipe_quantity = d.pop("recipeQuantity")

        recipe = RecipeSummary.from_dict(d.pop("recipe"))

        shopping_list_recipe_ref_out = cls(
            id=id,
            shopping_list_id=shopping_list_id,
            recipe_id=recipe_id,
            recipe_quantity=recipe_quantity,
            recipe=recipe,
        )

        shopping_list_recipe_ref_out.additional_properties = d
        return shopping_list_recipe_ref_out

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
