from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ai_provider_out_requestheaders import AIProviderOutRequestheaders
    from ..models.ai_provider_out_requestparams import AIProviderOutRequestparams


T = TypeVar("T", bound="AIProviderOut")


@_attrs_define
class AIProviderOut:
    """
    Attributes:
        name (str):
        base_url (None | str):
        model (str):
        timeout (int):  Default: 300.
        request_headers (AIProviderOutRequestheaders):
        request_params (AIProviderOutRequestparams):
        id (str):
    """

    name: str
    base_url: str | None
    model: str
    request_headers: AIProviderOutRequestheaders
    request_params: AIProviderOutRequestparams
    id: str
    timeout: int = 300
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        base_url: str | None
        base_url = self.base_url

        model = self.model

        timeout = self.timeout

        request_headers = self.request_headers.to_dict()

        request_params = self.request_params.to_dict()

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "baseUrl": base_url,
                "model": model,
                "timeout": timeout,
                "requestHeaders": request_headers,
                "requestParams": request_params,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ai_provider_out_requestheaders import AIProviderOutRequestheaders  # noqa: PLC0415
        from ..models.ai_provider_out_requestparams import AIProviderOutRequestparams  # noqa: PLC0415

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_base_url(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        base_url = _parse_base_url(d.pop("baseUrl"))

        model = d.pop("model")

        timeout = d.pop("timeout")

        request_headers = AIProviderOutRequestheaders.from_dict(d.pop("requestHeaders"))

        request_params = AIProviderOutRequestparams.from_dict(d.pop("requestParams"))

        id = d.pop("id")

        ai_provider_out = cls(
            name=name,
            base_url=base_url,
            model=model,
            timeout=timeout,
            request_headers=request_headers,
            request_params=request_params,
            id=id,
        )

        ai_provider_out.additional_properties = d
        return ai_provider_out

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
