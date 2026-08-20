from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, Unset

T = TypeVar("T", bound="BodyCreateRecipeWithAiStreamApiRecipesCreateAiStreamPost")


@_attrs_define
class BodyCreateRecipeWithAiStreamApiRecipesCreateAiStreamPost:
    """
    Attributes:
        content (None | str | Unset):
        url (None | str | Unset):
        translate_language (None | str | Unset):
        create_new_organizers (bool | Unset):  Default: False.
        images (list[str] | Unset):
    """

    content: str | Unset | None = UNSET
    url: str | Unset | None = UNSET
    translate_language: str | Unset | None = UNSET
    create_new_organizers: bool | Unset = False
    images: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content: str | Unset | None
        if isinstance(self.content, Unset):
            content = UNSET
        else:
            content = self.content

        url: str | Unset | None
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        translate_language: str | Unset | None
        if isinstance(self.translate_language, Unset):
            translate_language = UNSET
        else:
            translate_language = self.translate_language

        create_new_organizers = self.create_new_organizers

        images: list[str] | Unset = UNSET
        if not isinstance(self.images, Unset):
            images = self.images

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if content is not UNSET:
            field_dict["content"] = content
        if url is not UNSET:
            field_dict["url"] = url
        if translate_language is not UNSET:
            field_dict["translateLanguage"] = translate_language
        if create_new_organizers is not UNSET:
            field_dict["createNewOrganizers"] = create_new_organizers
        if images is not UNSET:
            field_dict["images"] = images

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        if not isinstance(self.content, Unset):
            if isinstance(self.content, str):
                files.append(("content", (None, str(self.content).encode(), "text/plain")))
            else:
                files.append(("content", (None, str(self.content).encode(), "text/plain")))

        if not isinstance(self.url, Unset):
            if isinstance(self.url, str):
                files.append(("url", (None, str(self.url).encode(), "text/plain")))
            else:
                files.append(("url", (None, str(self.url).encode(), "text/plain")))

        if not isinstance(self.translate_language, Unset):
            if isinstance(self.translate_language, str):
                files.append(
                    (
                        "translateLanguage",
                        (None, str(self.translate_language).encode(), "text/plain"),
                    )
                )
            else:
                files.append(
                    (
                        "translateLanguage",
                        (None, str(self.translate_language).encode(), "text/plain"),
                    )
                )

        if not isinstance(self.create_new_organizers, Unset):
            files.append(
                (
                    "createNewOrganizers",
                    (None, str(self.create_new_organizers).encode(), "text/plain"),
                )
            )

        if not isinstance(self.images, Unset):
            for images_item_element in self.images:
                files.append(("images", (None, str(images_item_element).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_content(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        content = _parse_content(d.pop("content", UNSET))

        def _parse_url(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        url = _parse_url(d.pop("url", UNSET))

        def _parse_translate_language(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        translate_language = _parse_translate_language(d.pop("translateLanguage", UNSET))

        create_new_organizers = d.pop("createNewOrganizers", UNSET)

        images = cast(list[str], d.pop("images", UNSET))

        body_create_recipe_with_ai_stream_api_recipes_create_ai_stream_post = cls(
            content=content,
            url=url,
            translate_language=translate_language,
            create_new_organizers=create_new_organizers,
            images=images,
        )

        body_create_recipe_with_ai_stream_api_recipes_create_ai_stream_post.additional_properties = d
        return body_create_recipe_with_ai_stream_api_recipes_create_ai_stream_post

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
