from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ai_provider_summary import AIProviderSummary


T = TypeVar("T", bound="AIProviderSettingsOut")


@_attrs_define
class AIProviderSettingsOut:
    """
    Attributes:
        default_provider_id (None | str):
        audio_provider_id (None | str):
        image_provider_id (None | str):
        providers (list[AIProviderSummary]):
        ai_enabled (bool):
        audio_provider_enabled (bool):
        image_provider_enabled (bool):
    """

    default_provider_id: None | str
    audio_provider_id: None | str
    image_provider_id: None | str
    providers: list[AIProviderSummary]
    ai_enabled: bool
    audio_provider_enabled: bool
    image_provider_enabled: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        default_provider_id: None | str
        default_provider_id = self.default_provider_id

        audio_provider_id: None | str
        audio_provider_id = self.audio_provider_id

        image_provider_id: None | str
        image_provider_id = self.image_provider_id

        providers = []
        for providers_item_data in self.providers:
            providers_item = providers_item_data.to_dict()
            providers.append(providers_item)

        ai_enabled = self.ai_enabled

        audio_provider_enabled = self.audio_provider_enabled

        image_provider_enabled = self.image_provider_enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "defaultProviderId": default_provider_id,
                "audioProviderId": audio_provider_id,
                "imageProviderId": image_provider_id,
                "providers": providers,
                "aiEnabled": ai_enabled,
                "audioProviderEnabled": audio_provider_enabled,
                "imageProviderEnabled": image_provider_enabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ai_provider_summary import AIProviderSummary

        d = dict(src_dict)

        def _parse_default_provider_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        default_provider_id = _parse_default_provider_id(d.pop("defaultProviderId"))

        def _parse_audio_provider_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        audio_provider_id = _parse_audio_provider_id(d.pop("audioProviderId"))

        def _parse_image_provider_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        image_provider_id = _parse_image_provider_id(d.pop("imageProviderId"))

        providers = []
        _providers = d.pop("providers")
        for providers_item_data in _providers:
            providers_item = AIProviderSummary.from_dict(providers_item_data)

            providers.append(providers_item)

        ai_enabled = d.pop("aiEnabled")

        audio_provider_enabled = d.pop("audioProviderEnabled")

        image_provider_enabled = d.pop("imageProviderEnabled")

        ai_provider_settings_out = cls(
            default_provider_id=default_provider_id,
            audio_provider_id=audio_provider_id,
            image_provider_id=image_provider_id,
            providers=providers,
            ai_enabled=ai_enabled,
            audio_provider_enabled=audio_provider_enabled,
            image_provider_enabled=image_provider_enabled,
        )

        ai_provider_settings_out.additional_properties = d
        return ai_provider_settings_out

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
