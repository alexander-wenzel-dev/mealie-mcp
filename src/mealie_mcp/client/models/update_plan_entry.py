from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.plan_entry_type import PlanEntryType
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdatePlanEntry")


@_attrs_define
class UpdatePlanEntry:
    """
    Attributes:
        date (datetime.date):
        id (int):
        group_id (UUID):
        user_id (UUID):
        entry_type (PlanEntryType | Unset):
        title (str | Unset):  Default: ''.
        text (str | Unset):  Default: ''.
        recipe_id (None | Unset | UUID):
    """

    date: datetime.date
    id: int
    group_id: UUID
    user_id: UUID
    entry_type: PlanEntryType | Unset = UNSET
    title: str | Unset = ""
    text: str | Unset = ""
    recipe_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date.isoformat()

        id = self.id

        group_id = str(self.group_id)

        user_id = str(self.user_id)

        entry_type: str | Unset = UNSET
        if not isinstance(self.entry_type, Unset):
            entry_type = self.entry_type.value

        title = self.title

        text = self.text

        recipe_id: None | str | Unset
        if isinstance(self.recipe_id, Unset):
            recipe_id = UNSET
        elif isinstance(self.recipe_id, UUID):
            recipe_id = str(self.recipe_id)
        else:
            recipe_id = self.recipe_id

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
        if entry_type is not UNSET:
            field_dict["entryType"] = entry_type
        if title is not UNSET:
            field_dict["title"] = title
        if text is not UNSET:
            field_dict["text"] = text
        if recipe_id is not UNSET:
            field_dict["recipeId"] = recipe_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = datetime.date.fromisoformat(d.pop("date"))

        id = d.pop("id")

        group_id = UUID(d.pop("groupId"))

        user_id = UUID(d.pop("userId"))

        _entry_type = d.pop("entryType", UNSET)
        entry_type: PlanEntryType | Unset
        if isinstance(_entry_type, Unset):
            entry_type = UNSET
        else:
            entry_type = PlanEntryType(_entry_type)

        title = d.pop("title", UNSET)

        text = d.pop("text", UNSET)

        def _parse_recipe_id(data: object) -> None | Unset | UUID:
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

        update_plan_entry = cls(
            date=date,
            id=id,
            group_id=group_id,
            user_id=user_id,
            entry_type=entry_type,
            title=title,
            text=text,
            recipe_id=recipe_id,
        )

        update_plan_entry.additional_properties = d
        return update_plan_entry

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
