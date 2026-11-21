from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.plan_entry_type import PlanEntryType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PlanEntryUpdate")


@_attrs_define
class PlanEntryUpdate:
    """
    Attributes:
        date (datetime.date):
        id (int):
        group_id (UUID):
        user_id (UUID):
        end_date (datetime.date | None | Unset):
        entry_type (PlanEntryType | Unset):
        title (str | Unset):  Default: ''.
        text (str | Unset):  Default: ''.
        recipe_id (None | Unset | UUID):
        recipe_scale (float | Unset):  Default: 1.0.
    """

    date: datetime.date
    id: int
    group_id: UUID
    user_id: UUID
    end_date: datetime.date | Unset | None = UNSET
    entry_type: PlanEntryType | Unset = UNSET
    title: str | Unset = ""
    text: str | Unset = ""
    recipe_id: Unset | UUID | None = UNSET
    recipe_scale: float | Unset = 1.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date.isoformat()

        id = self.id

        group_id = str(self.group_id)

        user_id = str(self.user_id)

        end_date: str | Unset | None
        if isinstance(self.end_date, Unset):
            end_date = UNSET
        elif isinstance(self.end_date, datetime.date):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date

        entry_type: str | Unset = UNSET
        if not isinstance(self.entry_type, Unset):
            entry_type = self.entry_type.value

        title = self.title

        text = self.text

        recipe_id: str | Unset | None
        if isinstance(self.recipe_id, Unset):
            recipe_id = UNSET
        elif isinstance(self.recipe_id, UUID):
            recipe_id = str(self.recipe_id)
        else:
            recipe_id = self.recipe_id

        recipe_scale = self.recipe_scale

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "id": id,
                "groupId": group_id,
                "userId": user_id,
            }
        )
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if entry_type is not UNSET:
            field_dict["entryType"] = entry_type
        if title is not UNSET:
            field_dict["title"] = title
        if text is not UNSET:
            field_dict["text"] = text
        if recipe_id is not UNSET:
            field_dict["recipeId"] = recipe_id
        if recipe_scale is not UNSET:
            field_dict["recipeScale"] = recipe_scale

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = datetime.date.fromisoformat(d.pop("date"))

        id = d.pop("id")

        group_id = UUID(d.pop("groupId"))

        user_id = UUID(d.pop("userId"))

        def _parse_end_date(data: object) -> datetime.date | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = datetime.date.fromisoformat(data)

                return end_date_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.date | None | Unset, data)

        end_date = _parse_end_date(d.pop("endDate", UNSET))

        _entry_type = d.pop("entryType", UNSET)
        entry_type: PlanEntryType | Unset
        if isinstance(_entry_type, Unset):
            entry_type = UNSET
        else:
            entry_type = PlanEntryType(_entry_type)

        title = d.pop("title", UNSET)

        text = d.pop("text", UNSET)

        def _parse_recipe_id(data: object) -> Unset | UUID | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                recipe_id_type_0 = UUID(data)

                return recipe_id_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | Unset | UUID, data)

        recipe_id = _parse_recipe_id(d.pop("recipeId", UNSET))

        recipe_scale = d.pop("recipeScale", UNSET)

        plan_entry_update = cls(
            date=date,
            id=id,
            group_id=group_id,
            user_id=user_id,
            end_date=end_date,
            entry_type=entry_type,
            title=title,
            text=text,
            recipe_id=recipe_id,
            recipe_scale=recipe_scale,
        )

        plan_entry_update.additional_properties = d
        return plan_entry_update

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
