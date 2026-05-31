from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types

T = TypeVar("T", bound="BodyUploadRecipeAssetApiRecipesSlugAssetsPost")


@_attrs_define
class BodyUploadRecipeAssetApiRecipesSlugAssetsPost:
    """
    Attributes:
        name (str):
        icon (str):
        extension (str):
        file (str):
    """

    name: str
    icon: str
    extension: str
    file: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        icon = self.icon

        extension = self.extension

        file = self.file

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "icon": icon,
                "extension": extension,
                "file": file,
            }
        )

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("name", (None, str(self.name).encode(), "text/plain")))

        files.append(("icon", (None, str(self.icon).encode(), "text/plain")))

        files.append(("extension", (None, str(self.extension).encode(), "text/plain")))

        files.append(("file", (None, str(self.file).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        icon = d.pop("icon")

        extension = d.pop("extension")

        file = d.pop("file")

        body_upload_recipe_asset_api_recipes_slug_assets_post = cls(
            name=name,
            icon=icon,
            extension=extension,
            file=file,
        )

        body_upload_recipe_asset_api_recipes_slug_assets_post.additional_properties = d
        return body_upload_recipe_asset_api_recipes_slug_assets_post

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
