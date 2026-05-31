from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserRatingUpdate")


@_attrs_define
class UserRatingUpdate:
    """
    Attributes:
        rating (float | None | Unset):
        is_favorite (bool | None | Unset):
    """

    rating: float | None | Unset = UNSET
    is_favorite: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rating: float | None | Unset
        if isinstance(self.rating, Unset):
            rating = UNSET
        else:
            rating = self.rating

        is_favorite: bool | None | Unset
        if isinstance(self.is_favorite, Unset):
            is_favorite = UNSET
        else:
            is_favorite = self.is_favorite

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if rating is not UNSET:
            field_dict["rating"] = rating
        if is_favorite is not UNSET:
            field_dict["isFavorite"] = is_favorite

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_rating(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        rating = _parse_rating(d.pop("rating", UNSET))

        def _parse_is_favorite(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_favorite = _parse_is_favorite(d.pop("isFavorite", UNSET))

        user_rating_update = cls(
            rating=rating,
            is_favorite=is_favorite,
        )

        user_rating_update.additional_properties = d
        return user_rating_update

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
