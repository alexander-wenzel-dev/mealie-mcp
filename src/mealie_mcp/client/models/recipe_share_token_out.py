from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.recipe_out import RecipeOut


T = TypeVar("T", bound="RecipeShareTokenOut")


@_attrs_define
class RecipeShareTokenOut:
    """
    Attributes:
        recipe_id (str):
        expires_at (datetime.datetime):
        group_id (str):
        id (str):
        created_at (datetime.datetime):
        recipe (RecipeOut): A saved recipe with all of its details.
    """

    recipe_id: str
    expires_at: datetime.datetime
    group_id: str
    id: str
    created_at: datetime.datetime
    recipe: RecipeOut
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_id = self.recipe_id

        expires_at = self.expires_at.isoformat()

        group_id = self.group_id

        id = self.id

        created_at = self.created_at.isoformat()

        recipe = self.recipe.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipeId": recipe_id,
                "expiresAt": expires_at,
                "groupId": group_id,
                "id": id,
                "createdAt": created_at,
                "recipe": recipe,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recipe_out import RecipeOut  # noqa: PLC0415

        d = dict(src_dict)
        recipe_id = d.pop("recipeId")

        expires_at = datetime.datetime.fromisoformat(d.pop("expiresAt"))

        group_id = d.pop("groupId")

        id = d.pop("id")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        recipe = RecipeOut.from_dict(d.pop("recipe"))

        recipe_share_token_out = cls(
            recipe_id=recipe_id,
            expires_at=expires_at,
            group_id=group_id,
            id=id,
            created_at=created_at,
            recipe=recipe,
        )

        recipe_share_token_out.additional_properties = d
        return recipe_share_token_out

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
