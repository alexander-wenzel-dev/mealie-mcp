from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.shopping_list_item_out_output_extras_type_0 import (
    ShoppingListItemOutOutputExtrasType0,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ingredient_food_output import IngredientFoodOutput
    from ..models.ingredient_unit_output import IngredientUnitOutput
    from ..models.multi_purpose_label_summary import MultiPurposeLabelSummary
    from ..models.recipe_output import RecipeOutput
    from ..models.shopping_list_item_recipe_ref_out import ShoppingListItemRecipeRefOut


T = TypeVar("T", bound="ShoppingListItemOutOutput")


@_attrs_define
class ShoppingListItemOutOutput:
    """
    Attributes:
        shopping_list_id (str):
        id (str):
        group_id (str):
        household_id (str):
        quantity (float | Unset):  Default: 1.0.
        unit (IngredientUnitOutput | None | Unset):
        food (IngredientFoodOutput | None | Unset):
        referenced_recipe (None | RecipeOutput | Unset):
        note (None | str | Unset):  Default: ''.
        display (str | Unset):  Default: ''.
        checked (bool | Unset):  Default: False.
        position (int | Unset):  Default: 0.
        food_id (None | str | Unset):
        label_id (None | str | Unset):
        unit_id (None | str | Unset):
        extras (None | ShoppingListItemOutOutputExtrasType0 | Unset):  Default: ShoppingListItemOutOutputExtrasType0().
        label (MultiPurposeLabelSummary | None | Unset):
        recipe_references (list[ShoppingListItemRecipeRefOut] | Unset):
        created_at (datetime.datetime | None | Unset):
        updated_at (datetime.datetime | None | Unset):
    """

    shopping_list_id: str
    id: str
    group_id: str
    household_id: str
    quantity: float | Unset = 1.0
    unit: IngredientUnitOutput | None | Unset = UNSET
    food: IngredientFoodOutput | None | Unset = UNSET
    referenced_recipe: None | RecipeOutput | Unset = UNSET
    note: None | str | Unset = ""
    display: str | Unset = ""
    checked: bool | Unset = False
    position: int | Unset = 0
    food_id: None | str | Unset = UNSET
    label_id: None | str | Unset = UNSET
    unit_id: None | str | Unset = UNSET
    extras: None | ShoppingListItemOutOutputExtrasType0 | Unset = (
        ShoppingListItemOutOutputExtrasType0()
    )
    label: MultiPurposeLabelSummary | None | Unset = UNSET
    recipe_references: list[ShoppingListItemRecipeRefOut] | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ingredient_food_output import IngredientFoodOutput
        from ..models.ingredient_unit_output import IngredientUnitOutput
        from ..models.multi_purpose_label_summary import MultiPurposeLabelSummary
        from ..models.recipe_output import RecipeOutput

        shopping_list_id = self.shopping_list_id

        id = self.id

        group_id = self.group_id

        household_id = self.household_id

        quantity = self.quantity

        unit: dict[str, Any] | None | Unset
        if isinstance(self.unit, Unset):
            unit = UNSET
        elif isinstance(self.unit, IngredientUnitOutput):
            unit = self.unit.to_dict()
        else:
            unit = self.unit

        food: dict[str, Any] | None | Unset
        if isinstance(self.food, Unset):
            food = UNSET
        elif isinstance(self.food, IngredientFoodOutput):
            food = self.food.to_dict()
        else:
            food = self.food

        referenced_recipe: dict[str, Any] | None | Unset
        if isinstance(self.referenced_recipe, Unset):
            referenced_recipe = UNSET
        elif isinstance(self.referenced_recipe, RecipeOutput):
            referenced_recipe = self.referenced_recipe.to_dict()
        else:
            referenced_recipe = self.referenced_recipe

        note: None | str | Unset
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        display = self.display

        checked = self.checked

        position = self.position

        food_id: None | str | Unset
        if isinstance(self.food_id, Unset):
            food_id = UNSET
        else:
            food_id = self.food_id

        label_id: None | str | Unset
        if isinstance(self.label_id, Unset):
            label_id = UNSET
        else:
            label_id = self.label_id

        unit_id: None | str | Unset
        if isinstance(self.unit_id, Unset):
            unit_id = UNSET
        else:
            unit_id = self.unit_id

        extras: dict[str, Any] | None | Unset
        if isinstance(self.extras, Unset):
            extras = UNSET
        elif isinstance(self.extras, ShoppingListItemOutOutputExtrasType0):
            extras = self.extras.to_dict()
        else:
            extras = self.extras

        label: dict[str, Any] | None | Unset
        if isinstance(self.label, Unset):
            label = UNSET
        elif isinstance(self.label, MultiPurposeLabelSummary):
            label = self.label.to_dict()
        else:
            label = self.label

        recipe_references: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.recipe_references, Unset):
            recipe_references = []
            for recipe_references_item_data in self.recipe_references:
                recipe_references_item = recipe_references_item_data.to_dict()
                recipe_references.append(recipe_references_item)

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "shoppingListId": shopping_list_id,
                "id": id,
                "groupId": group_id,
                "householdId": household_id,
            }
        )
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if unit is not UNSET:
            field_dict["unit"] = unit
        if food is not UNSET:
            field_dict["food"] = food
        if referenced_recipe is not UNSET:
            field_dict["referencedRecipe"] = referenced_recipe
        if note is not UNSET:
            field_dict["note"] = note
        if display is not UNSET:
            field_dict["display"] = display
        if checked is not UNSET:
            field_dict["checked"] = checked
        if position is not UNSET:
            field_dict["position"] = position
        if food_id is not UNSET:
            field_dict["foodId"] = food_id
        if label_id is not UNSET:
            field_dict["labelId"] = label_id
        if unit_id is not UNSET:
            field_dict["unitId"] = unit_id
        if extras is not UNSET:
            field_dict["extras"] = extras
        if label is not UNSET:
            field_dict["label"] = label
        if recipe_references is not UNSET:
            field_dict["recipeReferences"] = recipe_references
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_food_output import IngredientFoodOutput
        from ..models.ingredient_unit_output import IngredientUnitOutput
        from ..models.multi_purpose_label_summary import MultiPurposeLabelSummary
        from ..models.recipe_output import RecipeOutput
        from ..models.shopping_list_item_recipe_ref_out import ShoppingListItemRecipeRefOut

        d = dict(src_dict)
        shopping_list_id = d.pop("shoppingListId")

        id = d.pop("id")

        group_id = d.pop("groupId")

        household_id = d.pop("householdId")

        quantity = d.pop("quantity", UNSET)

        def _parse_unit(data: object) -> IngredientUnitOutput | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                unit_type_0 = IngredientUnitOutput.from_dict(data)

                return unit_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(IngredientUnitOutput | None | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        def _parse_food(data: object) -> IngredientFoodOutput | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                food_type_0 = IngredientFoodOutput.from_dict(data)

                return food_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(IngredientFoodOutput | None | Unset, data)

        food = _parse_food(d.pop("food", UNSET))

        def _parse_referenced_recipe(data: object) -> None | RecipeOutput | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                referenced_recipe_type_0 = RecipeOutput.from_dict(data)

                return referenced_recipe_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | RecipeOutput | Unset, data)

        referenced_recipe = _parse_referenced_recipe(d.pop("referencedRecipe", UNSET))

        def _parse_note(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        note = _parse_note(d.pop("note", UNSET))

        display = d.pop("display", UNSET)

        checked = d.pop("checked", UNSET)

        position = d.pop("position", UNSET)

        def _parse_food_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        food_id = _parse_food_id(d.pop("foodId", UNSET))

        def _parse_label_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        label_id = _parse_label_id(d.pop("labelId", UNSET))

        def _parse_unit_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unit_id = _parse_unit_id(d.pop("unitId", UNSET))

        def _parse_extras(data: object) -> None | ShoppingListItemOutOutputExtrasType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extras_type_0 = ShoppingListItemOutOutputExtrasType0.from_dict(data)

                return extras_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | ShoppingListItemOutOutputExtrasType0 | Unset, data)

        extras = _parse_extras(d.pop("extras", UNSET))

        def _parse_label(data: object) -> MultiPurposeLabelSummary | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                label_type_0 = MultiPurposeLabelSummary.from_dict(data)

                return label_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(MultiPurposeLabelSummary | None | Unset, data)

        label = _parse_label(d.pop("label", UNSET))

        _recipe_references = d.pop("recipeReferences", UNSET)
        recipe_references: list[ShoppingListItemRecipeRefOut] | Unset = UNSET
        if _recipe_references is not UNSET:
            recipe_references = []
            for recipe_references_item_data in _recipe_references:
                recipe_references_item = ShoppingListItemRecipeRefOut.from_dict(
                    recipe_references_item_data
                )

                recipe_references.append(recipe_references_item)

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = datetime.datetime.fromisoformat(data)

                return created_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("createdAt", UNSET))

        def _parse_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = datetime.datetime.fromisoformat(data)

                return updated_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updatedAt", UNSET))

        shopping_list_item_out_output = cls(
            shopping_list_id=shopping_list_id,
            id=id,
            group_id=group_id,
            household_id=household_id,
            quantity=quantity,
            unit=unit,
            food=food,
            referenced_recipe=referenced_recipe,
            note=note,
            display=display,
            checked=checked,
            position=position,
            food_id=food_id,
            label_id=label_id,
            unit_id=unit_id,
            extras=extras,
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
