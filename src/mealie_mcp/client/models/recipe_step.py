from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ingredient_references import IngredientReferences


T = TypeVar("T", bound="RecipeStep")


@_attrs_define
class RecipeStep:
    """
    Attributes:
        text (str):
        id (None | Unset | UUID):
        title (None | str | Unset):  Default: ''.
        summary (None | str | Unset):  Default: ''.
        ingredient_references (list[IngredientReferences] | Unset):
    """

    text: str
    id: None | Unset | UUID = UNSET
    title: None | str | Unset = ""
    summary: None | str | Unset = ""
    ingredient_references: list[IngredientReferences] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        elif isinstance(self.id, UUID):
            id = str(self.id)
        else:
            id = self.id

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        summary: None | str | Unset
        if isinstance(self.summary, Unset):
            summary = UNSET
        else:
            summary = self.summary

        ingredient_references: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.ingredient_references, Unset):
            ingredient_references = []
            for ingredient_references_item_data in self.ingredient_references:
                ingredient_references_item = ingredient_references_item_data.to_dict()
                ingredient_references.append(ingredient_references_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "text": text,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if title is not UNSET:
            field_dict["title"] = title
        if summary is not UNSET:
            field_dict["summary"] = summary
        if ingredient_references is not UNSET:
            field_dict["ingredientReferences"] = ingredient_references

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_references import IngredientReferences

        d = dict(src_dict)
        text = d.pop("text")

        def _parse_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                id_type_0 = UUID(data)

                return id_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | Unset | UUID, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_summary(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        summary = _parse_summary(d.pop("summary", UNSET))

        _ingredient_references = d.pop("ingredientReferences", UNSET)
        ingredient_references: list[IngredientReferences] | Unset = UNSET
        if _ingredient_references is not UNSET:
            ingredient_references = []
            for ingredient_references_item_data in _ingredient_references:
                ingredient_references_item = IngredientReferences.from_dict(
                    ingredient_references_item_data
                )

                ingredient_references.append(ingredient_references_item)

        recipe_step = cls(
            text=text,
            id=id,
            title=title,
            summary=summary,
            ingredient_references=ingredient_references,
        )

        recipe_step.additional_properties = d
        return recipe_step

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
