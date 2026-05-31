from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.recipe_category import RecipeCategory


T = TypeVar("T", bound="PaginationBaseRecipeCategory")


@_attrs_define
class PaginationBaseRecipeCategory:
    """
    Attributes:
        items (list[RecipeCategory]):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 10.
        total (int | Unset):  Default: 0.
        total_pages (int | Unset):  Default: 0.
        next_ (None | str | Unset):
        previous (None | str | Unset):
    """

    items: list[RecipeCategory]
    page: int | Unset = 1
    per_page: int | Unset = 10
    total: int | Unset = 0
    total_pages: int | Unset = 0
    next_: None | str | Unset = UNSET
    previous: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        page = self.page

        per_page = self.per_page

        total = self.total

        total_pages = self.total_pages

        next_: None | str | Unset
        if isinstance(self.next_, Unset):
            next_ = UNSET
        else:
            next_ = self.next_

        previous: None | str | Unset
        if isinstance(self.previous, Unset):
            previous = UNSET
        else:
            previous = self.previous

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
            }
        )
        if page is not UNSET:
            field_dict["page"] = page
        if per_page is not UNSET:
            field_dict["per_page"] = per_page
        if total is not UNSET:
            field_dict["total"] = total
        if total_pages is not UNSET:
            field_dict["total_pages"] = total_pages
        if next_ is not UNSET:
            field_dict["next"] = next_
        if previous is not UNSET:
            field_dict["previous"] = previous

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recipe_category import RecipeCategory

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = RecipeCategory.from_dict(items_item_data)

            items.append(items_item)

        page = d.pop("page", UNSET)

        per_page = d.pop("per_page", UNSET)

        total = d.pop("total", UNSET)

        total_pages = d.pop("total_pages", UNSET)

        def _parse_next_(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        next_ = _parse_next_(d.pop("next", UNSET))

        def _parse_previous(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        previous = _parse_previous(d.pop("previous", UNSET))

        pagination_base_recipe_category = cls(
            items=items,
            page=page,
            per_page=per_page,
            total=total,
            total_pages=total_pages,
            next_=next_,
            previous=previous,
        )

        pagination_base_recipe_category.additional_properties = d
        return pagination_base_recipe_category

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
