from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HouseholdRecipeSummary")


@_attrs_define
class HouseholdRecipeSummary:
    """
    Attributes:
        recipe_id (str):
        last_made (datetime.datetime | None | Unset):
    """

    recipe_id: str
    last_made: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_id = self.recipe_id

        last_made: None | str | Unset
        if isinstance(self.last_made, Unset):
            last_made = UNSET
        elif isinstance(self.last_made, datetime.datetime):
            last_made = self.last_made.isoformat()
        else:
            last_made = self.last_made

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipeId": recipe_id,
            }
        )
        if last_made is not UNSET:
            field_dict["lastMade"] = last_made

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recipe_id = d.pop("recipeId")

        def _parse_last_made(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_made_type_0 = datetime.datetime.fromisoformat(data)

                return last_made_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_made = _parse_last_made(d.pop("lastMade", UNSET))

        household_recipe_summary = cls(
            recipe_id=recipe_id,
            last_made=last_made,
        )

        household_recipe_summary.additional_properties = d
        return household_recipe_summary

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
