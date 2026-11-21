from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cookbook_household import CookbookHousehold
    from ..models.query_filter_json import QueryFilterJSON


T = TypeVar("T", bound="CookBookOut")


@_attrs_define
class CookBookOut:
    """
    Attributes:
        name (str):
        description (str):  Default: ''.
        slug (None | str):
        position (int):  Default: 1.
        public (bool):  Default: False.
        query_filter_string (str):  Default: ''.
        group_id (str):
        household_id (str):
        id (str):
        query_filter (QueryFilterJSON):
        household (CookbookHousehold | None):
    """

    name: str
    slug: str | None
    group_id: str
    household_id: str
    id: str
    query_filter: QueryFilterJSON
    household: CookbookHousehold | None
    description: str = ""
    position: int = 1
    public: bool = False
    query_filter_string: str = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.cookbook_household import CookbookHousehold  # noqa: PLC0415

        name = self.name

        description = self.description

        slug: str | None
        slug = self.slug

        position = self.position

        public = self.public

        query_filter_string = self.query_filter_string

        group_id = self.group_id

        household_id = self.household_id

        id = self.id

        query_filter = self.query_filter.to_dict()

        household: dict[str, Any] | None
        if isinstance(self.household, CookbookHousehold):
            household = self.household.to_dict()
        else:
            household = self.household

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "slug": slug,
                "position": position,
                "public": public,
                "queryFilterString": query_filter_string,
                "groupId": group_id,
                "householdId": household_id,
                "id": id,
                "queryFilter": query_filter,
                "household": household,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cookbook_household import CookbookHousehold  # noqa: PLC0415
        from ..models.query_filter_json import QueryFilterJSON  # noqa: PLC0415

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        def _parse_slug(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        slug = _parse_slug(d.pop("slug"))

        position = d.pop("position")

        public = d.pop("public")

        query_filter_string = d.pop("queryFilterString")

        group_id = d.pop("groupId")

        household_id = d.pop("householdId")

        id = d.pop("id")

        query_filter = QueryFilterJSON.from_dict(d.pop("queryFilter"))

        def _parse_household(data: object) -> CookbookHousehold | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                household_type_0 = CookbookHousehold.from_dict(data)

                return household_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(CookbookHousehold | None, data)

        household = _parse_household(d.pop("household"))

        cook_book_out = cls(
            name=name,
            description=description,
            slug=slug,
            position=position,
            public=public,
            query_filter_string=query_filter_string,
            group_id=group_id,
            household_id=household_id,
            id=id,
            query_filter=query_filter,
            household=household,
        )

        cook_book_out.additional_properties = d
        return cook_book_out

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
