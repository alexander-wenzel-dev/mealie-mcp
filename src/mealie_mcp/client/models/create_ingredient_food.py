from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_ingredient_food_extras_type_0 import CreateIngredientFoodExtrasType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_ingredient_food_alias import CreateIngredientFoodAlias


T = TypeVar("T", bound="CreateIngredientFood")


@_attrs_define
class CreateIngredientFood:
    """
    Attributes:
        name (str):
        id (None | str | Unset):
        plural_name (None | str | Unset):
        description (str | Unset):  Default: ''.
        extras (CreateIngredientFoodExtrasType0 | None | Unset):  Default: CreateIngredientFoodExtrasType0().
        label_id (None | str | Unset):
        aliases (list[CreateIngredientFoodAlias] | Unset):
        households_with_ingredient_food (list[str] | Unset):
    """

    name: str
    id: None | str | Unset = UNSET
    plural_name: None | str | Unset = UNSET
    description: str | Unset = ""
    extras: CreateIngredientFoodExtrasType0 | None | Unset = CreateIngredientFoodExtrasType0()
    label_id: None | str | Unset = UNSET
    aliases: list[CreateIngredientFoodAlias] | Unset = UNSET
    households_with_ingredient_food: list[str] | Unset = UNSET
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
        elif isinstance(self.extras, CreateIngredientFoodExtrasType0):
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
        if label_id is not UNSET:
            field_dict["labelId"] = label_id
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if households_with_ingredient_food is not UNSET:
            field_dict["householdsWithIngredientFood"] = households_with_ingredient_food

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_ingredient_food_alias import CreateIngredientFoodAlias

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

        def _parse_extras(data: object) -> CreateIngredientFoodExtrasType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extras_type_0 = CreateIngredientFoodExtrasType0.from_dict(data)

                return extras_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(CreateIngredientFoodExtrasType0 | None | Unset, data)

        extras = _parse_extras(d.pop("extras", UNSET))

        def _parse_label_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        label_id = _parse_label_id(d.pop("labelId", UNSET))

        _aliases = d.pop("aliases", UNSET)
        aliases: list[CreateIngredientFoodAlias] | Unset = UNSET
        if _aliases is not UNSET:
            aliases = []
            for aliases_item_data in _aliases:
                aliases_item = CreateIngredientFoodAlias.from_dict(aliases_item_data)

                aliases.append(aliases_item)

        households_with_ingredient_food = cast(
            list[str], d.pop("householdsWithIngredientFood", UNSET)
        )

        create_ingredient_food = cls(
            name=name,
            id=id,
            plural_name=plural_name,
            description=description,
            extras=extras,
            label_id=label_id,
            aliases=aliases,
            households_with_ingredient_food=households_with_ingredient_food,
        )

        create_ingredient_food.additional_properties = d
        return create_ingredient_food

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
