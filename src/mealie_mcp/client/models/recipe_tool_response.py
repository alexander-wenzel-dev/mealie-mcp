from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.recipe_summary import RecipeSummary


T = TypeVar("T", bound="RecipeToolResponse")


@_attrs_define
class RecipeToolResponse:
    """
    Attributes:
        name (str):
        id (str):
        group_id (str):
        slug (str):
        households_with_tool (list[str] | Unset):
        recipes (list[RecipeSummary] | Unset):
    """

    name: str
    id: str
    group_id: str
    slug: str
    households_with_tool: list[str] | Unset = UNSET
    recipes: list[RecipeSummary] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        id = self.id

        group_id = self.group_id

        slug = self.slug

        households_with_tool: list[str] | Unset = UNSET
        if not isinstance(self.households_with_tool, Unset):
            households_with_tool = self.households_with_tool

        recipes: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.recipes, Unset):
            recipes = []
            for recipes_item_data in self.recipes:
                recipes_item = recipes_item_data.to_dict()
                recipes.append(recipes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "id": id,
                "groupId": group_id,
                "slug": slug,
            }
        )
        if households_with_tool is not UNSET:
            field_dict["householdsWithTool"] = households_with_tool
        if recipes is not UNSET:
            field_dict["recipes"] = recipes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recipe_summary import RecipeSummary

        d = dict(src_dict)
        name = d.pop("name")

        id = d.pop("id")

        group_id = d.pop("groupId")

        slug = d.pop("slug")

        households_with_tool = cast(list[str], d.pop("householdsWithTool", UNSET))

        _recipes = d.pop("recipes", UNSET)
        recipes: list[RecipeSummary] | Unset = UNSET
        if _recipes is not UNSET:
            recipes = []
            for recipes_item_data in _recipes:
                recipes_item = RecipeSummary.from_dict(recipes_item_data)

                recipes.append(recipes_item)

        recipe_tool_response = cls(
            name=name,
            id=id,
            group_id=group_id,
            slug=slug,
            households_with_tool=households_with_tool,
            recipes=recipes,
        )

        recipe_tool_response.additional_properties = d
        return recipe_tool_response

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
