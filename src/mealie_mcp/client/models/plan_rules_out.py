from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.plan_rules_day import PlanRulesDay
from ..models.plan_rules_type import PlanRulesType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.query_filter_json import QueryFilterJSON


T = TypeVar("T", bound="PlanRulesOut")


@_attrs_define
class PlanRulesOut:
    """
    Attributes:
        group_id (str):
        household_id (str):
        id (str):
        day (PlanRulesDay | Unset):
        entry_type (PlanRulesType | Unset):
        query_filter_string (str | Unset):  Default: ''.
        query_filter (QueryFilterJSON | Unset):
    """

    group_id: str
    household_id: str
    id: str
    day: PlanRulesDay | Unset = UNSET
    entry_type: PlanRulesType | Unset = UNSET
    query_filter_string: str | Unset = ""
    query_filter: QueryFilterJSON | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        group_id = self.group_id

        household_id = self.household_id

        id = self.id

        day: str | Unset = UNSET
        if not isinstance(self.day, Unset):
            day = self.day.value

        entry_type: str | Unset = UNSET
        if not isinstance(self.entry_type, Unset):
            entry_type = self.entry_type.value

        query_filter_string = self.query_filter_string

        query_filter: dict[str, Any] | Unset = UNSET
        if not isinstance(self.query_filter, Unset):
            query_filter = self.query_filter.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "groupId": group_id,
                "householdId": household_id,
                "id": id,
            }
        )
        if day is not UNSET:
            field_dict["day"] = day
        if entry_type is not UNSET:
            field_dict["entryType"] = entry_type
        if query_filter_string is not UNSET:
            field_dict["queryFilterString"] = query_filter_string
        if query_filter is not UNSET:
            field_dict["queryFilter"] = query_filter

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.query_filter_json import QueryFilterJSON

        d = dict(src_dict)
        group_id = d.pop("groupId")

        household_id = d.pop("householdId")

        id = d.pop("id")

        _day = d.pop("day", UNSET)
        day: PlanRulesDay | Unset
        if isinstance(_day, Unset):
            day = UNSET
        else:
            day = PlanRulesDay(_day)

        _entry_type = d.pop("entryType", UNSET)
        entry_type: PlanRulesType | Unset
        if isinstance(_entry_type, Unset):
            entry_type = UNSET
        else:
            entry_type = PlanRulesType(_entry_type)

        query_filter_string = d.pop("queryFilterString", UNSET)

        _query_filter = d.pop("queryFilter", UNSET)
        query_filter: QueryFilterJSON | Unset
        if isinstance(_query_filter, Unset):
            query_filter = UNSET
        else:
            query_filter = QueryFilterJSON.from_dict(_query_filter)

        plan_rules_out = cls(
            group_id=group_id,
            household_id=household_id,
            id=id,
            day=day,
            entry_type=entry_type,
            query_filter_string=query_filter_string,
            query_filter=query_filter,
        )

        plan_rules_out.additional_properties = d
        return plan_rules_out

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
