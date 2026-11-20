from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.recipe_timeline_event_out import RecipeTimelineEventOut


T = TypeVar("T", bound="RecipeTimelineEventPagination")


@_attrs_define
class RecipeTimelineEventPagination:
    """
    Attributes:
        page (int):  Default: 1.
        per_page (int):  Default: 10.
        total (int):  Default: 0.
        total_pages (int):  Default: 0.
        items (list[RecipeTimelineEventOut]):
        next_ (None | str):
        previous (None | str):
    """

    items: list[RecipeTimelineEventOut]
    next_: str | None
    previous: str | None
    page: int = 1
    per_page: int = 10
    total: int = 0
    total_pages: int = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        page = self.page

        per_page = self.per_page

        total = self.total

        total_pages = self.total_pages

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        next_: str | None
        next_ = self.next_

        previous: str | None
        previous = self.previous

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": total_pages,
                "items": items,
                "next": next_,
                "previous": previous,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recipe_timeline_event_out import RecipeTimelineEventOut  # noqa: PLC0415

        d = dict(src_dict)
        page = d.pop("page")

        per_page = d.pop("per_page")

        total = d.pop("total")

        total_pages = d.pop("total_pages")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = RecipeTimelineEventOut.from_dict(items_item_data)

            items.append(items_item)

        def _parse_next_(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        next_ = _parse_next_(d.pop("next"))

        def _parse_previous(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        previous = _parse_previous(d.pop("previous"))

        recipe_timeline_event_pagination = cls(
            page=page,
            per_page=per_page,
            total=total,
            total_pages=total_pages,
            items=items,
            next_=next_,
            previous=previous,
        )

        recipe_timeline_event_pagination.additional_properties = d
        return recipe_timeline_event_pagination

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
