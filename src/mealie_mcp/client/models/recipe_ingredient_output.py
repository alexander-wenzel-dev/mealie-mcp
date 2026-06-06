from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_ingredient_food import CreateIngredientFood
    from ..models.create_ingredient_unit import CreateIngredientUnit
    from ..models.ingredient_food_output import IngredientFoodOutput
    from ..models.ingredient_unit_output import IngredientUnitOutput
    from ..models.recipe_output import RecipeOutput


T = TypeVar("T", bound="RecipeIngredientOutput")


@_attrs_define
class RecipeIngredientOutput:
    """
    Attributes:
        quantity (float | None | Unset):  Default: 0.0.
        unit (CreateIngredientUnit | IngredientUnitOutput | None | Unset):
        food (CreateIngredientFood | IngredientFoodOutput | None | Unset):
        referenced_recipe (None | RecipeOutput | Unset):
        note (None | str | Unset):  Default: ''.
        display (str | Unset):  Default: ''.
        title (None | str | Unset):
        original_text (None | str | Unset):
        reference_id (UUID | Unset):
    """

    quantity: float | None | Unset = 0.0
    unit: CreateIngredientUnit | IngredientUnitOutput | None | Unset = UNSET
    food: CreateIngredientFood | IngredientFoodOutput | None | Unset = UNSET
    referenced_recipe: None | RecipeOutput | Unset = UNSET
    note: None | str | Unset = ""
    display: str | Unset = ""
    title: None | str | Unset = UNSET
    original_text: None | str | Unset = UNSET
    reference_id: UUID | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.create_ingredient_food import CreateIngredientFood
        from ..models.create_ingredient_unit import CreateIngredientUnit
        from ..models.ingredient_food_output import IngredientFoodOutput
        from ..models.ingredient_unit_output import IngredientUnitOutput
        from ..models.recipe_output import RecipeOutput

        quantity: float | None | Unset
        if isinstance(self.quantity, Unset):
            quantity = UNSET
        else:
            quantity = self.quantity

        unit: dict[str, Any] | None | Unset
        if isinstance(self.unit, Unset):
            unit = UNSET
        elif isinstance(self.unit, IngredientUnitOutput) or isinstance(
            self.unit, CreateIngredientUnit
        ):
            unit = self.unit.to_dict()
        else:
            unit = self.unit

        food: dict[str, Any] | None | Unset
        if isinstance(self.food, Unset):
            food = UNSET
        elif isinstance(self.food, IngredientFoodOutput) or isinstance(
            self.food, CreateIngredientFood
        ):
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

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        original_text: None | str | Unset
        if isinstance(self.original_text, Unset):
            original_text = UNSET
        else:
            original_text = self.original_text

        reference_id: str | Unset = UNSET
        if not isinstance(self.reference_id, Unset):
            reference_id = str(self.reference_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
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
        if title is not UNSET:
            field_dict["title"] = title
        if original_text is not UNSET:
            field_dict["originalText"] = original_text
        if reference_id is not UNSET:
            field_dict["referenceId"] = reference_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_ingredient_food import CreateIngredientFood
        from ..models.create_ingredient_unit import CreateIngredientUnit
        from ..models.ingredient_food_output import IngredientFoodOutput
        from ..models.ingredient_unit_output import IngredientUnitOutput
        from ..models.recipe_output import RecipeOutput

        d = dict(src_dict)

        def _parse_quantity(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        quantity = _parse_quantity(d.pop("quantity", UNSET))

        def _parse_unit(data: object) -> CreateIngredientUnit | IngredientUnitOutput | None | Unset:
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
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                unit_type_1 = CreateIngredientUnit.from_dict(data)

                return unit_type_1
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(CreateIngredientUnit | IngredientUnitOutput | None | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        def _parse_food(data: object) -> CreateIngredientFood | IngredientFoodOutput | None | Unset:
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
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                food_type_1 = CreateIngredientFood.from_dict(data)

                return food_type_1
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(CreateIngredientFood | IngredientFoodOutput | None | Unset, data)

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

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_original_text(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        original_text = _parse_original_text(d.pop("originalText", UNSET))

        _reference_id = d.pop("referenceId", UNSET)
        reference_id: UUID | Unset
        if isinstance(_reference_id, Unset):
            reference_id = UNSET
        else:
            reference_id = UUID(_reference_id)

        recipe_ingredient_output = cls(
            quantity=quantity,
            unit=unit,
            food=food,
            referenced_recipe=referenced_recipe,
            note=note,
            display=display,
            title=title,
            original_text=original_text,
            reference_id=reference_id,
        )

        recipe_ingredient_output.additional_properties = d
        return recipe_ingredient_output

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
