from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.timeline_event_image import TimelineEventImage
from ..types import UNSET, Unset

T = TypeVar("T", bound="RecipeTimelineEventUpdate")


@_attrs_define
class RecipeTimelineEventUpdate:
    """
    Attributes:
        subject (str):
        event_message (None | str | Unset):
        image (None | TimelineEventImage | Unset):
    """

    subject: str
    event_message: None | str | Unset = UNSET
    image: None | TimelineEventImage | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        subject = self.subject

        event_message: None | str | Unset
        if isinstance(self.event_message, Unset):
            event_message = UNSET
        else:
            event_message = self.event_message

        image: None | str | Unset
        if isinstance(self.image, Unset):
            image = UNSET
        elif isinstance(self.image, TimelineEventImage):
            image = self.image.value
        else:
            image = self.image

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "subject": subject,
            }
        )
        if event_message is not UNSET:
            field_dict["eventMessage"] = event_message
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        subject = d.pop("subject")

        def _parse_event_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        event_message = _parse_event_message(d.pop("eventMessage", UNSET))

        def _parse_image(data: object) -> None | TimelineEventImage | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                image_type_0 = TimelineEventImage(data)

                return image_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | TimelineEventImage | Unset, data)

        image = _parse_image(d.pop("image", UNSET))

        recipe_timeline_event_update = cls(
            subject=subject,
            event_message=event_message,
            image=image,
        )

        recipe_timeline_event_update.additional_properties = d
        return recipe_timeline_event_update

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
