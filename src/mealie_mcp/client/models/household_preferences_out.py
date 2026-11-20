from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HouseholdPreferencesOut")


@_attrs_define
class HouseholdPreferencesOut:
    """
    Attributes:
        private_household (bool):  Default: True.
        show_announcements (bool):  Default: True.
        lock_recipe_edits_from_other_households (bool):  Default: True.
        first_day_of_week (int):  Default: 0.
        recipe_public (bool):  Default: True.
        recipe_show_nutrition (bool):  Default: False.
        recipe_show_assets (bool):  Default: False.
        recipe_landscape_view (bool):  Default: False.
        recipe_disable_comments (bool):  Default: False.
        id (str):
    """

    id: str
    private_household: bool = True
    show_announcements: bool = True
    lock_recipe_edits_from_other_households: bool = True
    first_day_of_week: int = 0
    recipe_public: bool = True
    recipe_show_nutrition: bool = False
    recipe_show_assets: bool = False
    recipe_landscape_view: bool = False
    recipe_disable_comments: bool = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        private_household = self.private_household

        show_announcements = self.show_announcements

        lock_recipe_edits_from_other_households = self.lock_recipe_edits_from_other_households

        first_day_of_week = self.first_day_of_week

        recipe_public = self.recipe_public

        recipe_show_nutrition = self.recipe_show_nutrition

        recipe_show_assets = self.recipe_show_assets

        recipe_landscape_view = self.recipe_landscape_view

        recipe_disable_comments = self.recipe_disable_comments

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "privateHousehold": private_household,
                "showAnnouncements": show_announcements,
                "lockRecipeEditsFromOtherHouseholds": lock_recipe_edits_from_other_households,
                "firstDayOfWeek": first_day_of_week,
                "recipePublic": recipe_public,
                "recipeShowNutrition": recipe_show_nutrition,
                "recipeShowAssets": recipe_show_assets,
                "recipeLandscapeView": recipe_landscape_view,
                "recipeDisableComments": recipe_disable_comments,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        private_household = d.pop("privateHousehold")

        show_announcements = d.pop("showAnnouncements")

        lock_recipe_edits_from_other_households = d.pop("lockRecipeEditsFromOtherHouseholds")

        first_day_of_week = d.pop("firstDayOfWeek")

        recipe_public = d.pop("recipePublic")

        recipe_show_nutrition = d.pop("recipeShowNutrition")

        recipe_show_assets = d.pop("recipeShowAssets")

        recipe_landscape_view = d.pop("recipeLandscapeView")

        recipe_disable_comments = d.pop("recipeDisableComments")

        id = d.pop("id")

        household_preferences_out = cls(
            private_household=private_household,
            show_announcements=show_announcements,
            lock_recipe_edits_from_other_households=lock_recipe_edits_from_other_households,
            first_day_of_week=first_day_of_week,
            recipe_public=recipe_public,
            recipe_show_nutrition=recipe_show_nutrition,
            recipe_show_assets=recipe_show_assets,
            recipe_landscape_view=recipe_landscape_view,
            recipe_disable_comments=recipe_disable_comments,
            id=id,
        )

        household_preferences_out.additional_properties = d
        return household_preferences_out

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
