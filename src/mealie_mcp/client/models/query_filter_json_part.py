from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.logical_operator import LogicalOperator
from ..models.relational_keyword import RelationalKeyword
from ..models.relational_operator import RelationalOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="QueryFilterJSONPart")


@_attrs_define
class QueryFilterJSONPart:
    """
    Attributes:
        left_parenthesis (None | str | Unset):
        right_parenthesis (None | str | Unset):
        logical_operator (LogicalOperator | None | Unset):
        attribute_name (None | str | Unset):
        relational_operator (None | RelationalKeyword | RelationalOperator | Unset):
        value (list[str] | None | str | Unset):
    """

    left_parenthesis: None | str | Unset = UNSET
    right_parenthesis: None | str | Unset = UNSET
    logical_operator: LogicalOperator | None | Unset = UNSET
    attribute_name: None | str | Unset = UNSET
    relational_operator: None | RelationalKeyword | RelationalOperator | Unset = UNSET
    value: list[str] | None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        left_parenthesis: None | str | Unset
        if isinstance(self.left_parenthesis, Unset):
            left_parenthesis = UNSET
        else:
            left_parenthesis = self.left_parenthesis

        right_parenthesis: None | str | Unset
        if isinstance(self.right_parenthesis, Unset):
            right_parenthesis = UNSET
        else:
            right_parenthesis = self.right_parenthesis

        logical_operator: None | str | Unset
        if isinstance(self.logical_operator, Unset):
            logical_operator = UNSET
        elif isinstance(self.logical_operator, LogicalOperator):
            logical_operator = self.logical_operator.value
        else:
            logical_operator = self.logical_operator

        attribute_name: None | str | Unset
        if isinstance(self.attribute_name, Unset):
            attribute_name = UNSET
        else:
            attribute_name = self.attribute_name

        relational_operator: None | str | Unset
        if isinstance(self.relational_operator, Unset):
            relational_operator = UNSET
        elif isinstance(self.relational_operator, RelationalKeyword) or isinstance(
            self.relational_operator, RelationalOperator
        ):
            relational_operator = self.relational_operator.value
        else:
            relational_operator = self.relational_operator

        value: list[str] | None | str | Unset
        if isinstance(self.value, Unset):
            value = UNSET
        elif isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if left_parenthesis is not UNSET:
            field_dict["leftParenthesis"] = left_parenthesis
        if right_parenthesis is not UNSET:
            field_dict["rightParenthesis"] = right_parenthesis
        if logical_operator is not UNSET:
            field_dict["logicalOperator"] = logical_operator
        if attribute_name is not UNSET:
            field_dict["attributeName"] = attribute_name
        if relational_operator is not UNSET:
            field_dict["relationalOperator"] = relational_operator
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_left_parenthesis(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        left_parenthesis = _parse_left_parenthesis(d.pop("leftParenthesis", UNSET))

        def _parse_right_parenthesis(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        right_parenthesis = _parse_right_parenthesis(d.pop("rightParenthesis", UNSET))

        def _parse_logical_operator(data: object) -> LogicalOperator | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                logical_operator_type_0 = LogicalOperator(data)

                return logical_operator_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(LogicalOperator | None | Unset, data)

        logical_operator = _parse_logical_operator(d.pop("logicalOperator", UNSET))

        def _parse_attribute_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        attribute_name = _parse_attribute_name(d.pop("attributeName", UNSET))

        def _parse_relational_operator(
            data: object,
        ) -> None | RelationalKeyword | RelationalOperator | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                relational_operator_type_0 = RelationalKeyword(data)

                return relational_operator_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                relational_operator_type_1 = RelationalOperator(data)

                return relational_operator_type_1
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | RelationalKeyword | RelationalOperator | Unset, data)

        relational_operator = _parse_relational_operator(d.pop("relationalOperator", UNSET))

        def _parse_value(data: object) -> list[str] | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_1 = cast(list[str], data)

                return value_type_1
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(list[str] | None | str | Unset, data)

        value = _parse_value(d.pop("value", UNSET))

        query_filter_json_part = cls(
            left_parenthesis=left_parenthesis,
            right_parenthesis=right_parenthesis,
            logical_operator=logical_operator,
            attribute_name=attribute_name,
            relational_operator=relational_operator,
            value=value,
        )

        query_filter_json_part.additional_properties = d
        return query_filter_json_part

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
