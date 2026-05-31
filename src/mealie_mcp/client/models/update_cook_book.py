from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateCookBook")


@_attrs_define
class UpdateCookBook:
    """
    Attributes:
        name (str):
        group_id (str):
        household_id (str):
        id (str):
        description (str | Unset):  Default: ''.
        slug (None | str | Unset):
        position (int | Unset):  Default: 1.
        public (bool | Unset):  Default: False.
        query_filter_string (str | Unset):  Default: ''.
    """

    name: str
    group_id: str
    household_id: str
    id: str
    description: str | Unset = ""
    slug: None | str | Unset = UNSET
    position: int | Unset = 1
    public: bool | Unset = False
    query_filter_string: str | Unset = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        group_id = self.group_id

        household_id = self.household_id

        id = self.id

        description = self.description

        slug: None | str | Unset
        if isinstance(self.slug, Unset):
            slug = UNSET
        else:
            slug = self.slug

        position = self.position

        public = self.public

        query_filter_string = self.query_filter_string

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "groupId": group_id,
                "householdId": household_id,
                "id": id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if slug is not UNSET:
            field_dict["slug"] = slug
        if position is not UNSET:
            field_dict["position"] = position
        if public is not UNSET:
            field_dict["public"] = public
        if query_filter_string is not UNSET:
            field_dict["queryFilterString"] = query_filter_string

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        group_id = d.pop("groupId")

        household_id = d.pop("householdId")

        id = d.pop("id")

        description = d.pop("description", UNSET)

        def _parse_slug(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        slug = _parse_slug(d.pop("slug", UNSET))

        position = d.pop("position", UNSET)

        public = d.pop("public", UNSET)

        query_filter_string = d.pop("queryFilterString", UNSET)

        update_cook_book = cls(
            name=name,
            group_id=group_id,
            household_id=household_id,
            id=id,
            description=description,
            slug=slug,
            position=position,
            public=public,
            query_filter_string=query_filter_string,
        )

        update_cook_book.additional_properties = d
        return update_cook_book

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
