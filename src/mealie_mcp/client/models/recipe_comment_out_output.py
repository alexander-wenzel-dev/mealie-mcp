from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.user_base import UserBase


T = TypeVar("T", bound="RecipeCommentOutOutput")


@_attrs_define
class RecipeCommentOutOutput:
    """
    Attributes:
        recipe_id (str):
        text (str):
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        user_id (str):
        user (UserBase):
    """

    recipe_id: str
    text: str
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    user_id: str
    user: UserBase
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_id = self.recipe_id

        text = self.text

        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

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
                "updatedAt": updated_at,
                "userId": user_id,
                "user": user,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_base import UserBase

        d = dict(src_dict)
        recipe_id = d.pop("recipeId")

        text = d.pop("text")

        id = d.pop("id")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))

        user_id = d.pop("userId")

        user = UserBase.from_dict(d.pop("user"))

        recipe_comment_out_output = cls(
            recipe_id=recipe_id,
            text=text,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            user_id=user_id,
            user=user,
        )

        recipe_comment_out_output.additional_properties = d
        return recipe_comment_out_output

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
