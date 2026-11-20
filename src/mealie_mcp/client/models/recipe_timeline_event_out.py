from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.timeline_event_image import TimelineEventImage
from ..models.timeline_event_type import TimelineEventType

T = TypeVar("T", bound="RecipeTimelineEventOut")


@_attrs_define
class RecipeTimelineEventOut:
    """
    Attributes:
        recipe_id (str):
        user_id (str):
        subject (str):
        event_type (TimelineEventType):
        event_message (None | str):
        image (None | TimelineEventImage):  Default: TimelineEventImage.DOES_NOT_HAVE_IMAGE.
        timestamp (datetime.datetime):
        id (str):
        group_id (str):
        household_id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    recipe_id: str
    user_id: str
    subject: str
    event_type: TimelineEventType
    event_message: str | None
    timestamp: datetime.datetime
    id: str
    group_id: str
    household_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    image: TimelineEventImage | None = TimelineEventImage.DOES_NOT_HAVE_IMAGE
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_id = self.recipe_id

        user_id = self.user_id

        subject = self.subject

        event_type = self.event_type.value

        event_message: str | None
        event_message = self.event_message

        image: str | None
        if isinstance(self.image, TimelineEventImage):
            image = self.image.value
        else:
            image = self.image

        timestamp = self.timestamp.isoformat()

        id = self.id

        group_id = self.group_id

        household_id = self.household_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipeId": recipe_id,
                "userId": user_id,
                "subject": subject,
                "eventType": event_type,
                "eventMessage": event_message,
                "image": image,
                "timestamp": timestamp,
                "id": id,
                "groupId": group_id,
                "householdId": household_id,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recipe_id = d.pop("recipeId")

        user_id = d.pop("userId")

        subject = d.pop("subject")

        event_type = TimelineEventType(d.pop("eventType"))

        def _parse_event_message(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        event_message = _parse_event_message(d.pop("eventMessage"))

        def _parse_image(data: object) -> TimelineEventImage | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                image_type_0 = TimelineEventImage(data)

                return image_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | TimelineEventImage, data)

        image = _parse_image(d.pop("image"))

        timestamp = datetime.datetime.fromisoformat(d.pop("timestamp"))

        id = d.pop("id")

        group_id = d.pop("groupId")

        household_id = d.pop("householdId")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))

        recipe_timeline_event_out = cls(
            recipe_id=recipe_id,
            user_id=user_id,
            subject=subject,
            event_type=event_type,
            event_message=event_message,
            image=image,
            timestamp=timestamp,
            id=id,
            group_id=group_id,
            household_id=household_id,
            created_at=created_at,
            updated_at=updated_at,
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
