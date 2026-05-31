from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.export_types import ExportTypes
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExportRecipes")


@_attrs_define
class ExportRecipes:
    """
    Attributes:
        recipes (list[str]):
        export_type (ExportTypes | Unset):
    """

    recipes: list[str]
    export_type: ExportTypes | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipes = self.recipes

        export_type: str | Unset = UNSET
        if not isinstance(self.export_type, Unset):
            export_type = self.export_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipes": recipes,
            }
        )
        if export_type is not UNSET:
            field_dict["exportType"] = export_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recipes = cast(list[str], d.pop("recipes"))

        _export_type = d.pop("exportType", UNSET)
        export_type: ExportTypes | Unset
        if isinstance(_export_type, Unset):
            export_type = UNSET
        else:
            export_type = ExportTypes(_export_type)

        export_recipes = cls(
            recipes=recipes,
            export_type=export_type,
        )

        export_recipes.additional_properties = d
        return export_recipes

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
