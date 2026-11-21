from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.category_draft import CategoryDraft
    from ..models.nutrition import Nutrition
    from ..models.recipe_asset import RecipeAsset
    from ..models.recipe_comment_out import RecipeCommentOut
    from ..models.recipe_draft_extras import RecipeDraftExtras
    from ..models.recipe_ingredient import RecipeIngredient
    from ..models.recipe_note import RecipeNote
    from ..models.recipe_settings import RecipeSettings
    from ..models.recipe_step import RecipeStep
    from ..models.tag_draft import TagDraft
    from ..models.tool_draft import ToolDraft


T = TypeVar("T", bound="RecipeDraft")


@_attrs_define
class RecipeDraft:
    """A recipe that is not saved yet, or a client's edit of a saved one.

    Scrapers, importers and migrations build drafts, and the recipe write routes accept them as request
    bodies. Every field is optional: RecipeService sets the owner when it saves a new draft, and the
    repository keeps the stored id and owner when a draft updates a saved recipe. Read a saved recipe
    back as `Recipe`, which guarantees those fields.

    A draft can carry an id before it is saved, so that files such as a scraped image can be written to
    the recipe's directory first.

        Attributes:
            id (None | str | Unset):
            user_id (None | str | Unset):
            household_id (None | str | Unset):
            group_id (None | str | Unset):
            name (None | str | Unset):
            slug (str | Unset):  Default: ''.
            image (Any | None | Unset):
            recipe_servings (float | Unset):  Default: 0.0.
            recipe_yield_quantity (float | Unset):  Default: 0.0.
            recipe_yield (None | str | Unset):
            total_time (None | str | Unset):
            prep_time (None | str | Unset):
            perform_time (None | str | Unset):
            total_time_seconds (int | None | Unset):
            prep_time_seconds (int | None | Unset):
            perform_time_seconds (int | None | Unset):
            description (None | str | Unset):  Default: ''.
            recipe_category (list[CategoryDraft] | Unset):
            tags (list[TagDraft] | Unset):
            tools (list[ToolDraft] | Unset):
            rating (float | None | Unset):
            org_url (None | str | Unset):
            date_added (datetime.date | None | Unset):
            date_updated (datetime.datetime | None | Unset):
            created_at (datetime.datetime | None | Unset):
            update_at (datetime.datetime | None | Unset):
            recipe_ingredient (list[RecipeIngredient] | Unset):
            recipe_instructions (list[RecipeStep] | Unset):
            nutrition (None | Nutrition | Unset):
            settings (None | RecipeSettings | Unset):
            assets (list[RecipeAsset] | Unset):
            notes (list[RecipeNote] | Unset):
            extras (RecipeDraftExtras | Unset):
            comments (list[RecipeCommentOut] | Unset):
    """

    id: str | Unset | None = UNSET
    user_id: str | Unset | None = UNSET
    household_id: str | Unset | None = UNSET
    group_id: str | Unset | None = UNSET
    name: str | Unset | None = UNSET
    slug: str | Unset = ""
    image: Any | Unset | None = UNSET
    recipe_servings: float | Unset = 0.0
    recipe_yield_quantity: float | Unset = 0.0
    recipe_yield: str | Unset | None = UNSET
    total_time: str | Unset | None = UNSET
    prep_time: str | Unset | None = UNSET
    perform_time: str | Unset | None = UNSET
    total_time_seconds: int | Unset | None = UNSET
    prep_time_seconds: int | Unset | None = UNSET
    perform_time_seconds: int | Unset | None = UNSET
    description: str | Unset | None = ""
    recipe_category: list[CategoryDraft] | Unset = UNSET
    tags: list[TagDraft] | Unset = UNSET
    tools: list[ToolDraft] | Unset = UNSET
    rating: float | Unset | None = UNSET
    org_url: str | Unset | None = UNSET
    date_added: datetime.date | Unset | None = UNSET
    date_updated: datetime.datetime | Unset | None = UNSET
    created_at: datetime.datetime | Unset | None = UNSET
    update_at: datetime.datetime | Unset | None = UNSET
    recipe_ingredient: list[RecipeIngredient] | Unset = UNSET
    recipe_instructions: list[RecipeStep] | Unset = UNSET
    nutrition: Nutrition | Unset | None = UNSET
    settings: RecipeSettings | Unset | None = UNSET
    assets: list[RecipeAsset] | Unset = UNSET
    notes: list[RecipeNote] | Unset = UNSET
    extras: RecipeDraftExtras | Unset = UNSET
    comments: list[RecipeCommentOut] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.nutrition import Nutrition  # noqa: PLC0415
        from ..models.recipe_settings import RecipeSettings  # noqa: PLC0415

        id: str | Unset | None
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        user_id: str | Unset | None
        if isinstance(self.user_id, Unset):
            user_id = UNSET
        else:
            user_id = self.user_id

        household_id: str | Unset | None
        if isinstance(self.household_id, Unset):
            household_id = UNSET
        else:
            household_id = self.household_id

        group_id: str | Unset | None
        if isinstance(self.group_id, Unset):
            group_id = UNSET
        else:
            group_id = self.group_id

        name: str | Unset | None
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        slug = self.slug

        image: Any | Unset | None
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        recipe_servings = self.recipe_servings

        recipe_yield_quantity = self.recipe_yield_quantity

        recipe_yield: str | Unset | None
        if isinstance(self.recipe_yield, Unset):
            recipe_yield = UNSET
        else:
            recipe_yield = self.recipe_yield

        total_time: str | Unset | None
        if isinstance(self.total_time, Unset):
            total_time = UNSET
        else:
            total_time = self.total_time

        prep_time: str | Unset | None
        if isinstance(self.prep_time, Unset):
            prep_time = UNSET
        else:
            prep_time = self.prep_time

        perform_time: str | Unset | None
        if isinstance(self.perform_time, Unset):
            perform_time = UNSET
        else:
            perform_time = self.perform_time

        total_time_seconds: int | Unset | None
        if isinstance(self.total_time_seconds, Unset):
            total_time_seconds = UNSET
        else:
            total_time_seconds = self.total_time_seconds

        prep_time_seconds: int | Unset | None
        if isinstance(self.prep_time_seconds, Unset):
            prep_time_seconds = UNSET
        else:
            prep_time_seconds = self.prep_time_seconds

        perform_time_seconds: int | Unset | None
        if isinstance(self.perform_time_seconds, Unset):
            perform_time_seconds = UNSET
        else:
            perform_time_seconds = self.perform_time_seconds

        description: str | Unset | None
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        recipe_category: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.recipe_category, Unset):
            recipe_category = []
            for recipe_category_item_data in self.recipe_category:
                recipe_category_item = recipe_category_item_data.to_dict()
                recipe_category.append(recipe_category_item)

        tags: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data.to_dict()
                tags.append(tags_item)

        tools: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.tools, Unset):
            tools = []
            for tools_item_data in self.tools:
                tools_item = tools_item_data.to_dict()
                tools.append(tools_item)

        rating: float | Unset | None
        if isinstance(self.rating, Unset):
            rating = UNSET
        else:
            rating = self.rating

        org_url: str | Unset | None
        if isinstance(self.org_url, Unset):
            org_url = UNSET
        else:
            org_url = self.org_url

        date_added: str | Unset | None
        if isinstance(self.date_added, Unset):
            date_added = UNSET
        elif isinstance(self.date_added, datetime.date):
            date_added = self.date_added.isoformat()
        else:
            date_added = self.date_added

        date_updated: str | Unset | None
        if isinstance(self.date_updated, Unset):
            date_updated = UNSET
        elif isinstance(self.date_updated, datetime.datetime):
            date_updated = self.date_updated.isoformat()
        else:
            date_updated = self.date_updated

        created_at: str | Unset | None
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        update_at: str | Unset | None
        if isinstance(self.update_at, Unset):
            update_at = UNSET
        elif isinstance(self.update_at, datetime.datetime):
            update_at = self.update_at.isoformat()
        else:
            update_at = self.update_at

        recipe_ingredient: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.recipe_ingredient, Unset):
            recipe_ingredient = []
            for recipe_ingredient_item_data in self.recipe_ingredient:
                recipe_ingredient_item = recipe_ingredient_item_data.to_dict()
                recipe_ingredient.append(recipe_ingredient_item)

        recipe_instructions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.recipe_instructions, Unset):
            recipe_instructions = []
            for recipe_instructions_item_data in self.recipe_instructions:
                recipe_instructions_item = recipe_instructions_item_data.to_dict()
                recipe_instructions.append(recipe_instructions_item)

        nutrition: dict[str, Any] | Unset | None
        if isinstance(self.nutrition, Unset):
            nutrition = UNSET
        elif isinstance(self.nutrition, Nutrition):
            nutrition = self.nutrition.to_dict()
        else:
            nutrition = self.nutrition

        settings: dict[str, Any] | Unset | None
        if isinstance(self.settings, Unset):
            settings = UNSET
        elif isinstance(self.settings, RecipeSettings):
            settings = self.settings.to_dict()
        else:
            settings = self.settings

        assets: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.assets, Unset):
            assets = []
            for assets_item_data in self.assets:
                assets_item = assets_item_data.to_dict()
                assets.append(assets_item)

        notes: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.notes, Unset):
            notes = []
            for notes_item_data in self.notes:
                notes_item = notes_item_data.to_dict()
                notes.append(notes_item)

        extras: dict[str, Any] | Unset = UNSET
        if not isinstance(self.extras, Unset):
            extras = self.extras.to_dict()

        comments: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.comments, Unset):
            comments = []
            for comments_item_data in self.comments:
                comments_item = comments_item_data.to_dict()
                comments.append(comments_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if user_id is not UNSET:
            field_dict["userId"] = user_id
        if household_id is not UNSET:
            field_dict["householdId"] = household_id
        if group_id is not UNSET:
            field_dict["groupId"] = group_id
        if name is not UNSET:
            field_dict["name"] = name
        if slug is not UNSET:
            field_dict["slug"] = slug
        if image is not UNSET:
            field_dict["image"] = image
        if recipe_servings is not UNSET:
            field_dict["recipeServings"] = recipe_servings
        if recipe_yield_quantity is not UNSET:
            field_dict["recipeYieldQuantity"] = recipe_yield_quantity
        if recipe_yield is not UNSET:
            field_dict["recipeYield"] = recipe_yield
        if total_time is not UNSET:
            field_dict["totalTime"] = total_time
        if prep_time is not UNSET:
            field_dict["prepTime"] = prep_time
        if perform_time is not UNSET:
            field_dict["performTime"] = perform_time
        if total_time_seconds is not UNSET:
            field_dict["totalTimeSeconds"] = total_time_seconds
        if prep_time_seconds is not UNSET:
            field_dict["prepTimeSeconds"] = prep_time_seconds
        if perform_time_seconds is not UNSET:
            field_dict["performTimeSeconds"] = perform_time_seconds
        if description is not UNSET:
            field_dict["description"] = description
        if recipe_category is not UNSET:
            field_dict["recipeCategory"] = recipe_category
        if tags is not UNSET:
            field_dict["tags"] = tags
        if tools is not UNSET:
            field_dict["tools"] = tools
        if rating is not UNSET:
            field_dict["rating"] = rating
        if org_url is not UNSET:
            field_dict["orgURL"] = org_url
        if date_added is not UNSET:
            field_dict["dateAdded"] = date_added
        if date_updated is not UNSET:
            field_dict["dateUpdated"] = date_updated
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if update_at is not UNSET:
            field_dict["update_at"] = update_at
        if recipe_ingredient is not UNSET:
            field_dict["recipeIngredient"] = recipe_ingredient
        if recipe_instructions is not UNSET:
            field_dict["recipeInstructions"] = recipe_instructions
        if nutrition is not UNSET:
            field_dict["nutrition"] = nutrition
        if settings is not UNSET:
            field_dict["settings"] = settings
        if assets is not UNSET:
            field_dict["assets"] = assets
        if notes is not UNSET:
            field_dict["notes"] = notes
        if extras is not UNSET:
            field_dict["extras"] = extras
        if comments is not UNSET:
            field_dict["comments"] = comments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.category_draft import CategoryDraft  # noqa: PLC0415
        from ..models.nutrition import Nutrition  # noqa: PLC0415
        from ..models.recipe_asset import RecipeAsset  # noqa: PLC0415
        from ..models.recipe_comment_out import RecipeCommentOut  # noqa: PLC0415
        from ..models.recipe_draft_extras import RecipeDraftExtras  # noqa: PLC0415
        from ..models.recipe_ingredient import RecipeIngredient  # noqa: PLC0415
        from ..models.recipe_note import RecipeNote  # noqa: PLC0415
        from ..models.recipe_settings import RecipeSettings  # noqa: PLC0415
        from ..models.recipe_step import RecipeStep  # noqa: PLC0415
        from ..models.tag_draft import TagDraft  # noqa: PLC0415
        from ..models.tool_draft import ToolDraft  # noqa: PLC0415

        d = dict(src_dict)

        def _parse_id(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_user_id(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        user_id = _parse_user_id(d.pop("userId", UNSET))

        def _parse_household_id(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        household_id = _parse_household_id(d.pop("householdId", UNSET))

        def _parse_group_id(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        group_id = _parse_group_id(d.pop("groupId", UNSET))

        def _parse_name(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        slug = d.pop("slug", UNSET)

        def _parse_image(data: object) -> Any | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | None | Unset, data)

        image = _parse_image(d.pop("image", UNSET))

        recipe_servings = d.pop("recipeServings", UNSET)

        recipe_yield_quantity = d.pop("recipeYieldQuantity", UNSET)

        def _parse_recipe_yield(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        recipe_yield = _parse_recipe_yield(d.pop("recipeYield", UNSET))

        def _parse_total_time(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        total_time = _parse_total_time(d.pop("totalTime", UNSET))

        def _parse_prep_time(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prep_time = _parse_prep_time(d.pop("prepTime", UNSET))

        def _parse_perform_time(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        perform_time = _parse_perform_time(d.pop("performTime", UNSET))

        def _parse_total_time_seconds(data: object) -> int | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_time_seconds = _parse_total_time_seconds(d.pop("totalTimeSeconds", UNSET))

        def _parse_prep_time_seconds(data: object) -> int | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        prep_time_seconds = _parse_prep_time_seconds(d.pop("prepTimeSeconds", UNSET))

        def _parse_perform_time_seconds(data: object) -> int | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        perform_time_seconds = _parse_perform_time_seconds(d.pop("performTimeSeconds", UNSET))

        def _parse_description(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _recipe_category = d.pop("recipeCategory", UNSET)
        recipe_category: list[CategoryDraft] | Unset = UNSET
        if _recipe_category is not UNSET:
            recipe_category = []
            for recipe_category_item_data in _recipe_category:
                recipe_category_item = CategoryDraft.from_dict(recipe_category_item_data)

                recipe_category.append(recipe_category_item)

        _tags = d.pop("tags", UNSET)
        tags: list[TagDraft] | Unset = UNSET
        if _tags is not UNSET:
            tags = []
            for tags_item_data in _tags:
                tags_item = TagDraft.from_dict(tags_item_data)

                tags.append(tags_item)

        _tools = d.pop("tools", UNSET)
        tools: list[ToolDraft] | Unset = UNSET
        if _tools is not UNSET:
            tools = []
            for tools_item_data in _tools:
                tools_item = ToolDraft.from_dict(tools_item_data)

                tools.append(tools_item)

        def _parse_rating(data: object) -> float | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        rating = _parse_rating(d.pop("rating", UNSET))

        def _parse_org_url(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        org_url = _parse_org_url(d.pop("orgURL", UNSET))

        def _parse_date_added(data: object) -> datetime.date | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_added_type_0 = datetime.date.fromisoformat(data)

                return date_added_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.date | None | Unset, data)

        date_added = _parse_date_added(d.pop("dateAdded", UNSET))

        def _parse_date_updated(data: object) -> datetime.datetime | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_updated_type_0 = datetime.datetime.fromisoformat(data)

                return date_updated_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None | Unset, data)

        date_updated = _parse_date_updated(d.pop("dateUpdated", UNSET))

        def _parse_created_at(data: object) -> datetime.datetime | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = datetime.datetime.fromisoformat(data)

                return created_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("createdAt", UNSET))

        def _parse_update_at(data: object) -> datetime.datetime | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                update_at_type_0 = datetime.datetime.fromisoformat(data)

                return update_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None | Unset, data)

        update_at = _parse_update_at(d.pop("update_at", UNSET))

        _recipe_ingredient = d.pop("recipeIngredient", UNSET)
        recipe_ingredient: list[RecipeIngredient] | Unset = UNSET
        if _recipe_ingredient is not UNSET:
            recipe_ingredient = []
            for recipe_ingredient_item_data in _recipe_ingredient:
                recipe_ingredient_item = RecipeIngredient.from_dict(recipe_ingredient_item_data)

                recipe_ingredient.append(recipe_ingredient_item)

        _recipe_instructions = d.pop("recipeInstructions", UNSET)
        recipe_instructions: list[RecipeStep] | Unset = UNSET
        if _recipe_instructions is not UNSET:
            recipe_instructions = []
            for recipe_instructions_item_data in _recipe_instructions:
                recipe_instructions_item = RecipeStep.from_dict(recipe_instructions_item_data)

                recipe_instructions.append(recipe_instructions_item)

        def _parse_nutrition(data: object) -> Nutrition | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                nutrition_type_0 = Nutrition.from_dict(data)

                return nutrition_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | Nutrition | Unset, data)

        nutrition = _parse_nutrition(d.pop("nutrition", UNSET))

        def _parse_settings(data: object) -> RecipeSettings | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                settings_type_0 = RecipeSettings.from_dict(data)

                return settings_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(None | RecipeSettings | Unset, data)

        settings = _parse_settings(d.pop("settings", UNSET))

        _assets = d.pop("assets", UNSET)
        assets: list[RecipeAsset] | Unset = UNSET
        if _assets is not UNSET:
            assets = []
            for assets_item_data in _assets:
                assets_item = RecipeAsset.from_dict(assets_item_data)

                assets.append(assets_item)

        _notes = d.pop("notes", UNSET)
        notes: list[RecipeNote] | Unset = UNSET
        if _notes is not UNSET:
            notes = []
            for notes_item_data in _notes:
                notes_item = RecipeNote.from_dict(notes_item_data)

                notes.append(notes_item)

        _extras = d.pop("extras", UNSET)
        extras: RecipeDraftExtras | Unset
        if isinstance(_extras, Unset):
            extras = UNSET
        else:
            extras = RecipeDraftExtras.from_dict(_extras)

        _comments = d.pop("comments", UNSET)
        comments: list[RecipeCommentOut] | Unset = UNSET
        if _comments is not UNSET:
            comments = []
            for comments_item_data in _comments:
                comments_item = RecipeCommentOut.from_dict(comments_item_data)

                comments.append(comments_item)

        recipe_draft = cls(
            id=id,
            user_id=user_id,
            household_id=household_id,
            group_id=group_id,
            name=name,
            slug=slug,
            image=image,
            recipe_servings=recipe_servings,
            recipe_yield_quantity=recipe_yield_quantity,
            recipe_yield=recipe_yield,
            total_time=total_time,
            prep_time=prep_time,
            perform_time=perform_time,
            total_time_seconds=total_time_seconds,
            prep_time_seconds=prep_time_seconds,
            perform_time_seconds=perform_time_seconds,
            description=description,
            recipe_category=recipe_category,
            tags=tags,
            tools=tools,
            rating=rating,
            org_url=org_url,
            date_added=date_added,
            date_updated=date_updated,
            created_at=created_at,
            update_at=update_at,
            recipe_ingredient=recipe_ingredient,
            recipe_instructions=recipe_instructions,
            nutrition=nutrition,
            settings=settings,
            assets=assets,
            notes=notes,
            extras=extras,
            comments=comments,
        )

        recipe_draft.additional_properties = d
        return recipe_draft

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
