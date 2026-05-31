from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types

T = TypeVar("T", bound="BodyUpdateEventImageApiRecipesTimelineEventsItemIdImagePut")


@_attrs_define
class BodyUpdateEventImageApiRecipesTimelineEventsItemIdImagePut:
    """
    Attributes:
        image (str):
        extension (str):
    """

    image: str
    extension: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image = self.image

        extension = self.extension

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "image": image,
                "extension": extension,
            }
        )

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("image", (None, str(self.image).encode(), "text/plain")))

        files.append(("extension", (None, str(self.extension).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        image = d.pop("image")

        extension = d.pop("extension")

        body_update_event_image_api_recipes_timeline_events_item_id_image_put = cls(
            image=image,
            extension=extension,
        )

        body_update_event_image_api_recipes_timeline_events_item_id_image_put.additional_properties = d
        return body_update_event_image_api_recipes_timeline_events_item_id_image_put

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
