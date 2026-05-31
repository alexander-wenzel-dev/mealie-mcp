from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.registered_parser import RegisteredParser
from ..types import UNSET, Unset

T = TypeVar("T", bound="IngredientsRequest")


@_attrs_define
class IngredientsRequest:
    """
    Attributes:
        ingredients (list[str]):
        parser (RegisteredParser | Unset):
    """

    ingredients: list[str]
    parser: RegisteredParser | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ingredients = self.ingredients

        parser: str | Unset = UNSET
        if not isinstance(self.parser, Unset):
            parser = self.parser.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ingredients": ingredients,
            }
        )
        if parser is not UNSET:
            field_dict["parser"] = parser

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ingredients = cast(list[str], d.pop("ingredients"))

        _parser = d.pop("parser", UNSET)
        parser: RegisteredParser | Unset
        if isinstance(_parser, Unset):
            parser = UNSET
        else:
            parser = RegisteredParser(_parser)

        ingredients_request = cls(
            ingredients=ingredients,
            parser=parser,
        )

        ingredients_request.additional_properties = d
        return ingredients_request

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
