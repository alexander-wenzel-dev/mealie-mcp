from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RecipeSettings")


@_attrs_define
class RecipeSettings:
    """
    Attributes:
        public (bool | Unset):  Default: False.
        show_nutrition (bool | Unset):  Default: False.
        show_assets (bool | Unset):  Default: False.
        landscape_view (bool | Unset):  Default: False.
        disable_comments (bool | Unset):  Default: True.
        locked (bool | Unset):  Default: False.
    """

    public: bool | Unset = False
    show_nutrition: bool | Unset = False
    show_assets: bool | Unset = False
    landscape_view: bool | Unset = False
    disable_comments: bool | Unset = True
    locked: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        public = self.public

        show_nutrition = self.show_nutrition

        show_assets = self.show_assets

        landscape_view = self.landscape_view

        disable_comments = self.disable_comments

        locked = self.locked

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if public is not UNSET:
            field_dict["public"] = public
        if show_nutrition is not UNSET:
            field_dict["showNutrition"] = show_nutrition
        if show_assets is not UNSET:
            field_dict["showAssets"] = show_assets
        if landscape_view is not UNSET:
            field_dict["landscapeView"] = landscape_view
        if disable_comments is not UNSET:
            field_dict["disableComments"] = disable_comments
        if locked is not UNSET:
            field_dict["locked"] = locked

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        public = d.pop("public", UNSET)

        show_nutrition = d.pop("showNutrition", UNSET)

        show_assets = d.pop("showAssets", UNSET)

        landscape_view = d.pop("landscapeView", UNSET)

        disable_comments = d.pop("disableComments", UNSET)

        locked = d.pop("locked", UNSET)

        recipe_settings = cls(
            public=public,
            show_nutrition=show_nutrition,
            show_assets=show_assets,
            landscape_view=landscape_view,
            disable_comments=disable_comments,
            locked=locked,
        )

        recipe_settings.additional_properties = d
        return recipe_settings

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
