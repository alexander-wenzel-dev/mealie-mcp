from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.user_rating_summary import UserRatingSummary


T = TypeVar("T", bound="UserRatingsUserRatingSummary")


@_attrs_define
class UserRatingsUserRatingSummary:
    """
    Attributes:
        ratings (list[UserRatingSummary]):
    """

    ratings: list[UserRatingSummary]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ratings = []
        for ratings_item_data in self.ratings:
            ratings_item = ratings_item_data.to_dict()
            ratings.append(ratings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ratings": ratings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_rating_summary import UserRatingSummary

        d = dict(src_dict)
        ratings = []
        _ratings = d.pop("ratings")
        for ratings_item_data in _ratings:
            ratings_item = UserRatingSummary.from_dict(ratings_item_data)

            ratings.append(ratings_item)

        user_ratings_user_rating_summary = cls(
            ratings=ratings,
        )

        user_ratings_user_rating_summary.additional_properties = d
        return user_ratings_user_rating_summary

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
