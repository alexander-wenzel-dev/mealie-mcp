from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReadHouseholdPreferences")


@_attrs_define
class ReadHouseholdPreferences:
    """
    Attributes:
        id (str):
        private_household (bool | Unset):  Default: True.
        show_announcements (bool | Unset):  Default: True.
        lock_recipe_edits_from_other_households (bool | Unset):  Default: True.
        first_day_of_week (int | Unset):  Default: 0.
        recipe_public (bool | Unset):  Default: True.
        recipe_show_nutrition (bool | Unset):  Default: False.
        recipe_show_assets (bool | Unset):  Default: False.
        recipe_landscape_view (bool | Unset):  Default: False.
        recipe_disable_comments (bool | Unset):  Default: False.
    """

    id: str
    private_household: bool | Unset = True
    show_announcements: bool | Unset = True
    lock_recipe_edits_from_other_households: bool | Unset = True
    first_day_of_week: int | Unset = 0
    recipe_public: bool | Unset = True
    recipe_show_nutrition: bool | Unset = False
    recipe_show_assets: bool | Unset = False
    recipe_landscape_view: bool | Unset = False
    recipe_disable_comments: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        private_household = self.private_household

        show_announcements = self.show_announcements

        lock_recipe_edits_from_other_households = self.lock_recipe_edits_from_other_households

        first_day_of_week = self.first_day_of_week

        recipe_public = self.recipe_public

        recipe_show_nutrition = self.recipe_show_nutrition

        recipe_show_assets = self.recipe_show_assets

        recipe_landscape_view = self.recipe_landscape_view

        recipe_disable_comments = self.recipe_disable_comments

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if private_household is not UNSET:
            field_dict["privateHousehold"] = private_household
        if show_announcements is not UNSET:
            field_dict["showAnnouncements"] = show_announcements
        if lock_recipe_edits_from_other_households is not UNSET:
            field_dict["lockRecipeEditsFromOtherHouseholds"] = (
                lock_recipe_edits_from_other_households
            )
        if first_day_of_week is not UNSET:
            field_dict["firstDayOfWeek"] = first_day_of_week
        if recipe_public is not UNSET:
            field_dict["recipePublic"] = recipe_public
        if recipe_show_nutrition is not UNSET:
            field_dict["recipeShowNutrition"] = recipe_show_nutrition
        if recipe_show_assets is not UNSET:
            field_dict["recipeShowAssets"] = recipe_show_assets
        if recipe_landscape_view is not UNSET:
            field_dict["recipeLandscapeView"] = recipe_landscape_view
        if recipe_disable_comments is not UNSET:
            field_dict["recipeDisableComments"] = recipe_disable_comments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        private_household = d.pop("privateHousehold", UNSET)

        show_announcements = d.pop("showAnnouncements", UNSET)

        lock_recipe_edits_from_other_households = d.pop("lockRecipeEditsFromOtherHouseholds", UNSET)

        first_day_of_week = d.pop("firstDayOfWeek", UNSET)

        recipe_public = d.pop("recipePublic", UNSET)

        recipe_show_nutrition = d.pop("recipeShowNutrition", UNSET)

        recipe_show_assets = d.pop("recipeShowAssets", UNSET)

        recipe_landscape_view = d.pop("recipeLandscapeView", UNSET)

        recipe_disable_comments = d.pop("recipeDisableComments", UNSET)

        read_household_preferences = cls(
            id=id,
            private_household=private_household,
            show_announcements=show_announcements,
            lock_recipe_edits_from_other_households=lock_recipe_edits_from_other_households,
            first_day_of_week=first_day_of_week,
            recipe_public=recipe_public,
            recipe_show_nutrition=recipe_show_nutrition,
            recipe_show_assets=recipe_show_assets,
            recipe_landscape_view=recipe_landscape_view,
            recipe_disable_comments=recipe_disable_comments,
        )

        read_household_preferences.additional_properties = d
        return read_household_preferences

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
