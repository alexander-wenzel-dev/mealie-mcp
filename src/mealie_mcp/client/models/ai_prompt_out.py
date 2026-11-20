from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ai_prompt_mode import AIPromptMode

T = TypeVar("T", bound="AIPromptOut")


@_attrs_define
class AIPromptOut:
    """
    Attributes:
        name (str):
        is_system (bool):
        default_content (str):
        mode (AIPromptMode | None):
        content (None | str):
        default_changed (bool):  Default: False.
    """

    name: str
    is_system: bool
    default_content: str
    mode: AIPromptMode | None
    content: str | None
    default_changed: bool = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        is_system = self.is_system

        default_content = self.default_content

        mode: str | None
        if isinstance(self.mode, AIPromptMode):
            mode = self.mode.value
        else:
            mode = self.mode

        content: str | None
        content = self.content

        default_changed = self.default_changed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "isSystem": is_system,
                "defaultContent": default_content,
                "mode": mode,
                "content": content,
                "defaultChanged": default_changed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        is_system = d.pop("isSystem")

        default_content = d.pop("defaultContent")

        def _parse_mode(data: object) -> AIPromptMode | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mode_type_0 = AIPromptMode(data)

                return mode_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(AIPromptMode | None, data)

        mode = _parse_mode(d.pop("mode"))

        def _parse_content(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        content = _parse_content(d.pop("content"))

        default_changed = d.pop("defaultChanged")

        ai_prompt_out = cls(
            name=name,
            is_system=is_system,
            default_content=default_content,
            mode=mode,
            content=content,
            default_changed=default_changed,
        )

        ai_prompt_out.additional_properties = d
        return ai_prompt_out

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
