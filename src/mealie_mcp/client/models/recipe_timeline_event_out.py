from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.timeline_event_image import TimelineEventImage
from ..models.timeline_event_type import TimelineEventType
from ..types import UNSET, Unset

T = TypeVar("T", bound="RecipeTimelineEventOut")


@_attrs_define
class RecipeTimelineEventOut:
    """
    Attributes:
        recipe_id (str):
        user_id (str):
        subject (str):
        event_type (TimelineEventType):
        id (str):
        group_id (str):
        household_id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        event_message (None | str | Unset):
        image (None | TimelineEventImage | Unset):  Default: TimelineEventImage.DOES_NOT_HAVE_IMAGE.
        timestamp (datetime.datetime | Unset):  Default: datetime.datetime.fromisoformat('2026-06-27T04:10:24.507252Z').
    """

    recipe_id: str
    user_id: str
    subject: str
    event_type: TimelineEventType
    id: str
    group_id: str
    household_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    event_message: None | str | Unset = UNSET
    image: None | TimelineEventImage | Unset = TimelineEventImage.DOES_NOT_HAVE_IMAGE
    timestamp: datetime.datetime | Unset = datetime.datetime.fromisoformat(
        "2026-06-27T04:10:24.507252Z"
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_id = self.recipe_id

        user_id = self.user_id

        subject = self.subject

        event_type = self.event_type.value

        id = self.id

        group_id = self.group_id

        household_id = self.household_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

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

        timestamp: str | Unset = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipeId": recipe_id,
                "userId": user_id,
                "subject": subject,
                "eventType": event_type,
                "id": id,
                "groupId": group_id,
                "householdId": household_id,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )
        if event_message is not UNSET:
            field_dict["eventMessage"] = event_message
        if image is not UNSET:
            field_dict["image"] = image
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recipe_id = d.pop("recipeId")

        user_id = d.pop("userId")

        subject = d.pop("subject")

        event_type = TimelineEventType(d.pop("eventType"))

        id = d.pop("id")

        group_id = d.pop("groupId")

        household_id = d.pop("householdId")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))

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

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: datetime.datetime | Unset
        if isinstance(_timestamp, Unset):
            timestamp = UNSET
        else:
            timestamp = datetime.datetime.fromisoformat(_timestamp)

        recipe_timeline_event_out = cls(
            recipe_id=recipe_id,
            user_id=user_id,
            subject=subject,
            event_type=event_type,
            id=id,
            group_id=group_id,
            household_id=household_id,
            created_at=created_at,
            updated_at=updated_at,
            event_message=event_message,
            image=image,
            timestamp=timestamp,
        )

        recipe_timeline_event_out.additional_properties = d
        return recipe_timeline_event_out

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
