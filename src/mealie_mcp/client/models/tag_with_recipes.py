from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.recipe_summary import RecipeSummary


T = TypeVar("T", bound="TagWithRecipes")


@_attrs_define
class TagWithRecipes:
    """
    Attributes:
        id (str):
        group_id (str):
        name (str):
        slug (str):
        recipe_count (int):  Default: 0.
        recipes (list[RecipeSummary]):
    """

    id: str
    group_id: str
    name: str
    slug: str
    recipes: list[RecipeSummary]
    recipe_count: int = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        group_id = self.group_id

        name = self.name

        slug = self.slug

        recipe_count = self.recipe_count

        recipes = []
        for recipes_item_data in self.recipes:
            recipes_item = recipes_item_data.to_dict()
            recipes.append(recipes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "groupId": group_id,
                "name": name,
                "slug": slug,
                "recipeCount": recipe_count,
                "recipes": recipes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recipe_summary import RecipeSummary  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        group_id = d.pop("groupId")

        name = d.pop("name")

        slug = d.pop("slug")

        recipe_count = d.pop("recipeCount")

        recipes = []
        _recipes = d.pop("recipes")
        for recipes_item_data in _recipes:
            recipes_item = RecipeSummary.from_dict(recipes_item_data)

            recipes.append(recipes_item)

        tag_with_recipes = cls(
            id=id,
            group_id=group_id,
            name=name,
            slug=slug,
            recipe_count=recipe_count,
            recipes=recipes,
        )

        tag_with_recipes.additional_properties = d
        return tag_with_recipes

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
