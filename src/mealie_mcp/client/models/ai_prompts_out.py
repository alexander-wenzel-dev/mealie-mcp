from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ai_prompt_out import AIPromptOut


T = TypeVar("T", bound="AIPromptsOut")


@_attrs_define
class AIPromptsOut:
    """
    Attributes:
        global_instructions (None | str):
        prompts (list[AIPromptOut]):
    """

    global_instructions: str | None
    prompts: list[AIPromptOut]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        global_instructions: str | None
        global_instructions = self.global_instructions

        prompts = []
        for prompts_item_data in self.prompts:
            prompts_item = prompts_item_data.to_dict()
            prompts.append(prompts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "globalInstructions": global_instructions,
                "prompts": prompts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ai_prompt_out import AIPromptOut  # noqa: PLC0415

        d = dict(src_dict)

        def _parse_global_instructions(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        global_instructions = _parse_global_instructions(d.pop("globalInstructions"))

        prompts = []
        _prompts = d.pop("prompts")
        for prompts_item_data in _prompts:
            prompts_item = AIPromptOut.from_dict(prompts_item_data)

            prompts.append(prompts_item)

        ai_prompts_out = cls(
            global_instructions=global_instructions,
            prompts=prompts,
        )

        ai_prompts_out.additional_properties = d
        return ai_prompts_out

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
