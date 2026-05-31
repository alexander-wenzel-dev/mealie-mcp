from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cookbook_household import CookbookHousehold
    from ..models.query_filter_json import QueryFilterJSON


T = TypeVar("T", bound="ReadCookBook")


@_attrs_define
class ReadCookBook:
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
        query_filter (QueryFilterJSON | Unset):
        household (CookbookHousehold | None | Unset):
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
    query_filter: QueryFilterJSON | Unset = UNSET
    household: CookbookHousehold | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.cookbook_household import CookbookHousehold

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

        query_filter: dict[str, Any] | Unset = UNSET
        if not isinstance(self.query_filter, Unset):
            query_filter = self.query_filter.to_dict()

        household: dict[str, Any] | None | Unset
        if isinstance(self.household, Unset):
            household = UNSET
        elif isinstance(self.household, CookbookHousehold):
            household = self.household.to_dict()
        else:
            household = self.household

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
        if query_filter is not UNSET:
            field_dict["queryFilter"] = query_filter
        if household is not UNSET:
            field_dict["household"] = household

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cookbook_household import CookbookHousehold
        from ..models.query_filter_json import QueryFilterJSON

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

        _query_filter = d.pop("queryFilter", UNSET)
        query_filter: QueryFilterJSON | Unset
        if isinstance(_query_filter, Unset):
            query_filter = UNSET
        else:
            query_filter = QueryFilterJSON.from_dict(_query_filter)

        def _parse_household(data: object) -> CookbookHousehold | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                household_type_0 = CookbookHousehold.from_dict(data)

                return household_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(CookbookHousehold | None | Unset, data)

        household = _parse_household(d.pop("household", UNSET))

        read_cook_book = cls(
            name=name,
            group_id=group_id,
            household_id=household_id,
            id=id,
            description=description,
            slug=slug,
            position=position,
            public=public,
            query_filter_string=query_filter_string,
            query_filter=query_filter,
            household=household,
        )

        read_cook_book.additional_properties = d
        return read_cook_book

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
