from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MealPlanICalTokenOut")


@_attrs_define
class MealPlanICalTokenOut:
    """
    Attributes:
        household_id (str):
        mealplan_ical_token (None | str):
    """

    household_id: str
    mealplan_ical_token: str | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        household_id = self.household_id

        mealplan_ical_token: str | None
        mealplan_ical_token = self.mealplan_ical_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "householdId": household_id,
                "mealplanIcalToken": mealplan_ical_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        household_id = d.pop("householdId")

        def _parse_mealplan_ical_token(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        mealplan_ical_token = _parse_mealplan_ical_token(d.pop("mealplanIcalToken"))

        meal_plan_i_cal_token_out = cls(
            household_id=household_id,
            mealplan_ical_token=mealplan_ical_token,
        )

        meal_plan_i_cal_token_out.additional_properties = d
        return meal_plan_i_cal_token_out

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
