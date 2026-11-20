from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ingredient_food_create import IngredientFoodCreate
    from ..models.ingredient_food_out import IngredientFoodOut
    from ..models.ingredient_unit_create import IngredientUnitCreate
    from ..models.ingredient_unit_out import IngredientUnitOut
    from ..models.recipe_draft import RecipeDraft
    from ..models.recipe_ingredient_substitution import RecipeIngredientSubstitution


T = TypeVar("T", bound="RecipeIngredient")


@_attrs_define
class RecipeIngredient:
    """
    Attributes:
        quantity (float | None | Unset):  Default: 0.0.
        unit (IngredientUnitCreate | IngredientUnitOut | None | Unset):
        food (IngredientFoodCreate | IngredientFoodOut | None | Unset):
        referenced_recipe (None | RecipeDraft | Unset):
        note (None | str | Unset):  Default: ''.
        display (str | Unset):  Default: ''.
        title (None | str | Unset):
        original_text (None | str | Unset):
        substitutions (list[RecipeIngredientSubstitution] | Unset):
        reference_id (UUID | Unset):
    """

    quantity: float | Unset | None = 0.0
    unit: IngredientUnitCreate | IngredientUnitOut | Unset | None = UNSET
    food: IngredientFoodCreate | IngredientFoodOut | Unset | None = UNSET
    referenced_recipe: RecipeDraft | Unset | None = UNSET
    note: str | Unset | None = ""
    display: str | Unset = ""
    title: str | Unset | None = UNSET
    original_text: str | Unset | None = UNSET
    substitutions: list[RecipeIngredientSubstitution] | Unset = UNSET
    reference_id: UUID | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ingredient_food_create import IngredientFoodCreate  # noqa: PLC0415
        from ..models.ingredient_food_out import IngredientFoodOut  # noqa: PLC0415
        from ..models.ingredient_unit_create import IngredientUnitCreate  # noqa: PLC0415
        from ..models.ingredient_unit_out import IngredientUnitOut  # noqa: PLC0415
        from ..models.recipe_draft import RecipeDraft  # noqa: PLC0415

        quantity: float | Unset | None
        if isinstance(self.quantity, Unset):
            quantity = UNSET
        else:
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

        title: str | Unset | None
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        original_text: str | Unset | None
        if isinstance(self.original_text, Unset):
            original_text = UNSET
        else:
            original_text = self.original_text

        substitutions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.substitutions, Unset):
            substitutions = []
            for substitutions_item_data in self.substitutions:
                substitutions_item = substitutions_item_data.to_dict()
                substitutions.append(substitutions_item)

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
        if substitutions is not UNSET:
            field_dict["substitutions"] = substitutions
        if reference_id is not UNSET:
            field_dict["referenceId"] = reference_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_food_create import IngredientFoodCreate  # noqa: PLC0415
        from ..models.ingredient_food_out import IngredientFoodOut  # noqa: PLC0415
        from ..models.ingredient_unit_create import IngredientUnitCreate  # noqa: PLC0415
        from ..models.ingredient_unit_out import IngredientUnitOut  # noqa: PLC0415
        from ..models.recipe_draft import RecipeDraft  # noqa: PLC0415
        from ..models.recipe_ingredient_substitution import RecipeIngredientSubstitution  # noqa: PLC0415

        d = dict(src_dict)

        def _parse_quantity(data: object) -> float | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        quantity = _parse_quantity(d.pop("quantity", UNSET))

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

        def _parse_title(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_original_text(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        original_text = _parse_original_text(d.pop("originalText", UNSET))

        _substitutions = d.pop("substitutions", UNSET)
        substitutions: list[RecipeIngredientSubstitution] | Unset = UNSET
        if _substitutions is not UNSET:
            substitutions = []
            for substitutions_item_data in _substitutions:
                substitutions_item = RecipeIngredientSubstitution.from_dict(substitutions_item_data)

                substitutions.append(substitutions_item)

        _reference_id = d.pop("referenceId", UNSET)
        reference_id: UUID | Unset
        if isinstance(_reference_id, Unset):
            reference_id = UNSET
        else:
            reference_id = UUID(_reference_id)

        recipe_ingredient = cls(
            quantity=quantity,
            unit=unit,
            food=food,
            referenced_recipe=referenced_recipe,
            note=note,
            display=display,
            title=title,
            original_text=original_text,
            substitutions=substitutions,
            reference_id=reference_id,
        )

        recipe_ingredient.additional_properties = d
        return recipe_ingredient

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
