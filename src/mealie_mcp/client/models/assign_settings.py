from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.recipe_settings import RecipeSettings


T = TypeVar("T", bound="AssignSettings")


@_attrs_define
class AssignSettings:
    """
    Attributes:
        recipes (list[str]):
        settings (RecipeSettings):
    """

    recipes: list[str]
    settings: RecipeSettings
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipes = self.recipes

        settings = self.settings.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipes": recipes,
                "settings": settings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recipe_settings import RecipeSettings

        d = dict(src_dict)
        recipes = cast(list[str], d.pop("recipes"))

        settings = RecipeSettings.from_dict(d.pop("settings"))

        assign_settings = cls(
            recipes=recipes,
            settings=settings,
        )

        assign_settings.additional_properties = d
        return assign_settings

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
