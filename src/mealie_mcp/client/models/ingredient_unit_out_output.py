from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ingredient_unit_alias import IngredientUnitAlias
    from ..models.ingredient_unit_out_output_extras_type_0 import IngredientUnitOutOutputExtrasType0


T = TypeVar("T", bound="IngredientUnitOutOutput")


@_attrs_define
class IngredientUnitOutOutput:
    """
    Attributes:
        id (str):
        name (str):
        plural_name (None | str):
        description (str):  Default: ''.
        extras (IngredientUnitOutOutputExtrasType0 | None):
        fraction (bool):  Default: True.
        abbreviation (str):  Default: ''.
        plural_abbreviation (None | str):  Default: ''.
        use_abbreviation (bool):  Default: False.
        aliases (list[IngredientUnitAlias]):
        standard_quantity (float | None):
        standard_unit (None | str):
        created_at (datetime.datetime | None):
        updated_at (datetime.datetime | None):
    """

    id: str
    name: str
    plural_name: str | None
    extras: IngredientUnitOutOutputExtrasType0 | None
    aliases: list[IngredientUnitAlias]
    standard_quantity: float | None
    standard_unit: str | None
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    description: str = ""
    fraction: bool = True
    abbreviation: str = ""
    plural_abbreviation: str | None = ""
    use_abbreviation: bool = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ingredient_unit_out_output_extras_type_0 import (
            IngredientUnitOutOutputExtrasType0,
        )

        id = self.id

        name = self.name

        plural_name: str | None
        plural_name = self.plural_name

        description = self.description

        extras: dict[str, Any] | None
        if isinstance(self.extras, IngredientUnitOutOutputExtrasType0):
            extras = self.extras.to_dict()
        else:
            extras = self.extras

        fraction = self.fraction

        abbreviation = self.abbreviation

        plural_abbreviation: str | None
        plural_abbreviation = self.plural_abbreviation

        use_abbreviation = self.use_abbreviation

        aliases = []
        for aliases_item_data in self.aliases:
            aliases_item = aliases_item_data.to_dict()
            aliases.append(aliases_item)

        standard_quantity: float | None
        standard_quantity = self.standard_quantity

        standard_unit: str | None
        standard_unit = self.standard_unit

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
                "fraction": fraction,
                "abbreviation": abbreviation,
                "pluralAbbreviation": plural_abbreviation,
                "useAbbreviation": use_abbreviation,
                "aliases": aliases,
                "standardQuantity": standard_quantity,
                "standardUnit": standard_unit,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_unit_alias import IngredientUnitAlias  # noqa: PLC0415
        from ..models.ingredient_unit_out_output_extras_type_0 import (
            IngredientUnitOutOutputExtrasType0,
        )

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        def _parse_plural_name(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        plural_name = _parse_plural_name(d.pop("pluralName"))

        description = d.pop("description")

        def _parse_extras(data: object) -> IngredientUnitOutOutputExtrasType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extras_type_0 = IngredientUnitOutOutputExtrasType0.from_dict(data)

                return extras_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(IngredientUnitOutOutputExtrasType0 | None, data)

        extras = _parse_extras(d.pop("extras"))

        fraction = d.pop("fraction")

        abbreviation = d.pop("abbreviation")

        def _parse_plural_abbreviation(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        plural_abbreviation = _parse_plural_abbreviation(d.pop("pluralAbbreviation"))

        use_abbreviation = d.pop("useAbbreviation")

        aliases = []
        _aliases = d.pop("aliases")
        for aliases_item_data in _aliases:
            aliases_item = IngredientUnitAlias.from_dict(aliases_item_data)

            aliases.append(aliases_item)

        def _parse_standard_quantity(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        standard_quantity = _parse_standard_quantity(d.pop("standardQuantity"))

        def _parse_standard_unit(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        standard_unit = _parse_standard_unit(d.pop("standardUnit"))

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

        ingredient_unit_out_output = cls(
            id=id,
            name=name,
            plural_name=plural_name,
            description=description,
            extras=extras,
            fraction=fraction,
            abbreviation=abbreviation,
            plural_abbreviation=plural_abbreviation,
            use_abbreviation=use_abbreviation,
            aliases=aliases,
            standard_quantity=standard_quantity,
            standard_unit=standard_unit,
            created_at=created_at,
            updated_at=updated_at,
        )

        ingredient_unit_out_output.additional_properties = d
        return ingredient_unit_out_output

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
