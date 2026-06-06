from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.shopping_list_item_update_extras_type_0 import ShoppingListItemUpdateExtrasType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_ingredient_food import CreateIngredientFood
    from ..models.create_ingredient_unit import CreateIngredientUnit
    from ..models.ingredient_food import IngredientFood
    from ..models.ingredient_unit import IngredientUnit
    from ..models.recipe import Recipe
    from ..models.shopping_list_item_recipe_ref_create import ShoppingListItemRecipeRefCreate
    from ..models.shopping_list_item_recipe_ref_update import ShoppingListItemRecipeRefUpdate


T = TypeVar("T", bound="ShoppingListItemUpdate")


@_attrs_define
class ShoppingListItemUpdate:
    """
    Attributes:
        shopping_list_id (str):
        quantity (float | Unset):  Default: 1.0.
        unit (CreateIngredientUnit | IngredientUnit | None | Unset):
        food (CreateIngredientFood | IngredientFood | None | Unset):
        referenced_recipe (None | Recipe | Unset):
        note (None | str | Unset):  Default: ''.
        display (str | Unset):  Default: ''.
        checked (bool | Unset):  Default: False.
        position (int | Unset):  Default: 0.
        food_id (None | str | Unset):
        label_id (None | str | Unset):
        unit_id (None | str | Unset):
        extras (None | ShoppingListItemUpdateExtrasType0 | Unset):  Default: ShoppingListItemUpdateExtrasType0().
        recipe_references (list[ShoppingListItemRecipeRefCreate | ShoppingListItemRecipeRefUpdate] | Unset):
    """

    shopping_list_id: str
    quantity: float | Unset = 1.0
    unit: CreateIngredientUnit | IngredientUnit | None | Unset = UNSET
    food: CreateIngredientFood | IngredientFood | None | Unset = UNSET
    referenced_recipe: None | Recipe | Unset = UNSET
    note: None | str | Unset = ""
    display: str | Unset = ""
    checked: bool | Unset = False
    position: int | Unset = 0
    food_id: None | str | Unset = UNSET
    label_id: None | str | Unset = UNSET
    unit_id: None | str | Unset = UNSET
    extras: None | ShoppingListItemUpdateExtrasType0 | Unset = ShoppingListItemUpdateExtrasType0()
    recipe_references: (
        list[ShoppingListItemRecipeRefCreate | ShoppingListItemRecipeRefUpdate] | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.create_ingredient_food import CreateIngredientFood
        from ..models.create_ingredient_unit import CreateIngredientUnit
        from ..models.ingredient_food import IngredientFood
        from ..models.ingredient_unit import IngredientUnit
        from ..models.recipe import Recipe
        from ..models.shopping_list_item_recipe_ref_create import ShoppingListItemRecipeRefCreate

        shopping_list_id = self.shopping_list_id

        quantity = self.quantity

        unit: dict[str, Any] | None | Unset
        if isinstance(self.unit, Unset):
            unit = UNSET
        elif isinstance(self.unit, IngredientUnit) or isinstance(self.unit, CreateIngredientUnit):
            unit = self.unit.to_dict()
        else:
            unit = self.unit

        food: dict[str, Any] | None | Unset
        if isinstance(self.food, Unset):
            food = UNSET
        elif isinstance(self.food, IngredientFood) or isinstance(self.food, CreateIngredientFood):
            food = self.food.to_dict()
        else:
            food = self.food

        referenced_recipe: dict[str, Any] | None | Unset
        if isinstance(self.referenced_recipe, Unset):
            referenced_recipe = UNSET
        elif isinstance(self.referenced_recipe, Recipe):
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
        from ..models.create_ingredient_food import CreateIngredientFood
        from ..models.create_ingredient_unit import CreateIngredientUnit
        from ..models.ingredient_food import IngredientFood
        from ..models.ingredient_unit import IngredientUnit
        from ..models.recipe import Recipe
        from ..models.shopping_list_item_recipe_ref_create import ShoppingListItemRecipeRefCreate
        from ..models.shopping_list_item_recipe_ref_update import ShoppingListItemRecipeRefUpdate

        d = dict(src_dict)
        shopping_list_id = d.pop("shoppingListId")

        quantity = d.pop("quantity", UNSET)

        def _parse_unit(data: object) -> CreateIngredientUnit | IngredientUnit | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                unit_type_0 = IngredientUnit.from_dict(data)

                return unit_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                unit_type_1 = CreateIngredientUnit.from_dict(data)

                return unit_type_1
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(CreateIngredientUnit | IngredientUnit | None | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        def _parse_food(data: object) -> CreateIngredientFood | IngredientFood | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                food_type_0 = IngredientFood.from_dict(data)

                return food_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                food_type_1 = CreateIngredientFood.from_dict(data)

                return food_type_1
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(CreateIngredientFood | IngredientFood | None | Unset, data)

        food = _parse_food(d.pop("food", UNSET))

        def _parse_referenced_recipe(data: object) -> None | Recipe | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                referenced_recipe_type_0 = Recipe.from_dict(data)

                return referenced_recipe_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | Recipe | Unset, data)

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

        def _parse_extras(data: object) -> None | ShoppingListItemUpdateExtrasType0 | Unset:
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
