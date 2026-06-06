from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.mealie_schema_recipe_recipe_comments_user_base import (
        MealieSchemaRecipeRecipeCommentsUserBase,
    )


T = TypeVar("T", bound="RecipeCommentOut")


@_attrs_define
class RecipeCommentOut:
    """
    Attributes:
        recipe_id (str):
        text (str):
        id (str):
        created_at (datetime.datetime):
        update_at (datetime.datetime):
        user_id (str):
        user (MealieSchemaRecipeRecipeCommentsUserBase):
    """

    recipe_id: str
    text: str
    id: str
    created_at: datetime.datetime
    update_at: datetime.datetime
    user_id: str
    user: MealieSchemaRecipeRecipeCommentsUserBase
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_id = self.recipe_id

        text = self.text

        id = self.id

        created_at = self.created_at.isoformat()

        update_at = self.update_at.isoformat()

        user_id = self.user_id

        user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipeId": recipe_id,
                "text": text,
                "id": id,
                "createdAt": created_at,
                "update_at": update_at,
                "userId": user_id,
                "user": user,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mealie_schema_recipe_recipe_comments_user_base import (
            MealieSchemaRecipeRecipeCommentsUserBase,
        )

        d = dict(src_dict)
        recipe_id = d.pop("recipeId")

        text = d.pop("text")

        id = d.pop("id")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        update_at = datetime.datetime.fromisoformat(d.pop("update_at"))

        user_id = d.pop("userId")

        user = MealieSchemaRecipeRecipeCommentsUserBase.from_dict(d.pop("user"))

        recipe_comment_out = cls(
            recipe_id=recipe_id,
            text=text,
            id=id,
            created_at=created_at,
            update_at=update_at,
            user_id=user_id,
            user=user,
        )

        recipe_comment_out.additional_properties = d
        return recipe_comment_out

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
