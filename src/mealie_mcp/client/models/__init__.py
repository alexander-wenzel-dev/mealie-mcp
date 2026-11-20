"""Contains all the data models used in inputs/outputs"""

from .admin_about_info import AdminAboutInfo
from .ai_prompt_mode import AIPromptMode
from .ai_prompt_out import AIPromptOut
from .ai_prompt_override_update import AIPromptOverrideUpdate
from .ai_prompts_out import AIPromptsOut
from .ai_provider_create import AIProviderCreate
from .ai_provider_create_requestheaders import AIProviderCreateRequestheaders
from .ai_provider_create_requestparams import AIProviderCreateRequestparams
from .ai_provider_out import AIProviderOut
from .ai_provider_out_requestheaders import AIProviderOutRequestheaders
from .ai_provider_out_requestparams import AIProviderOutRequestparams
from .ai_provider_settings_out import AIProviderSettingsOut
from .ai_provider_settings_update import AIProviderSettingsUpdate
from .ai_provider_summary import AIProviderSummary
from .ai_provider_test_result import AIProviderTestResult
from .ai_provider_update import AIProviderUpdate
from .ai_provider_update_requestheaders import AIProviderUpdateRequestheaders
from .ai_provider_update_requestparams import AIProviderUpdateRequestparams
from .all_backups import AllBackups
from .app_info import AppInfo
from .app_startup_info import AppStartupInfo
from .app_statistics import AppStatistics
from .app_theme import AppTheme
from .assign_categories import AssignCategories
from .assign_settings import AssignSettings
from .assign_tags import AssignTags
from .auth_method import AuthMethod
from .backup_file import BackupFile
from .body_create_recipe_from_zip_api_recipes_create_zip_post import (
    BodyCreateRecipeFromZipApiRecipesCreateZipPost,
)
from .body_create_recipe_with_ai_api_recipes_create_ai_post import (
    BodyCreateRecipeWithAiApiRecipesCreateAiPost,
)
from .body_create_recipe_with_ai_stream_api_recipes_create_ai_stream_post import (
    BodyCreateRecipeWithAiStreamApiRecipesCreateAiStreamPost,
)
from .body_debug_openai_api_admin_debug_openai_provider_id_post import (
    BodyDebugOpenaiApiAdminDebugOpenaiProviderIdPost,
)
from .body_get_token_api_auth_token_post import BodyGetTokenApiAuthTokenPost
from .body_start_data_migration_api_groups_migrations_post import (
    BodyStartDataMigrationApiGroupsMigrationsPost,
)
from .body_trigger_action_api_households_recipe_actions_item_id_trigger_recipe_slug_post import (
    BodyTriggerActionApiHouseholdsRecipeActionsItemIdTriggerRecipeSlugPost,
)
from .body_update_event_image_api_recipes_timeline_events_item_id_image_put import (
    BodyUpdateEventImageApiRecipesTimelineEventsItemIdImagePut,
)
from .body_update_recipe_image_api_recipes_slug_image_put import (
    BodyUpdateRecipeImageApiRecipesSlugImagePut,
)
from .body_update_user_image_api_users_id_image_post import BodyUpdateUserImageApiUsersIdImagePost
from .body_upload_one_api_admin_backups_upload_post import BodyUploadOneApiAdminBackupsUploadPost
from .body_upload_recipe_asset_api_recipes_slug_assets_post import (
    BodyUploadRecipeAssetApiRecipesSlugAssetsPost,
)
from .category_create import CategoryCreate
from .category_draft import CategoryDraft
from .category_out import CategoryOut
from .category_pagination import CategoryPagination
from .category_with_recipes import CategoryWithRecipes
from .change_password import ChangePassword
from .check_app_config import CheckAppConfig
from .cook_book_create import CookBookCreate
from .cook_book_out import CookBookOut
from .cook_book_pagination import CookBookPagination
from .cook_book_update import CookBookUpdate
from .cookbook_household import CookbookHousehold
from .debug_response import DebugResponse
from .delete_recipes import DeleteRecipes
from .delete_token_response import DeleteTokenResponse
from .email_invitation import EmailInvitation
from .email_invitation_response import EmailInvitationResponse
from .email_ready import EmailReady
from .email_success import EmailSuccess
from .email_test import EmailTest
from .export_recipes import ExportRecipes
from .export_types import ExportTypes
from .file_token_response import FileTokenResponse
from .forgot_password import ForgotPassword
from .format_response import FormatResponse
from .group_admin_update import GroupAdminUpdate
from .group_base import GroupBase
from .group_data_export import GroupDataExport
from .group_event_notifier_create import GroupEventNotifierCreate
from .group_event_notifier_options import GroupEventNotifierOptions
from .group_event_notifier_options_out import GroupEventNotifierOptionsOut
from .group_event_notifier_out import GroupEventNotifierOut
from .group_event_notifier_update import GroupEventNotifierUpdate
from .group_event_pagination import GroupEventPagination
from .group_household_summary import GroupHouseholdSummary
from .group_out import GroupOut
from .group_pagination import GroupPagination
from .group_preferences_out import GroupPreferencesOut
from .group_preferences_update import GroupPreferencesUpdate
from .group_recipe_action_create import GroupRecipeActionCreate
from .group_recipe_action_out import GroupRecipeActionOut
from .group_recipe_action_pagination import GroupRecipeActionPagination
from .group_recipe_action_save import GroupRecipeActionSave
from .group_recipe_action_type import GroupRecipeActionType
from .group_storage import GroupStorage
from .group_summary import GroupSummary
from .household_admin_update import HouseholdAdminUpdate
from .household_create import HouseholdCreate
from .household_out import HouseholdOut
from .household_pagination import HouseholdPagination
from .household_preferences_out import HouseholdPreferencesOut
from .household_preferences_update import HouseholdPreferencesUpdate
from .household_recipe_summary import HouseholdRecipeSummary
from .household_statistics import HouseholdStatistics
from .household_summary import HouseholdSummary
from .household_user_summary import HouseholdUserSummary
from .http_validation_error import HTTPValidationError
from .image_type import ImageType
from .ingredient_confidence import IngredientConfidence
from .ingredient_food_alias import IngredientFoodAlias
from .ingredient_food_alias_create import IngredientFoodAliasCreate
from .ingredient_food_create import IngredientFoodCreate
from .ingredient_food_create_extras_type_0 import IngredientFoodCreateExtrasType0
from .ingredient_food_merge import IngredientFoodMerge
from .ingredient_food_out import IngredientFoodOut
from .ingredient_food_out_extras_type_0 import IngredientFoodOutExtrasType0
from .ingredient_food_out_output import IngredientFoodOutOutput
from .ingredient_food_out_output_extras_type_0 import IngredientFoodOutOutputExtrasType0
from .ingredient_food_pagination import IngredientFoodPagination
from .ingredient_food_substitution import IngredientFoodSubstitution
from .ingredient_food_substitution_create import IngredientFoodSubstitutionCreate
from .ingredient_food_substitution_output import IngredientFoodSubstitutionOutput
from .ingredient_food_summary import IngredientFoodSummary
from .ingredient_food_summary_output import IngredientFoodSummaryOutput
from .ingredient_references import IngredientReferences
from .ingredient_request import IngredientRequest
from .ingredient_unit_alias import IngredientUnitAlias
from .ingredient_unit_alias_create import IngredientUnitAliasCreate
from .ingredient_unit_create import IngredientUnitCreate
from .ingredient_unit_create_extras_type_0 import IngredientUnitCreateExtrasType0
from .ingredient_unit_merge import IngredientUnitMerge
from .ingredient_unit_out import IngredientUnitOut
from .ingredient_unit_out_extras_type_0 import IngredientUnitOutExtrasType0
from .ingredient_unit_out_output import IngredientUnitOutOutput
from .ingredient_unit_out_output_extras_type_0 import IngredientUnitOutOutputExtrasType0
from .ingredient_unit_pagination import IngredientUnitPagination
from .ingredients_request import IngredientsRequest
from .invite_token_create import InviteTokenCreate
from .invite_token_out import InviteTokenOut
from .logical_operator import LogicalOperator
from .long_live_token_create_response import LongLiveTokenCreateResponse
from .long_live_token_in import LongLiveTokenIn
from .long_live_token_out import LongLiveTokenOut
from .long_live_token_out_output import LongLiveTokenOutOutput
from .maintenance_storage_details import MaintenanceStorageDetails
from .maintenance_summary import MaintenanceSummary
from .meal_plan_i_cal_token_out import MealPlanICalTokenOut
from .multi_purpose_label_create import MultiPurposeLabelCreate
from .multi_purpose_label_merge import MultiPurposeLabelMerge
from .multi_purpose_label_out import MultiPurposeLabelOut
from .multi_purpose_label_pagination import MultiPurposeLabelPagination
from .multi_purpose_label_summary import MultiPurposeLabelSummary
from .multi_purpose_label_summary_output import MultiPurposeLabelSummaryOutput
from .multi_purpose_label_update import MultiPurposeLabelUpdate
from .native_oidc_token_request import NativeOIDCTokenRequest
from .note_reference import NoteReference
from .nutrition import Nutrition
from .oidc_native_config import OIDCNativeConfig
from .order_by_null_position import OrderByNullPosition
from .order_direction import OrderDirection
from .organizer_merge import OrganizerMerge
from .pagination_base_category_out import PaginationBaseCategoryOut
from .pagination_base_cook_book_out import PaginationBaseCookBookOut
from .pagination_base_household_summary import PaginationBaseHouseholdSummary
from .pagination_base_ingredient_food_out import PaginationBaseIngredientFoodOut
from .pagination_base_recipe_summary import PaginationBaseRecipeSummary
from .pagination_base_tag_out import PaginationBaseTagOut
from .pagination_base_tool_out import PaginationBaseToolOut
from .pagination_base_user_out import PaginationBaseUserOut
from .pagination_base_user_summary import PaginationBaseUserSummary
from .parsed_ingredient import ParsedIngredient
from .password_reset_token import PasswordResetToken
from .plan_entry_create import PlanEntryCreate
from .plan_entry_out import PlanEntryOut
from .plan_entry_pagination import PlanEntryPagination
from .plan_entry_type import PlanEntryType
from .plan_entry_update import PlanEntryUpdate
from .plan_rules_create import PlanRulesCreate
from .plan_rules_day import PlanRulesDay
from .plan_rules_out import PlanRulesOut
from .plan_rules_pagination import PlanRulesPagination
from .plan_rules_type import PlanRulesType
from .query_filter_json import QueryFilterJSON
from .query_filter_json_part import QueryFilterJSONPart
from .random_plan_entry_create import RandomPlanEntryCreate
from .recipe_asset import RecipeAsset
from .recipe_comment_create import RecipeCommentCreate
from .recipe_comment_out import RecipeCommentOut
from .recipe_comment_out_output import RecipeCommentOutOutput
from .recipe_comment_pagination import RecipeCommentPagination
from .recipe_comment_update import RecipeCommentUpdate
from .recipe_comment_user import RecipeCommentUser
from .recipe_create import RecipeCreate
from .recipe_draft import RecipeDraft
from .recipe_draft_extras import RecipeDraftExtras
from .recipe_draft_output import RecipeDraftOutput
from .recipe_draft_output_extras import RecipeDraftOutputExtras
from .recipe_duplicate import RecipeDuplicate
from .recipe_ingredient import RecipeIngredient
from .recipe_ingredient_output import RecipeIngredientOutput
from .recipe_ingredient_substitution import RecipeIngredientSubstitution
from .recipe_ingredient_substitution_output import RecipeIngredientSubstitutionOutput
from .recipe_last_made import RecipeLastMade
from .recipe_note import RecipeNote
from .recipe_out import RecipeOut
from .recipe_out_extras import RecipeOutExtras
from .recipe_settings import RecipeSettings
from .recipe_share_token_create import RecipeShareTokenCreate
from .recipe_share_token_out import RecipeShareTokenOut
from .recipe_share_token_summary import RecipeShareTokenSummary
from .recipe_step import RecipeStep
from .recipe_suggestion_response import RecipeSuggestionResponse
from .recipe_suggestion_response_item import RecipeSuggestionResponseItem
from .recipe_suggestion_substituted_food import RecipeSuggestionSubstitutedFood
from .recipe_summary import RecipeSummary
from .recipe_timeline_event_in import RecipeTimelineEventIn
from .recipe_timeline_event_out import RecipeTimelineEventOut
from .recipe_timeline_event_pagination import RecipeTimelineEventPagination
from .recipe_timeline_event_update import RecipeTimelineEventUpdate
from .recipe_url_bulk_create import RecipeUrlBulkCreate
from .recipe_url_create import RecipeUrlCreate
from .registered_parser import RegisteredParser
from .relational_keyword import RelationalKeyword
from .relational_operator import RelationalOperator
from .report_category import ReportCategory
from .report_entry_out import ReportEntryOut
from .report_out import ReportOut
from .report_summary import ReportSummary
from .report_summary_status import ReportSummaryStatus
from .reset_password import ResetPassword
from .scrape_recipe import ScrapeRecipe
from .scrape_recipe_data import ScrapeRecipeData
from .scrape_recipe_test import ScrapeRecipeTest
from .seeder_config import SeederConfig
from .set_permissions import SetPermissions
from .shopping_list_add_recipe_params import ShoppingListAddRecipeParams
from .shopping_list_add_recipe_params_bulk import ShoppingListAddRecipeParamsBulk
from .shopping_list_create import ShoppingListCreate
from .shopping_list_create_extras_type_0 import ShoppingListCreateExtrasType0
from .shopping_list_item_create import ShoppingListItemCreate
from .shopping_list_item_create_extras_type_0 import ShoppingListItemCreateExtrasType0
from .shopping_list_item_out import ShoppingListItemOut
from .shopping_list_item_out_extras_type_0 import ShoppingListItemOutExtrasType0
from .shopping_list_item_out_output import ShoppingListItemOutOutput
from .shopping_list_item_out_output_extras_type_0 import ShoppingListItemOutOutputExtrasType0
from .shopping_list_item_pagination import ShoppingListItemPagination
from .shopping_list_item_recipe_ref_create import ShoppingListItemRecipeRefCreate
from .shopping_list_item_recipe_ref_out import ShoppingListItemRecipeRefOut
from .shopping_list_item_recipe_ref_out_output import ShoppingListItemRecipeRefOutOutput
from .shopping_list_item_recipe_ref_update import ShoppingListItemRecipeRefUpdate
from .shopping_list_item_update import ShoppingListItemUpdate
from .shopping_list_item_update_bulk import ShoppingListItemUpdateBulk
from .shopping_list_item_update_bulk_extras_type_0 import ShoppingListItemUpdateBulkExtrasType0
from .shopping_list_item_update_extras_type_0 import ShoppingListItemUpdateExtrasType0
from .shopping_list_items_collection_out import ShoppingListItemsCollectionOut
from .shopping_list_multi_purpose_label_out import ShoppingListMultiPurposeLabelOut
from .shopping_list_multi_purpose_label_update import ShoppingListMultiPurposeLabelUpdate
from .shopping_list_out import ShoppingListOut
from .shopping_list_out_extras_type_0 import ShoppingListOutExtrasType0
from .shopping_list_pagination import ShoppingListPagination
from .shopping_list_recipe_ref_out import ShoppingListRecipeRefOut
from .shopping_list_remove_recipe_params import ShoppingListRemoveRecipeParams
from .shopping_list_summary import ShoppingListSummary
from .shopping_list_summary_extras_type_0 import ShoppingListSummaryExtrasType0
from .shopping_list_update import ShoppingListUpdate
from .shopping_list_update_extras_type_0 import ShoppingListUpdateExtrasType0
from .success_response import SuccessResponse
from .supported_migrations import SupportedMigrations
from .tag_create import TagCreate
from .tag_draft import TagDraft
from .tag_out import TagOut
from .tag_pagination import TagPagination
from .tag_with_recipes import TagWithRecipes
from .timeline_event_image import TimelineEventImage
from .timeline_event_type import TimelineEventType
from .tool_create import ToolCreate
from .tool_draft import ToolDraft
from .tool_out import ToolOut
from .tool_pagination import ToolPagination
from .tool_with_recipes import ToolWithRecipes
from .unlock_results import UnlockResults
from .update_image_response import UpdateImageResponse
from .user_base import UserBase
from .user_in import UserIn
from .user_out import UserOut
from .user_out_output import UserOutOutput
from .user_pagination import UserPagination
from .user_rating_out import UserRatingOut
from .user_rating_summary import UserRatingSummary
from .user_rating_update import UserRatingUpdate
from .user_ratings_user_rating_out import UserRatingsUserRatingOut
from .user_ratings_user_rating_summary import UserRatingsUserRatingSummary
from .user_registration_create import UserRegistrationCreate
from .user_summary import UserSummary
from .validation_error import ValidationError
from .validation_error_context import ValidationErrorContext
from .webhook_create import WebhookCreate
from .webhook_out import WebhookOut
from .webhook_pagination import WebhookPagination
from .webhook_type import WebhookType

__all__ = (
    "AIPromptMode",
    "AIPromptOut",
    "AIPromptOverrideUpdate",
    "AIPromptsOut",
    "AIProviderCreate",
    "AIProviderCreateRequestheaders",
    "AIProviderCreateRequestparams",
    "AIProviderOut",
    "AIProviderOutRequestheaders",
    "AIProviderOutRequestparams",
    "AIProviderSettingsOut",
    "AIProviderSettingsUpdate",
    "AIProviderSummary",
    "AIProviderTestResult",
    "AIProviderUpdate",
    "AIProviderUpdateRequestheaders",
    "AIProviderUpdateRequestparams",
    "AdminAboutInfo",
    "AllBackups",
    "AppInfo",
    "AppStartupInfo",
    "AppStatistics",
    "AppTheme",
    "AssignCategories",
    "AssignSettings",
    "AssignTags",
    "AuthMethod",
    "BackupFile",
    "BodyCreateRecipeFromZipApiRecipesCreateZipPost",
    "BodyCreateRecipeWithAiApiRecipesCreateAiPost",
    "BodyCreateRecipeWithAiStreamApiRecipesCreateAiStreamPost",
    "BodyDebugOpenaiApiAdminDebugOpenaiProviderIdPost",
    "BodyGetTokenApiAuthTokenPost",
    "BodyStartDataMigrationApiGroupsMigrationsPost",
    "BodyTriggerActionApiHouseholdsRecipeActionsItemIdTriggerRecipeSlugPost",
    "BodyUpdateEventImageApiRecipesTimelineEventsItemIdImagePut",
    "BodyUpdateRecipeImageApiRecipesSlugImagePut",
    "BodyUpdateUserImageApiUsersIdImagePost",
    "BodyUploadOneApiAdminBackupsUploadPost",
    "BodyUploadRecipeAssetApiRecipesSlugAssetsPost",
    "CategoryCreate",
    "CategoryDraft",
    "CategoryOut",
    "CategoryPagination",
    "CategoryWithRecipes",
    "ChangePassword",
    "CheckAppConfig",
    "CookBookCreate",
    "CookBookOut",
    "CookBookPagination",
    "CookBookUpdate",
    "CookbookHousehold",
    "DebugResponse",
    "DeleteRecipes",
    "DeleteTokenResponse",
    "EmailInvitation",
    "EmailInvitationResponse",
    "EmailReady",
    "EmailSuccess",
    "EmailTest",
    "ExportRecipes",
    "ExportTypes",
    "FileTokenResponse",
    "ForgotPassword",
    "FormatResponse",
    "GroupAdminUpdate",
    "GroupBase",
    "GroupDataExport",
    "GroupEventNotifierCreate",
    "GroupEventNotifierOptions",
    "GroupEventNotifierOptionsOut",
    "GroupEventNotifierOut",
    "GroupEventNotifierUpdate",
    "GroupEventPagination",
    "GroupHouseholdSummary",
    "GroupOut",
    "GroupPagination",
    "GroupPreferencesOut",
    "GroupPreferencesUpdate",
    "GroupRecipeActionCreate",
    "GroupRecipeActionOut",
    "GroupRecipeActionPagination",
    "GroupRecipeActionSave",
    "GroupRecipeActionType",
    "GroupStorage",
    "GroupSummary",
    "HTTPValidationError",
    "HouseholdAdminUpdate",
    "HouseholdCreate",
    "HouseholdOut",
    "HouseholdPagination",
    "HouseholdPreferencesOut",
    "HouseholdPreferencesUpdate",
    "HouseholdRecipeSummary",
    "HouseholdStatistics",
    "HouseholdSummary",
    "HouseholdUserSummary",
    "ImageType",
    "IngredientConfidence",
    "IngredientFoodAlias",
    "IngredientFoodAliasCreate",
    "IngredientFoodCreate",
    "IngredientFoodCreateExtrasType0",
    "IngredientFoodMerge",
    "IngredientFoodOut",
    "IngredientFoodOutExtrasType0",
    "IngredientFoodOutOutput",
    "IngredientFoodOutOutputExtrasType0",
    "IngredientFoodPagination",
    "IngredientFoodSubstitution",
    "IngredientFoodSubstitutionCreate",
    "IngredientFoodSubstitutionOutput",
    "IngredientFoodSummary",
    "IngredientFoodSummaryOutput",
    "IngredientReferences",
    "IngredientRequest",
    "IngredientUnitAlias",
    "IngredientUnitAliasCreate",
    "IngredientUnitCreate",
    "IngredientUnitCreateExtrasType0",
    "IngredientUnitMerge",
    "IngredientUnitOut",
    "IngredientUnitOutExtrasType0",
    "IngredientUnitOutOutput",
    "IngredientUnitOutOutputExtrasType0",
    "IngredientUnitPagination",
    "IngredientsRequest",
    "InviteTokenCreate",
    "InviteTokenOut",
    "LogicalOperator",
    "LongLiveTokenCreateResponse",
    "LongLiveTokenIn",
    "LongLiveTokenOut",
    "LongLiveTokenOutOutput",
    "MaintenanceStorageDetails",
    "MaintenanceSummary",
    "MealPlanICalTokenOut",
    "MultiPurposeLabelCreate",
    "MultiPurposeLabelMerge",
    "MultiPurposeLabelOut",
    "MultiPurposeLabelPagination",
    "MultiPurposeLabelSummary",
    "MultiPurposeLabelSummaryOutput",
    "MultiPurposeLabelUpdate",
    "NativeOIDCTokenRequest",
    "NoteReference",
    "Nutrition",
    "OIDCNativeConfig",
    "OrderByNullPosition",
    "OrderDirection",
    "OrganizerMerge",
    "PaginationBaseCategoryOut",
    "PaginationBaseCookBookOut",
    "PaginationBaseHouseholdSummary",
    "PaginationBaseIngredientFoodOut",
    "PaginationBaseRecipeSummary",
    "PaginationBaseTagOut",
    "PaginationBaseToolOut",
    "PaginationBaseUserOut",
    "PaginationBaseUserSummary",
    "ParsedIngredient",
    "PasswordResetToken",
    "PlanEntryCreate",
    "PlanEntryOut",
    "PlanEntryPagination",
    "PlanEntryType",
    "PlanEntryUpdate",
    "PlanRulesCreate",
    "PlanRulesDay",
    "PlanRulesOut",
    "PlanRulesPagination",
    "PlanRulesType",
    "QueryFilterJSON",
    "QueryFilterJSONPart",
    "RandomPlanEntryCreate",
    "RecipeAsset",
    "RecipeCommentCreate",
    "RecipeCommentOut",
    "RecipeCommentOutOutput",
    "RecipeCommentPagination",
    "RecipeCommentUpdate",
    "RecipeCommentUser",
    "RecipeCreate",
    "RecipeDraft",
    "RecipeDraftExtras",
    "RecipeDraftOutput",
    "RecipeDraftOutputExtras",
    "RecipeDuplicate",
    "RecipeIngredient",
    "RecipeIngredientOutput",
    "RecipeIngredientSubstitution",
    "RecipeIngredientSubstitutionOutput",
    "RecipeLastMade",
    "RecipeNote",
    "RecipeOut",
    "RecipeOutExtras",
    "RecipeSettings",
    "RecipeShareTokenCreate",
    "RecipeShareTokenOut",
    "RecipeShareTokenSummary",
    "RecipeStep",
    "RecipeSuggestionResponse",
    "RecipeSuggestionResponseItem",
    "RecipeSuggestionSubstitutedFood",
    "RecipeSummary",
    "RecipeTimelineEventIn",
    "RecipeTimelineEventOut",
    "RecipeTimelineEventPagination",
    "RecipeTimelineEventUpdate",
    "RecipeUrlBulkCreate",
    "RecipeUrlCreate",
    "RegisteredParser",
    "RelationalKeyword",
    "RelationalOperator",
    "ReportCategory",
    "ReportEntryOut",
    "ReportOut",
    "ReportSummary",
    "ReportSummaryStatus",
    "ResetPassword",
    "ScrapeRecipe",
    "ScrapeRecipeData",
    "ScrapeRecipeTest",
    "SeederConfig",
    "SetPermissions",
    "ShoppingListAddRecipeParams",
    "ShoppingListAddRecipeParamsBulk",
    "ShoppingListCreate",
    "ShoppingListCreateExtrasType0",
    "ShoppingListItemCreate",
    "ShoppingListItemCreateExtrasType0",
    "ShoppingListItemOut",
    "ShoppingListItemOutExtrasType0",
    "ShoppingListItemOutOutput",
    "ShoppingListItemOutOutputExtrasType0",
    "ShoppingListItemPagination",
    "ShoppingListItemRecipeRefCreate",
    "ShoppingListItemRecipeRefOut",
    "ShoppingListItemRecipeRefOutOutput",
    "ShoppingListItemRecipeRefUpdate",
    "ShoppingListItemUpdate",
    "ShoppingListItemUpdateBulk",
    "ShoppingListItemUpdateBulkExtrasType0",
    "ShoppingListItemUpdateExtrasType0",
    "ShoppingListItemsCollectionOut",
    "ShoppingListMultiPurposeLabelOut",
    "ShoppingListMultiPurposeLabelUpdate",
    "ShoppingListOut",
    "ShoppingListOutExtrasType0",
    "ShoppingListPagination",
    "ShoppingListRecipeRefOut",
    "ShoppingListRemoveRecipeParams",
    "ShoppingListSummary",
    "ShoppingListSummaryExtrasType0",
    "ShoppingListUpdate",
    "ShoppingListUpdateExtrasType0",
    "SuccessResponse",
    "SupportedMigrations",
    "TagCreate",
    "TagDraft",
    "TagOut",
    "TagPagination",
    "TagWithRecipes",
    "TimelineEventImage",
    "TimelineEventType",
    "ToolCreate",
    "ToolDraft",
    "ToolOut",
    "ToolPagination",
    "ToolWithRecipes",
    "UnlockResults",
    "UpdateImageResponse",
    "UserBase",
    "UserIn",
    "UserOut",
    "UserOutOutput",
    "UserPagination",
    "UserRatingOut",
    "UserRatingSummary",
    "UserRatingUpdate",
    "UserRatingsUserRatingOut",
    "UserRatingsUserRatingSummary",
    "UserRegistrationCreate",
    "UserSummary",
    "ValidationError",
    "ValidationErrorContext",
    "WebhookCreate",
    "WebhookOut",
    "WebhookPagination",
    "WebhookType",
)
