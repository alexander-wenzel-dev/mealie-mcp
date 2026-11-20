from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UserRatingOut")


@_attrs_define
class UserRatingOut:
    """
    Attributes:
        recipe_id (str):
        rating (float | None):
        is_favorite (bool):  Default: False.
        user_id (str):
        id (str):
    """

    recipe_id: str
    rating: float | None
    user_id: str
    id: str
    is_favorite: bool = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_id = self.recipe_id

        rating: float | None
        rating = self.rating

        is_favorite = self.is_favorite

        user_id = self.user_id

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipeId": recipe_id,
                "rating": rating,
                "isFavorite": is_favorite,
                "userId": user_id,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recipe_id = d.pop("recipeId")

        def _parse_rating(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        rating = _parse_rating(d.pop("rating"))

        is_favorite = d.pop("isFavorite")

        user_id = d.pop("userId")

        id = d.pop("id")

        user_rating_out = cls(
            recipe_id=recipe_id,
            rating=rating,
            is_favorite=is_favorite,
            user_id=user_id,
            id=id,
        )

        user_rating_out.additional_properties = d
        return user_rating_out

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
