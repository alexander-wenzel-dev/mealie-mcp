from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_ingredient_unit_extras_type_0 import CreateIngredientUnitExtrasType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_ingredient_unit_alias import CreateIngredientUnitAlias


T = TypeVar("T", bound="CreateIngredientUnit")


@_attrs_define
class CreateIngredientUnit:
    """
    Attributes:
        name (str):
        id (None | str | Unset):
        plural_name (None | str | Unset):
        description (str | Unset):  Default: ''.
        extras (CreateIngredientUnitExtrasType0 | None | Unset):  Default: CreateIngredientUnitExtrasType0().
        fraction (bool | Unset):  Default: True.
        abbreviation (str | Unset):  Default: ''.
        plural_abbreviation (None | str | Unset):  Default: ''.
        use_abbreviation (bool | Unset):  Default: False.
        aliases (list[CreateIngredientUnitAlias] | Unset):
        standard_quantity (float | None | Unset):
        standard_unit (None | str | Unset):
    """

    name: str
    id: None | str | Unset = UNSET
    plural_name: None | str | Unset = UNSET
    description: str | Unset = ""
    extras: CreateIngredientUnitExtrasType0 | None | Unset = CreateIngredientUnitExtrasType0()
    fraction: bool | Unset = True
    abbreviation: str | Unset = ""
    plural_abbreviation: None | str | Unset = ""
    use_abbreviation: bool | Unset = False
    aliases: list[CreateIngredientUnitAlias] | Unset = UNSET
    standard_quantity: float | None | Unset = UNSET
    standard_unit: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        plural_name: None | str | Unset
        if isinstance(self.plural_name, Unset):
            plural_name = UNSET
        else:
            plural_name = self.plural_name

        description = self.description

        extras: dict[str, Any] | None | Unset
        if isinstance(self.extras, Unset):
            extras = UNSET
        elif isinstance(self.extras, CreateIngredientUnitExtrasType0):
            extras = self.extras.to_dict()
        else:
            extras = self.extras

        fraction = self.fraction

        abbreviation = self.abbreviation

        plural_abbreviation: None | str | Unset
        if isinstance(self.plural_abbreviation, Unset):
            plural_abbreviation = UNSET
        else:
            plural_abbreviation = self.plural_abbreviation

        use_abbreviation = self.use_abbreviation

        aliases: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.aliases, Unset):
            aliases = []
            for aliases_item_data in self.aliases:
                aliases_item = aliases_item_data.to_dict()
                aliases.append(aliases_item)

        standard_quantity: float | None | Unset
        if isinstance(self.standard_quantity, Unset):
            standard_quantity = UNSET
        else:
            standard_quantity = self.standard_quantity

        standard_unit: None | str | Unset
        if isinstance(self.standard_unit, Unset):
            standard_unit = UNSET
        else:
            standard_unit = self.standard_unit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if plural_name is not UNSET:
            field_dict["pluralName"] = plural_name
        if description is not UNSET:
            field_dict["description"] = description
        if extras is not UNSET:
            field_dict["extras"] = extras
        if fraction is not UNSET:
            field_dict["fraction"] = fraction
        if abbreviation is not UNSET:
            field_dict["abbreviation"] = abbreviation
        if plural_abbreviation is not UNSET:
            field_dict["pluralAbbreviation"] = plural_abbreviation
        if use_abbreviation is not UNSET:
            field_dict["useAbbreviation"] = use_abbreviation
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if standard_quantity is not UNSET:
            field_dict["standardQuantity"] = standard_quantity
        if standard_unit is not UNSET:
            field_dict["standardUnit"] = standard_unit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_ingredient_unit_alias import CreateIngredientUnitAlias

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_plural_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        plural_name = _parse_plural_name(d.pop("pluralName", UNSET))

        description = d.pop("description", UNSET)

        def _parse_extras(data: object) -> CreateIngredientUnitExtrasType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extras_type_0 = CreateIngredientUnitExtrasType0.from_dict(data)

                return extras_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(CreateIngredientUnitExtrasType0 | None | Unset, data)

        extras = _parse_extras(d.pop("extras", UNSET))

        fraction = d.pop("fraction", UNSET)

        abbreviation = d.pop("abbreviation", UNSET)

        def _parse_plural_abbreviation(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        plural_abbreviation = _parse_plural_abbreviation(d.pop("pluralAbbreviation", UNSET))

        use_abbreviation = d.pop("useAbbreviation", UNSET)

        _aliases = d.pop("aliases", UNSET)
        aliases: list[CreateIngredientUnitAlias] | Unset = UNSET
        if _aliases is not UNSET:
            aliases = []
            for aliases_item_data in _aliases:
                aliases_item = CreateIngredientUnitAlias.from_dict(aliases_item_data)

                aliases.append(aliases_item)

        def _parse_standard_quantity(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        standard_quantity = _parse_standard_quantity(d.pop("standardQuantity", UNSET))

        def _parse_standard_unit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        standard_unit = _parse_standard_unit(d.pop("standardUnit", UNSET))

        create_ingredient_unit = cls(
            name=name,
            id=id,
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
        )

        create_ingredient_unit.additional_properties = d
        return create_ingredient_unit

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
