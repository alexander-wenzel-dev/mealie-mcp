from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.recipe_summary import RecipeSummary


T = TypeVar("T", bound="RecipeTagResponse")


@_attrs_define
class RecipeTagResponse:
    """
    Attributes:
        name (str):
        id (str):
        slug (str):
        group_id (None | str | Unset):
        recipes (list[RecipeSummary] | Unset):
    """

    name: str
    id: str
    slug: str
    group_id: None | str | Unset = UNSET
    recipes: list[RecipeSummary] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        id = self.id

        slug = self.slug

        group_id: None | str | Unset
        if isinstance(self.group_id, Unset):
            group_id = UNSET
        else:
            group_id = self.group_id

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
                "slug": slug,
            }
        )
        if group_id is not UNSET:
            field_dict["groupId"] = group_id
        if recipes is not UNSET:
            field_dict["recipes"] = recipes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recipe_summary import RecipeSummary

        d = dict(src_dict)
        name = d.pop("name")

        id = d.pop("id")

        slug = d.pop("slug")

        def _parse_group_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        group_id = _parse_group_id(d.pop("groupId", UNSET))

        _recipes = d.pop("recipes", UNSET)
        recipes: list[RecipeSummary] | Unset = UNSET
        if _recipes is not UNSET:
            recipes = []
            for recipes_item_data in _recipes:
                recipes_item = RecipeSummary.from_dict(recipes_item_data)

                recipes.append(recipes_item)

        recipe_tag_response = cls(
            name=name,
            id=id,
            slug=slug,
            group_id=group_id,
            recipes=recipes,
        )

        recipe_tag_response.additional_properties = d
        return recipe_tag_response

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
