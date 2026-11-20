from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.plan_rules_day import PlanRulesDay
from ..models.plan_rules_type import PlanRulesType

if TYPE_CHECKING:
    from ..models.query_filter_json import QueryFilterJSON


T = TypeVar("T", bound="PlanRulesOut")


@_attrs_define
class PlanRulesOut:
    """
    Attributes:
        day (PlanRulesDay): The day a meal plan rule applies to, or the weekday of the meal plan entry rules are looked
            up for.

            On a rule, `unset` means the rule applies to all days. When looking up rules for an entry, `unset`
            means the entry isn't on a specific weekday (e.g. it spans a week), so only rules that apply to all
            days match it.
        entry_type (PlanRulesType):
        query_filter_string (str):  Default: ''.
        group_id (str):
        household_id (str):
        id (str):
        query_filter (QueryFilterJSON):
    """

    day: PlanRulesDay
    entry_type: PlanRulesType
    group_id: str
    household_id: str
    id: str
    query_filter: QueryFilterJSON
    query_filter_string: str = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        day = self.day.value

        entry_type = self.entry_type.value

        query_filter_string = self.query_filter_string

        group_id = self.group_id

        household_id = self.household_id

        id = self.id

        query_filter = self.query_filter.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "day": day,
                "entryType": entry_type,
                "queryFilterString": query_filter_string,
                "groupId": group_id,
                "householdId": household_id,
                "id": id,
                "queryFilter": query_filter,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.query_filter_json import QueryFilterJSON  # noqa: PLC0415

        d = dict(src_dict)
        day = PlanRulesDay(d.pop("day"))

        entry_type = PlanRulesType(d.pop("entryType"))

        query_filter_string = d.pop("queryFilterString")

        group_id = d.pop("groupId")

        household_id = d.pop("householdId")

        id = d.pop("id")

        query_filter = QueryFilterJSON.from_dict(d.pop("queryFilter"))

        plan_rules_out = cls(
            day=day,
            entry_type=entry_type,
            query_filter_string=query_filter_string,
            group_id=group_id,
            household_id=household_id,
            id=id,
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
