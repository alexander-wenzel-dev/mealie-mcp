from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GroupEventNotifierOptionsOut")


@_attrs_define
class GroupEventNotifierOptionsOut:
    """
    Attributes:
        test_message (bool):  Default: False.
        webhook_task (bool):  Default: False.
        recipe_created (bool):  Default: False.
        recipe_updated (bool):  Default: False.
        recipe_deleted (bool):  Default: False.
        user_signup (bool):  Default: False.
        data_migrations (bool):  Default: False.
        data_export (bool):  Default: False.
        data_import (bool):  Default: False.
        mealplan_entry_created (bool):  Default: False.
        mealplan_entry_updated (bool):  Default: False.
        mealplan_entry_deleted (bool):  Default: False.
        shopping_list_created (bool):  Default: False.
        shopping_list_updated (bool):  Default: False.
        shopping_list_deleted (bool):  Default: False.
        cookbook_created (bool):  Default: False.
        cookbook_updated (bool):  Default: False.
        cookbook_deleted (bool):  Default: False.
        tag_created (bool):  Default: False.
        tag_updated (bool):  Default: False.
        tag_deleted (bool):  Default: False.
        category_created (bool):  Default: False.
        category_updated (bool):  Default: False.
        category_deleted (bool):  Default: False.
        label_created (bool):  Default: False.
        label_updated (bool):  Default: False.
        label_deleted (bool):  Default: False.
        id (str):
    """

    id: str
    test_message: bool = False
    webhook_task: bool = False
    recipe_created: bool = False
    recipe_updated: bool = False
    recipe_deleted: bool = False
    user_signup: bool = False
    data_migrations: bool = False
    data_export: bool = False
    data_import: bool = False
    mealplan_entry_created: bool = False
    mealplan_entry_updated: bool = False
    mealplan_entry_deleted: bool = False
    shopping_list_created: bool = False
    shopping_list_updated: bool = False
    shopping_list_deleted: bool = False
    cookbook_created: bool = False
    cookbook_updated: bool = False
    cookbook_deleted: bool = False
    tag_created: bool = False
    tag_updated: bool = False
    tag_deleted: bool = False
    category_created: bool = False
    category_updated: bool = False
    category_deleted: bool = False
    label_created: bool = False
    label_updated: bool = False
    label_deleted: bool = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        test_message = self.test_message

        webhook_task = self.webhook_task

        recipe_created = self.recipe_created

        recipe_updated = self.recipe_updated

        recipe_deleted = self.recipe_deleted

        user_signup = self.user_signup

        data_migrations = self.data_migrations

        data_export = self.data_export

        data_import = self.data_import

        mealplan_entry_created = self.mealplan_entry_created

        mealplan_entry_updated = self.mealplan_entry_updated

        mealplan_entry_deleted = self.mealplan_entry_deleted

        shopping_list_created = self.shopping_list_created

        shopping_list_updated = self.shopping_list_updated

        shopping_list_deleted = self.shopping_list_deleted

        cookbook_created = self.cookbook_created

        cookbook_updated = self.cookbook_updated

        cookbook_deleted = self.cookbook_deleted

        tag_created = self.tag_created

        tag_updated = self.tag_updated

        tag_deleted = self.tag_deleted

        category_created = self.category_created

        category_updated = self.category_updated

        category_deleted = self.category_deleted

        label_created = self.label_created

        label_updated = self.label_updated

        label_deleted = self.label_deleted

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "testMessage": test_message,
                "webhookTask": webhook_task,
                "recipeCreated": recipe_created,
                "recipeUpdated": recipe_updated,
                "recipeDeleted": recipe_deleted,
                "userSignup": user_signup,
                "dataMigrations": data_migrations,
                "dataExport": data_export,
                "dataImport": data_import,
                "mealplanEntryCreated": mealplan_entry_created,
                "mealplanEntryUpdated": mealplan_entry_updated,
                "mealplanEntryDeleted": mealplan_entry_deleted,
                "shoppingListCreated": shopping_list_created,
                "shoppingListUpdated": shopping_list_updated,
                "shoppingListDeleted": shopping_list_deleted,
                "cookbookCreated": cookbook_created,
                "cookbookUpdated": cookbook_updated,
                "cookbookDeleted": cookbook_deleted,
                "tagCreated": tag_created,
                "tagUpdated": tag_updated,
                "tagDeleted": tag_deleted,
                "categoryCreated": category_created,
                "categoryUpdated": category_updated,
                "categoryDeleted": category_deleted,
                "labelCreated": label_created,
                "labelUpdated": label_updated,
                "labelDeleted": label_deleted,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        test_message = d.pop("testMessage")

        webhook_task = d.pop("webhookTask")

        recipe_created = d.pop("recipeCreated")

        recipe_updated = d.pop("recipeUpdated")

        recipe_deleted = d.pop("recipeDeleted")

        user_signup = d.pop("userSignup")

        data_migrations = d.pop("dataMigrations")

        data_export = d.pop("dataExport")

        data_import = d.pop("dataImport")

        mealplan_entry_created = d.pop("mealplanEntryCreated")

        mealplan_entry_updated = d.pop("mealplanEntryUpdated")

        mealplan_entry_deleted = d.pop("mealplanEntryDeleted")

        shopping_list_created = d.pop("shoppingListCreated")

        shopping_list_updated = d.pop("shoppingListUpdated")

        shopping_list_deleted = d.pop("shoppingListDeleted")

        cookbook_created = d.pop("cookbookCreated")

        cookbook_updated = d.pop("cookbookUpdated")

        cookbook_deleted = d.pop("cookbookDeleted")

        tag_created = d.pop("tagCreated")

        tag_updated = d.pop("tagUpdated")

        tag_deleted = d.pop("tagDeleted")

        category_created = d.pop("categoryCreated")

        category_updated = d.pop("categoryUpdated")

        category_deleted = d.pop("categoryDeleted")

        label_created = d.pop("labelCreated")

        label_updated = d.pop("labelUpdated")

        label_deleted = d.pop("labelDeleted")

        id = d.pop("id")

        group_event_notifier_options_out = cls(
            test_message=test_message,
            webhook_task=webhook_task,
            recipe_created=recipe_created,
            recipe_updated=recipe_updated,
            recipe_deleted=recipe_deleted,
            user_signup=user_signup,
            data_migrations=data_migrations,
            data_export=data_export,
            data_import=data_import,
            mealplan_entry_created=mealplan_entry_created,
            mealplan_entry_updated=mealplan_entry_updated,
            mealplan_entry_deleted=mealplan_entry_deleted,
            shopping_list_created=shopping_list_created,
            shopping_list_updated=shopping_list_updated,
            shopping_list_deleted=shopping_list_deleted,
            cookbook_created=cookbook_created,
            cookbook_updated=cookbook_updated,
            cookbook_deleted=cookbook_deleted,
            tag_created=tag_created,
            tag_updated=tag_updated,
            tag_deleted=tag_deleted,
            category_created=category_created,
            category_updated=category_updated,
            category_deleted=category_deleted,
            label_created=label_created,
            label_updated=label_updated,
            label_deleted=label_deleted,
            id=id,
        )

        group_event_notifier_options_out.additional_properties = d
        return group_event_notifier_options_out

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
