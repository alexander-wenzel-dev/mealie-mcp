from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ingredient_food_create import IngredientFoodCreate
    from ..models.ingredient_food_out import IngredientFoodOut
    from ..models.ingredient_unit_create import IngredientUnitCreate
    from ..models.ingredient_unit_out import IngredientUnitOut
    from ..models.recipe_draft import RecipeDraft
    from ..models.shopping_list_item_recipe_ref_create import ShoppingListItemRecipeRefCreate
    from ..models.shopping_list_item_recipe_ref_update import ShoppingListItemRecipeRefUpdate
    from ..models.shopping_list_item_update_extras_type_0 import ShoppingListItemUpdateExtrasType0


T = TypeVar("T", bound="ShoppingListItemUpdate")


@_attrs_define
class ShoppingListItemUpdate:
    """
    Attributes:
        shopping_list_id (str):
        quantity (float | Unset):  Default: 1.0.
        unit (IngredientUnitCreate | IngredientUnitOut | None | Unset):
        food (IngredientFoodCreate | IngredientFoodOut | None | Unset):
        referenced_recipe (None | RecipeDraft | Unset):
        note (None | str | Unset):  Default: ''.
        display (str | Unset):  Default: ''.
        checked (bool | Unset):  Default: False.
        position (int | Unset):  Default: 0.
        food_id (None | str | Unset):
        label_id (None | str | Unset):
        unit_id (None | str | Unset):
        extras (None | ShoppingListItemUpdateExtrasType0 | Unset):
        recipe_references (list[ShoppingListItemRecipeRefCreate | ShoppingListItemRecipeRefUpdate] | Unset):
    """

    shopping_list_id: str
    quantity: float | Unset = 1.0
    unit: IngredientUnitCreate | IngredientUnitOut | Unset | None = UNSET
    food: IngredientFoodCreate | IngredientFoodOut | Unset | None = UNSET
    referenced_recipe: RecipeDraft | Unset | None = UNSET
    note: str | Unset | None = ""
    display: str | Unset = ""
    checked: bool | Unset = False
    position: int | Unset = 0
    food_id: str | Unset | None = UNSET
    label_id: str | Unset | None = UNSET
    unit_id: str | Unset | None = UNSET
    extras: ShoppingListItemUpdateExtrasType0 | Unset | None = UNSET
    recipe_references: (
        list[ShoppingListItemRecipeRefCreate | ShoppingListItemRecipeRefUpdate] | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ingredient_food_create import IngredientFoodCreate  # noqa: PLC0415
        from ..models.ingredient_food_out import IngredientFoodOut  # noqa: PLC0415
        from ..models.ingredient_unit_create import IngredientUnitCreate  # noqa: PLC0415
        from ..models.ingredient_unit_out import IngredientUnitOut  # noqa: PLC0415
        from ..models.recipe_draft import RecipeDraft  # noqa: PLC0415
        from ..models.shopping_list_item_recipe_ref_create import ShoppingListItemRecipeRefCreate  # noqa: PLC0415
        from ..models.shopping_list_item_update_extras_type_0 import (
            ShoppingListItemUpdateExtrasType0,
        )

        shopping_list_id = self.shopping_list_id

        quantity = self.quantity

        unit: dict[str, Any] | Unset | None
        if isinstance(self.unit, Unset):
            unit = UNSET
        elif isinstance(self.unit, IngredientUnitOut) or isinstance(
            self.unit, IngredientUnitCreate
        ):
            unit = self.unit.to_dict()
        else:
            unit = self.unit

        food: dict[str, Any] | Unset | None
        if isinstance(self.food, Unset):
            food = UNSET
        elif isinstance(self.food, IngredientFoodOut) or isinstance(
            self.food, IngredientFoodCreate
        ):
            food = self.food.to_dict()
        else:
            food = self.food

        referenced_recipe: dict[str, Any] | Unset | None
        if isinstance(self.referenced_recipe, Unset):
            referenced_recipe = UNSET
        elif isinstance(self.referenced_recipe, RecipeDraft):
            referenced_recipe = self.referenced_recipe.to_dict()
        else:
            referenced_recipe = self.referenced_recipe

        note: str | Unset | None
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        display = self.display

        checked = self.checked

        position = self.position

        food_id: str | Unset | None
        if isinstance(self.food_id, Unset):
            food_id = UNSET
        else:
            food_id = self.food_id

        label_id: str | Unset | None
        if isinstance(self.label_id, Unset):
            label_id = UNSET
        else:
            label_id = self.label_id

        unit_id: str | Unset | None
        if isinstance(self.unit_id, Unset):
            unit_id = UNSET
        else:
            unit_id = self.unit_id

        extras: dict[str, Any] | Unset | None
        if isinstance(self.extras, Unset):
            extras = UNSET
        elif isinstance(self.extras, ShoppingListItemUpdateExtrasType0):
            extras = self.extras.to_dict()
        else:
            extras = self.extras

        recipe_references: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.recipe_references, Unset):
            recipe_references = []
            for recipe_references_item_data in self.recipe_references:
                recipe_references_item: dict[str, Any]
                if isinstance(recipe_references_item_data, ShoppingListItemRecipeRefCreate):
                    recipe_references_item = recipe_references_item_data.to_dict()
                else:
                    recipe_references_item = recipe_references_item_data.to_dict()

                recipe_references.append(recipe_references_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "shoppingListId": shopping_list_id,
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
        if recipe_references is not UNSET:
            field_dict["recipeReferences"] = recipe_references

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_food_create import IngredientFoodCreate  # noqa: PLC0415
        from ..models.ingredient_food_out import IngredientFoodOut  # noqa: PLC0415
        from ..models.ingredient_unit_create import IngredientUnitCreate  # noqa: PLC0415
        from ..models.ingredient_unit_out import IngredientUnitOut  # noqa: PLC0415
        from ..models.recipe_draft import RecipeDraft  # noqa: PLC0415
        from ..models.shopping_list_item_recipe_ref_create import ShoppingListItemRecipeRefCreate  # noqa: PLC0415
        from ..models.shopping_list_item_recipe_ref_update import ShoppingListItemRecipeRefUpdate  # noqa: PLC0415
        from ..models.shopping_list_item_update_extras_type_0 import (
            ShoppingListItemUpdateExtrasType0,
        )

        d = dict(src_dict)
        shopping_list_id = d.pop("shoppingListId")

        quantity = d.pop("quantity", UNSET)

        def _parse_unit(data: object) -> IngredientUnitCreate | IngredientUnitOut | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                unit_type_0 = IngredientUnitOut.from_dict(data)

                return unit_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                unit_type_1 = IngredientUnitCreate.from_dict(data)

                return unit_type_1
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(IngredientUnitCreate | IngredientUnitOut | None | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        def _parse_food(data: object) -> IngredientFoodCreate | IngredientFoodOut | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                food_type_0 = IngredientFoodOut.from_dict(data)

                return food_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                food_type_1 = IngredientFoodCreate.from_dict(data)

                return food_type_1
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(IngredientFoodCreate | IngredientFoodOut | None | Unset, data)

        food = _parse_food(d.pop("food", UNSET))

        def _parse_referenced_recipe(data: object) -> RecipeDraft | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                referenced_recipe_type_0 = RecipeDraft.from_dict(data)

                return referenced_recipe_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | RecipeDraft | Unset, data)

        referenced_recipe = _parse_referenced_recipe(d.pop("referencedRecipe", UNSET))

        def _parse_note(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        note = _parse_note(d.pop("note", UNSET))

        display = d.pop("display", UNSET)

        checked = d.pop("checked", UNSET)

        position = d.pop("position", UNSET)

        def _parse_food_id(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        food_id = _parse_food_id(d.pop("foodId", UNSET))

        def _parse_label_id(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        label_id = _parse_label_id(d.pop("labelId", UNSET))

        def _parse_unit_id(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unit_id = _parse_unit_id(d.pop("unitId", UNSET))

        def _parse_extras(data: object) -> ShoppingListItemUpdateExtrasType0 | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extras_type_0 = ShoppingListItemUpdateExtrasType0.from_dict(data)

                return extras_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | ShoppingListItemUpdateExtrasType0 | Unset, data)

        extras = _parse_extras(d.pop("extras", UNSET))

        _recipe_references = d.pop("recipeReferences", UNSET)
        recipe_references: (
            list[ShoppingListItemRecipeRefCreate | ShoppingListItemRecipeRefUpdate] | Unset
        ) = UNSET
        if _recipe_references is not UNSET:
            recipe_references = []
            for recipe_references_item_data in _recipe_references:

                def _parse_recipe_references_item(
                    data: object,
                ) -> ShoppingListItemRecipeRefCreate | ShoppingListItemRecipeRefUpdate:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        recipe_references_item_type_0 = ShoppingListItemRecipeRefCreate.from_dict(
                            data
                        )

                        return recipe_references_item_type_0
                    except TypeError, ValueError, AttributeError, KeyError:
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    recipe_references_item_type_1 = ShoppingListItemRecipeRefUpdate.from_dict(data)

                    return recipe_references_item_type_1

                recipe_references_item = _parse_recipe_references_item(recipe_references_item_data)

                recipe_references.append(recipe_references_item)

        shopping_list_item_update = cls(
            shopping_list_id=shopping_list_id,
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
            recipe_references=recipe_references,
        )

        shopping_list_item_update.additional_properties = d
        return shopping_list_item_update

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
