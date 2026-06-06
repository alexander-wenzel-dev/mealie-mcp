from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ingredient_food_output_extras_type_0 import IngredientFoodOutputExtrasType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ingredient_food_alias import IngredientFoodAlias
    from ..models.multi_purpose_label_summary import MultiPurposeLabelSummary


T = TypeVar("T", bound="IngredientFoodOutput")


@_attrs_define
class IngredientFoodOutput:
    """
    Attributes:
        id (str):
        name (str):
        plural_name (None | str | Unset):
        description (str | Unset):  Default: ''.
        extras (IngredientFoodOutputExtrasType0 | None | Unset):  Default: IngredientFoodOutputExtrasType0().
        label_id (None | str | Unset):
        aliases (list[IngredientFoodAlias] | Unset):
        households_with_ingredient_food (list[str] | Unset):
        label (MultiPurposeLabelSummary | None | Unset):
        created_at (datetime.datetime | None | Unset):
        updated_at (datetime.datetime | None | Unset):
    """

    id: str
    name: str
    plural_name: None | str | Unset = UNSET
    description: str | Unset = ""
    extras: IngredientFoodOutputExtrasType0 | None | Unset = IngredientFoodOutputExtrasType0()
    label_id: None | str | Unset = UNSET
    aliases: list[IngredientFoodAlias] | Unset = UNSET
    households_with_ingredient_food: list[str] | Unset = UNSET
    label: MultiPurposeLabelSummary | None | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.multi_purpose_label_summary import MultiPurposeLabelSummary

        id = self.id

        name = self.name

        plural_name: None | str | Unset
        if isinstance(self.plural_name, Unset):
            plural_name = UNSET
        else:
            plural_name = self.plural_name

        description = self.description

        extras: dict[str, Any] | None | Unset
        if isinstance(self.extras, Unset):
            extras = UNSET
        elif isinstance(self.extras, IngredientFoodOutputExtrasType0):
            extras = self.extras.to_dict()
        else:
            extras = self.extras

        label_id: None | str | Unset
        if isinstance(self.label_id, Unset):
            label_id = UNSET
        else:
            label_id = self.label_id

        aliases: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.aliases, Unset):
            aliases = []
            for aliases_item_data in self.aliases:
                aliases_item = aliases_item_data.to_dict()
                aliases.append(aliases_item)

        households_with_ingredient_food: list[str] | Unset = UNSET
        if not isinstance(self.households_with_ingredient_food, Unset):
            households_with_ingredient_food = self.households_with_ingredient_food

        label: dict[str, Any] | None | Unset
        if isinstance(self.label, Unset):
            label = UNSET
        elif isinstance(self.label, MultiPurposeLabelSummary):
            label = self.label.to_dict()
        else:
            label = self.label

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if plural_name is not UNSET:
            field_dict["pluralName"] = plural_name
        if description is not UNSET:
            field_dict["description"] = description
        if extras is not UNSET:
            field_dict["extras"] = extras
        if label_id is not UNSET:
            field_dict["labelId"] = label_id
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if households_with_ingredient_food is not UNSET:
            field_dict["householdsWithIngredientFood"] = households_with_ingredient_food
        if label is not UNSET:
            field_dict["label"] = label
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_food_alias import IngredientFoodAlias
        from ..models.multi_purpose_label_summary import MultiPurposeLabelSummary

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        def _parse_plural_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        plural_name = _parse_plural_name(d.pop("pluralName", UNSET))

        description = d.pop("description", UNSET)

        def _parse_extras(data: object) -> IngredientFoodOutputExtrasType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extras_type_0 = IngredientFoodOutputExtrasType0.from_dict(data)

                return extras_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(IngredientFoodOutputExtrasType0 | None | Unset, data)

        extras = _parse_extras(d.pop("extras", UNSET))

        def _parse_label_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        label_id = _parse_label_id(d.pop("labelId", UNSET))

        _aliases = d.pop("aliases", UNSET)
        aliases: list[IngredientFoodAlias] | Unset = UNSET
        if _aliases is not UNSET:
            aliases = []
            for aliases_item_data in _aliases:
                aliases_item = IngredientFoodAlias.from_dict(aliases_item_data)

                aliases.append(aliases_item)

        households_with_ingredient_food = cast(
            list[str], d.pop("householdsWithIngredientFood", UNSET)
        )

        def _parse_label(data: object) -> MultiPurposeLabelSummary | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                label_type_0 = MultiPurposeLabelSummary.from_dict(data)

                return label_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(MultiPurposeLabelSummary | None | Unset, data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = datetime.datetime.fromisoformat(data)

                return created_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("createdAt", UNSET))

        def _parse_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = datetime.datetime.fromisoformat(data)

                return updated_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updatedAt", UNSET))

        ingredient_food_output = cls(
            id=id,
            name=name,
            plural_name=plural_name,
            description=description,
            extras=extras,
            label_id=label_id,
            aliases=aliases,
            households_with_ingredient_food=households_with_ingredient_food,
            label=label,
            created_at=created_at,
            updated_at=updated_at,
        )

        ingredient_food_output.additional_properties = d
        return ingredient_food_output

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
