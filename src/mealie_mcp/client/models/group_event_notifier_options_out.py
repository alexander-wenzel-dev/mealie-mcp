from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GroupEventNotifierOptionsOut")


@_attrs_define
class GroupEventNotifierOptionsOut:
    """
    Attributes:
        id (str):
        test_message (bool | Unset):  Default: False.
        webhook_task (bool | Unset):  Default: False.
        recipe_created (bool | Unset):  Default: False.
        recipe_updated (bool | Unset):  Default: False.
        recipe_deleted (bool | Unset):  Default: False.
        user_signup (bool | Unset):  Default: False.
        data_migrations (bool | Unset):  Default: False.
        data_export (bool | Unset):  Default: False.
        data_import (bool | Unset):  Default: False.
        mealplan_entry_created (bool | Unset):  Default: False.
        mealplan_entry_updated (bool | Unset):  Default: False.
        mealplan_entry_deleted (bool | Unset):  Default: False.
        shopping_list_created (bool | Unset):  Default: False.
        shopping_list_updated (bool | Unset):  Default: False.
        shopping_list_deleted (bool | Unset):  Default: False.
        cookbook_created (bool | Unset):  Default: False.
        cookbook_updated (bool | Unset):  Default: False.
        cookbook_deleted (bool | Unset):  Default: False.
        tag_created (bool | Unset):  Default: False.
        tag_updated (bool | Unset):  Default: False.
        tag_deleted (bool | Unset):  Default: False.
        category_created (bool | Unset):  Default: False.
        category_updated (bool | Unset):  Default: False.
        category_deleted (bool | Unset):  Default: False.
        label_created (bool | Unset):  Default: False.
        label_updated (bool | Unset):  Default: False.
        label_deleted (bool | Unset):  Default: False.
    """

    id: str
    test_message: bool | Unset = False
    webhook_task: bool | Unset = False
    recipe_created: bool | Unset = False
    recipe_updated: bool | Unset = False
    recipe_deleted: bool | Unset = False
    user_signup: bool | Unset = False
    data_migrations: bool | Unset = False
    data_export: bool | Unset = False
    data_import: bool | Unset = False
    mealplan_entry_created: bool | Unset = False
    mealplan_entry_updated: bool | Unset = False
    mealplan_entry_deleted: bool | Unset = False
    shopping_list_created: bool | Unset = False
    shopping_list_updated: bool | Unset = False
    shopping_list_deleted: bool | Unset = False
    cookbook_created: bool | Unset = False
    cookbook_updated: bool | Unset = False
    cookbook_deleted: bool | Unset = False
    tag_created: bool | Unset = False
    tag_updated: bool | Unset = False
    tag_deleted: bool | Unset = False
    category_created: bool | Unset = False
    category_updated: bool | Unset = False
    category_deleted: bool | Unset = False
    label_created: bool | Unset = False
    label_updated: bool | Unset = False
    label_deleted: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if test_message is not UNSET:
            field_dict["testMessage"] = test_message
        if webhook_task is not UNSET:
            field_dict["webhookTask"] = webhook_task
        if recipe_created is not UNSET:
            field_dict["recipeCreated"] = recipe_created
        if recipe_updated is not UNSET:
            field_dict["recipeUpdated"] = recipe_updated
        if recipe_deleted is not UNSET:
            field_dict["recipeDeleted"] = recipe_deleted
        if user_signup is not UNSET:
            field_dict["userSignup"] = user_signup
        if data_migrations is not UNSET:
            field_dict["dataMigrations"] = data_migrations
        if data_export is not UNSET:
            field_dict["dataExport"] = data_export
        if data_import is not UNSET:
            field_dict["dataImport"] = data_import
        if mealplan_entry_created is not UNSET:
            field_dict["mealplanEntryCreated"] = mealplan_entry_created
        if mealplan_entry_updated is not UNSET:
            field_dict["mealplanEntryUpdated"] = mealplan_entry_updated
        if mealplan_entry_deleted is not UNSET:
            field_dict["mealplanEntryDeleted"] = mealplan_entry_deleted
        if shopping_list_created is not UNSET:
            field_dict["shoppingListCreated"] = shopping_list_created
        if shopping_list_updated is not UNSET:
            field_dict["shoppingListUpdated"] = shopping_list_updated
        if shopping_list_deleted is not UNSET:
            field_dict["shoppingListDeleted"] = shopping_list_deleted
        if cookbook_created is not UNSET:
            field_dict["cookbookCreated"] = cookbook_created
        if cookbook_updated is not UNSET:
            field_dict["cookbookUpdated"] = cookbook_updated
        if cookbook_deleted is not UNSET:
            field_dict["cookbookDeleted"] = cookbook_deleted
        if tag_created is not UNSET:
            field_dict["tagCreated"] = tag_created
        if tag_updated is not UNSET:
            field_dict["tagUpdated"] = tag_updated
        if tag_deleted is not UNSET:
            field_dict["tagDeleted"] = tag_deleted
        if category_created is not UNSET:
            field_dict["categoryCreated"] = category_created
        if category_updated is not UNSET:
            field_dict["categoryUpdated"] = category_updated
        if category_deleted is not UNSET:
            field_dict["categoryDeleted"] = category_deleted
        if label_created is not UNSET:
            field_dict["labelCreated"] = label_created
        if label_updated is not UNSET:
            field_dict["labelUpdated"] = label_updated
        if label_deleted is not UNSET:
            field_dict["labelDeleted"] = label_deleted

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        test_message = d.pop("testMessage", UNSET)

        webhook_task = d.pop("webhookTask", UNSET)

        recipe_created = d.pop("recipeCreated", UNSET)

        recipe_updated = d.pop("recipeUpdated", UNSET)

        recipe_deleted = d.pop("recipeDeleted", UNSET)

        user_signup = d.pop("userSignup", UNSET)

        data_migrations = d.pop("dataMigrations", UNSET)

        data_export = d.pop("dataExport", UNSET)

        data_import = d.pop("dataImport", UNSET)

        mealplan_entry_created = d.pop("mealplanEntryCreated", UNSET)

        mealplan_entry_updated = d.pop("mealplanEntryUpdated", UNSET)

        mealplan_entry_deleted = d.pop("mealplanEntryDeleted", UNSET)

        shopping_list_created = d.pop("shoppingListCreated", UNSET)

        shopping_list_updated = d.pop("shoppingListUpdated", UNSET)

        shopping_list_deleted = d.pop("shoppingListDeleted", UNSET)

        cookbook_created = d.pop("cookbookCreated", UNSET)

        cookbook_updated = d.pop("cookbookUpdated", UNSET)

        cookbook_deleted = d.pop("cookbookDeleted", UNSET)

        tag_created = d.pop("tagCreated", UNSET)

        tag_updated = d.pop("tagUpdated", UNSET)

        tag_deleted = d.pop("tagDeleted", UNSET)

        category_created = d.pop("categoryCreated", UNSET)

        category_updated = d.pop("categoryUpdated", UNSET)

        category_deleted = d.pop("categoryDeleted", UNSET)

        label_created = d.pop("labelCreated", UNSET)

        label_updated = d.pop("labelUpdated", UNSET)

        label_deleted = d.pop("labelDeleted", UNSET)

        group_event_notifier_options_out = cls(
            id=id,
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
