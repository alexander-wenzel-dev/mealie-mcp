from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ingredient_food_out_output import IngredientFoodOutOutput
    from ..models.ingredient_unit_out_output import IngredientUnitOutOutput
    from ..models.multi_purpose_label_summary_output import MultiPurposeLabelSummaryOutput
    from ..models.recipe_draft_output import RecipeDraftOutput
    from ..models.shopping_list_item_out_output_extras_type_0 import (
        ShoppingListItemOutOutputExtrasType0,
    )
    from ..models.shopping_list_item_recipe_ref_out_output import ShoppingListItemRecipeRefOutOutput


T = TypeVar("T", bound="ShoppingListItemOutOutput")


@_attrs_define
class ShoppingListItemOutOutput:
    """
    Attributes:
        quantity (float):  Default: 1.0.
        unit (IngredientUnitOutOutput | None):
        food (IngredientFoodOutOutput | None):
        referenced_recipe (None | RecipeDraftOutput):
        note (None | str):  Default: ''.
        display (str):  Default: ''.
        shopping_list_id (str):
        checked (bool):  Default: False.
        position (int):  Default: 0.
        food_id (None | str):
        label_id (None | str):
        unit_id (None | str):
        extras (None | ShoppingListItemOutOutputExtrasType0):
        id (str):
        group_id (str):
        household_id (str):
        label (MultiPurposeLabelSummaryOutput | None):
        recipe_references (list[ShoppingListItemRecipeRefOutOutput]):
        created_at (datetime.datetime | None):
        updated_at (datetime.datetime | None):
    """

    unit: IngredientUnitOutOutput | None
    food: IngredientFoodOutOutput | None
    referenced_recipe: RecipeDraftOutput | None
    shopping_list_id: str
    food_id: str | None
    label_id: str | None
    unit_id: str | None
    extras: ShoppingListItemOutOutputExtrasType0 | None
    id: str
    group_id: str
    household_id: str
    label: MultiPurposeLabelSummaryOutput | None
    recipe_references: list[ShoppingListItemRecipeRefOutOutput]
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    quantity: float = 1.0
    note: str | None = ""
    display: str = ""
    checked: bool = False
    position: int = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ingredient_food_out_output import IngredientFoodOutOutput  # noqa: PLC0415
        from ..models.ingredient_unit_out_output import IngredientUnitOutOutput  # noqa: PLC0415
        from ..models.multi_purpose_label_summary_output import MultiPurposeLabelSummaryOutput  # noqa: PLC0415
        from ..models.recipe_draft_output import RecipeDraftOutput  # noqa: PLC0415
        from ..models.shopping_list_item_out_output_extras_type_0 import (
            ShoppingListItemOutOutputExtrasType0,
        )

        quantity = self.quantity

        unit: dict[str, Any] | None
        if isinstance(self.unit, IngredientUnitOutOutput):
            unit = self.unit.to_dict()
        else:
            unit = self.unit

        food: dict[str, Any] | None
        if isinstance(self.food, IngredientFoodOutOutput):
            food = self.food.to_dict()
        else:
            food = self.food

        referenced_recipe: dict[str, Any] | None
        if isinstance(self.referenced_recipe, RecipeDraftOutput):
            referenced_recipe = self.referenced_recipe.to_dict()
        else:
            referenced_recipe = self.referenced_recipe

        note: str | None
        note = self.note

        display = self.display

        shopping_list_id = self.shopping_list_id

        checked = self.checked

        position = self.position

        food_id: str | None
        food_id = self.food_id

        label_id: str | None
        label_id = self.label_id

        unit_id: str | None
        unit_id = self.unit_id

        extras: dict[str, Any] | None
        if isinstance(self.extras, ShoppingListItemOutOutputExtrasType0):
            extras = self.extras.to_dict()
        else:
            extras = self.extras

        id = self.id

        group_id = self.group_id

        household_id = self.household_id

        label: dict[str, Any] | None
        if isinstance(self.label, MultiPurposeLabelSummaryOutput):
            label = self.label.to_dict()
        else:
            label = self.label

        recipe_references = []
        for recipe_references_item_data in self.recipe_references:
            recipe_references_item = recipe_references_item_data.to_dict()
            recipe_references.append(recipe_references_item)

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
                "quantity": quantity,
                "unit": unit,
                "food": food,
                "referencedRecipe": referenced_recipe,
                "note": note,
                "display": display,
                "shoppingListId": shopping_list_id,
                "checked": checked,
                "position": position,
                "foodId": food_id,
                "labelId": label_id,
                "unitId": unit_id,
                "extras": extras,
                "id": id,
                "groupId": group_id,
                "householdId": household_id,
                "label": label,
                "recipeReferences": recipe_references,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_food_out_output import IngredientFoodOutOutput  # noqa: PLC0415
        from ..models.ingredient_unit_out_output import IngredientUnitOutOutput  # noqa: PLC0415
        from ..models.multi_purpose_label_summary_output import MultiPurposeLabelSummaryOutput  # noqa: PLC0415
        from ..models.recipe_draft_output import RecipeDraftOutput  # noqa: PLC0415
        from ..models.shopping_list_item_out_output_extras_type_0 import (
            ShoppingListItemOutOutputExtrasType0,
        )
        from ..models.shopping_list_item_recipe_ref_out_output import (
            ShoppingListItemRecipeRefOutOutput,
        )

        d = dict(src_dict)
        quantity = d.pop("quantity")

        def _parse_unit(data: object) -> IngredientUnitOutOutput | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                unit_type_0 = IngredientUnitOutOutput.from_dict(data)

                return unit_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(IngredientUnitOutOutput | None, data)

        unit = _parse_unit(d.pop("unit"))

        def _parse_food(data: object) -> IngredientFoodOutOutput | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                food_type_0 = IngredientFoodOutOutput.from_dict(data)

                return food_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(IngredientFoodOutOutput | None, data)

        food = _parse_food(d.pop("food"))

        def _parse_referenced_recipe(data: object) -> RecipeDraftOutput | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                referenced_recipe_type_0 = RecipeDraftOutput.from_dict(data)

                return referenced_recipe_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | RecipeDraftOutput, data)

        referenced_recipe = _parse_referenced_recipe(d.pop("referencedRecipe"))

        def _parse_note(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        note = _parse_note(d.pop("note"))

        display = d.pop("display")

        shopping_list_id = d.pop("shoppingListId")

        checked = d.pop("checked")

        position = d.pop("position")

        def _parse_food_id(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        food_id = _parse_food_id(d.pop("foodId"))

        def _parse_label_id(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        label_id = _parse_label_id(d.pop("labelId"))

        def _parse_unit_id(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        unit_id = _parse_unit_id(d.pop("unitId"))

        def _parse_extras(data: object) -> ShoppingListItemOutOutputExtrasType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extras_type_0 = ShoppingListItemOutOutputExtrasType0.from_dict(data)

                return extras_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | ShoppingListItemOutOutputExtrasType0, data)

        extras = _parse_extras(d.pop("extras"))

        id = d.pop("id")

        group_id = d.pop("groupId")

        household_id = d.pop("householdId")

        def _parse_label(data: object) -> MultiPurposeLabelSummaryOutput | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                label_type_0 = MultiPurposeLabelSummaryOutput.from_dict(data)

                return label_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(MultiPurposeLabelSummaryOutput | None, data)

        label = _parse_label(d.pop("label"))

        recipe_references = []
        _recipe_references = d.pop("recipeReferences")
        for recipe_references_item_data in _recipe_references:
            recipe_references_item = ShoppingListItemRecipeRefOutOutput.from_dict(
                recipe_references_item_data
            )

            recipe_references.append(recipe_references_item)

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

        shopping_list_item_out_output = cls(
            quantity=quantity,
            unit=unit,
            food=food,
            referenced_recipe=referenced_recipe,
            note=note,
            display=display,
            shopping_list_id=shopping_list_id,
            checked=checked,
            position=position,
            food_id=food_id,
            label_id=label_id,
            unit_id=unit_id,
            extras=extras,
            id=id,
            group_id=group_id,
            household_id=household_id,
            label=label,
            recipe_references=recipe_references,
            created_at=created_at,
            updated_at=updated_at,
        )

        shopping_list_item_out_output.additional_properties = d
        return shopping_list_item_out_output

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
