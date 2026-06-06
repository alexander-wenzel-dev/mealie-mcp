from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.recipe_output import RecipeOutput


T = TypeVar("T", bound="RecipeShareToken")


@_attrs_define
class RecipeShareToken:
    """
    Attributes:
        recipe_id (str):
        group_id (str):
        id (str):
        created_at (datetime.datetime):
        recipe (RecipeOutput):
        expires_at (datetime.datetime | Unset):
    """

    recipe_id: str
    group_id: str
    id: str
    created_at: datetime.datetime
    recipe: RecipeOutput
    expires_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_id = self.recipe_id

        group_id = self.group_id

        id = self.id

        created_at = self.created_at.isoformat()

        recipe = self.recipe.to_dict()

        expires_at: str | Unset = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipeId": recipe_id,
                "groupId": group_id,
                "id": id,
                "createdAt": created_at,
                "recipe": recipe,
            }
        )
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recipe_output import RecipeOutput

        d = dict(src_dict)
        recipe_id = d.pop("recipeId")

        group_id = d.pop("groupId")

        id = d.pop("id")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        recipe = RecipeOutput.from_dict(d.pop("recipe"))

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: datetime.datetime | Unset
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = datetime.datetime.fromisoformat(_expires_at)

        recipe_share_token = cls(
            recipe_id=recipe_id,
            group_id=group_id,
            id=id,
            created_at=created_at,
            recipe=recipe,
            expires_at=expires_at,
        )

        recipe_share_token.additional_properties = d
        return recipe_share_token

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
