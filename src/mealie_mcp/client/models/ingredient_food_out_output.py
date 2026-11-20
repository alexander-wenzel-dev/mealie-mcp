from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ingredient_food_alias import IngredientFoodAlias
    from ..models.ingredient_food_out_output_extras_type_0 import IngredientFoodOutOutputExtrasType0
    from ..models.ingredient_food_substitution_output import IngredientFoodSubstitutionOutput
    from ..models.multi_purpose_label_summary_output import MultiPurposeLabelSummaryOutput


T = TypeVar("T", bound="IngredientFoodOutOutput")


@_attrs_define
class IngredientFoodOutOutput:
    """
    Attributes:
        id (str):
        name (str):
        plural_name (None | str):
        description (str):  Default: ''.
        extras (IngredientFoodOutOutputExtrasType0 | None):
        label_id (None | str):
        aliases (list[IngredientFoodAlias]):
        substitutions (list[IngredientFoodSubstitutionOutput]):
        households_with_ingredient_food (list[str]):
        label (MultiPurposeLabelSummaryOutput | None):
        recipe_count (int):  Default: 0.
        created_at (datetime.datetime | None):
        updated_at (datetime.datetime | None):
    """

    id: str
    name: str
    plural_name: str | None
    extras: IngredientFoodOutOutputExtrasType0 | None
    label_id: str | None
    aliases: list[IngredientFoodAlias]
    substitutions: list[IngredientFoodSubstitutionOutput]
    households_with_ingredient_food: list[str]
    label: MultiPurposeLabelSummaryOutput | None
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    description: str = ""
    recipe_count: int = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ingredient_food_out_output_extras_type_0 import (
            IngredientFoodOutOutputExtrasType0,
        )
        from ..models.multi_purpose_label_summary_output import MultiPurposeLabelSummaryOutput  # noqa: PLC0415

        id = self.id

        name = self.name

        plural_name: str | None
        plural_name = self.plural_name

        description = self.description

        extras: dict[str, Any] | None
        if isinstance(self.extras, IngredientFoodOutOutputExtrasType0):
            extras = self.extras.to_dict()
        else:
            extras = self.extras

        label_id: str | None
        label_id = self.label_id

        aliases = []
        for aliases_item_data in self.aliases:
            aliases_item = aliases_item_data.to_dict()
            aliases.append(aliases_item)

        substitutions = []
        for substitutions_item_data in self.substitutions:
            substitutions_item = substitutions_item_data.to_dict()
            substitutions.append(substitutions_item)

        households_with_ingredient_food = self.households_with_ingredient_food

        label: dict[str, Any] | None
        if isinstance(self.label, MultiPurposeLabelSummaryOutput):
            label = self.label.to_dict()
        else:
            label = self.label

        recipe_count = self.recipe_count

        created_at: str | None
        if isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: str | None
        if isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "pluralName": plural_name,
                "description": description,
                "extras": extras,
                "labelId": label_id,
                "aliases": aliases,
                "substitutions": substitutions,
                "householdsWithIngredientFood": households_with_ingredient_food,
                "label": label,
                "recipeCount": recipe_count,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_food_alias import IngredientFoodAlias  # noqa: PLC0415
        from ..models.ingredient_food_out_output_extras_type_0 import (
            IngredientFoodOutOutputExtrasType0,
        )
        from ..models.ingredient_food_substitution_output import IngredientFoodSubstitutionOutput  # noqa: PLC0415
        from ..models.multi_purpose_label_summary_output import MultiPurposeLabelSummaryOutput  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        def _parse_plural_name(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        plural_name = _parse_plural_name(d.pop("pluralName"))

        description = d.pop("description")

        def _parse_extras(data: object) -> IngredientFoodOutOutputExtrasType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extras_type_0 = IngredientFoodOutOutputExtrasType0.from_dict(data)

                return extras_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(IngredientFoodOutOutputExtrasType0 | None, data)

        extras = _parse_extras(d.pop("extras"))

        def _parse_label_id(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        label_id = _parse_label_id(d.pop("labelId"))

        aliases = []
        _aliases = d.pop("aliases")
        for aliases_item_data in _aliases:
            aliases_item = IngredientFoodAlias.from_dict(aliases_item_data)

            aliases.append(aliases_item)

        substitutions = []
        _substitutions = d.pop("substitutions")
        for substitutions_item_data in _substitutions:
            substitutions_item = IngredientFoodSubstitutionOutput.from_dict(substitutions_item_data)

            substitutions.append(substitutions_item)

        households_with_ingredient_food = cast(list[str], d.pop("householdsWithIngredientFood"))

        def _parse_label(data: object) -> MultiPurposeLabelSummaryOutput | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                label_type_0 = MultiPurposeLabelSummaryOutput.from_dict(data)

                return label_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(MultiPurposeLabelSummaryOutput | None, data)

        label = _parse_label(d.pop("label"))

        recipe_count = d.pop("recipeCount")

        def _parse_created_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = datetime.datetime.fromisoformat(data)

                return created_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None, data)

        created_at = _parse_created_at(d.pop("createdAt"))

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

        ingredient_food_out_output = cls(
            id=id,
            name=name,
            plural_name=plural_name,
            description=description,
            extras=extras,
            label_id=label_id,
            aliases=aliases,
            substitutions=substitutions,
            households_with_ingredient_food=households_with_ingredient_food,
            label=label,
            recipe_count=recipe_count,
            created_at=created_at,
            updated_at=updated_at,
        )

        ingredient_food_out_output.additional_properties = d
        return ingredient_food_out_output

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
