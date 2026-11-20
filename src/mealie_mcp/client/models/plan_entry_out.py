from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.plan_entry_type import PlanEntryType

if TYPE_CHECKING:
    from ..models.recipe_summary import RecipeSummary


T = TypeVar("T", bound="PlanEntryOut")


@_attrs_define
class PlanEntryOut:
    """
    Attributes:
        date (datetime.date):
        end_date (datetime.date | None):
        entry_type (PlanEntryType):
        title (str):  Default: ''.
        text (str):  Default: ''.
        recipe_id (None | UUID):
        recipe_scale (float):  Default: 1.0.
        id (int):
        group_id (UUID):
        user_id (UUID):
        household_id (UUID):
        recipe (None | RecipeSummary):
        updated_at (datetime.datetime | None):
    """

    date: datetime.date
    end_date: datetime.date | None
    entry_type: PlanEntryType
    recipe_id: UUID | None
    id: int
    group_id: UUID
    user_id: UUID
    household_id: UUID
    recipe: RecipeSummary | None
    updated_at: datetime.datetime | None
    title: str = ""
    text: str = ""
    recipe_scale: float = 1.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.recipe_summary import RecipeSummary  # noqa: PLC0415

        date = self.date.isoformat()

        end_date: str | None
        if isinstance(self.end_date, datetime.date):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date

        entry_type = self.entry_type.value

        title = self.title

        text = self.text

        recipe_id: str | None
        if isinstance(self.recipe_id, UUID):
            recipe_id = str(self.recipe_id)
        else:
            recipe_id = self.recipe_id

        recipe_scale = self.recipe_scale

        id = self.id

        group_id = str(self.group_id)

        user_id = str(self.user_id)

        household_id = str(self.household_id)

        recipe: dict[str, Any] | None
        if isinstance(self.recipe, RecipeSummary):
            recipe = self.recipe.to_dict()
        else:
            recipe = self.recipe

        updated_at: str | None
        if isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "endDate": end_date,
                "entryType": entry_type,
                "title": title,
                "text": text,
                "recipeId": recipe_id,
                "recipeScale": recipe_scale,
                "id": id,
                "groupId": group_id,
                "userId": user_id,
                "householdId": household_id,
                "recipe": recipe,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recipe_summary import RecipeSummary  # noqa: PLC0415

        d = dict(src_dict)
        date = datetime.date.fromisoformat(d.pop("date"))

        def _parse_end_date(data: object) -> datetime.date | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = datetime.date.fromisoformat(data)

                return end_date_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.date | None, data)

        end_date = _parse_end_date(d.pop("endDate"))

        entry_type = PlanEntryType(d.pop("entryType"))

        title = d.pop("title")

        text = d.pop("text")

        def _parse_recipe_id(data: object) -> UUID | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                recipe_id_type_0 = UUID(data)

                return recipe_id_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | UUID, data)

        recipe_id = _parse_recipe_id(d.pop("recipeId"))

        recipe_scale = d.pop("recipeScale")

        id = d.pop("id")

        group_id = UUID(d.pop("groupId"))

        user_id = UUID(d.pop("userId"))

        household_id = UUID(d.pop("householdId"))

        def _parse_recipe(data: object) -> RecipeSummary | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                recipe_type_0 = RecipeSummary.from_dict(data)

                return recipe_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | RecipeSummary, data)

        recipe = _parse_recipe(d.pop("recipe"))

        def _parse_updated_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = datetime.datetime.fromisoformat(data)

                return updated_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None, data)

        updated_at = _parse_updated_at(d.pop("updatedAt"))

        plan_entry_out = cls(
            date=date,
            end_date=end_date,
            entry_type=entry_type,
            title=title,
            text=text,
            recipe_id=recipe_id,
            recipe_scale=recipe_scale,
            id=id,
            group_id=group_id,
            user_id=user_id,
            household_id=household_id,
            recipe=recipe,
            updated_at=updated_at,
        )

        plan_entry_out.additional_properties = d
        return plan_entry_out

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
