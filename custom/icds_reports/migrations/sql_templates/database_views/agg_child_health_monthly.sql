DROP VIEW IF EXISTS agg_child_health_monthly CASCADE;
CREATE VIEW agg_child_health_monthly AS
    SELECT
        "awc_location_months"."awc_id" AS "awc_id",
        "awc_location_months"."awc_name" AS "awc_name",
        "awc_location_months"."awc_site_code" AS "awc_site_code",
        "awc_location_months"."supervisor_id" AS "supervisor_id",
        "awc_location_months"."supervisor_name" AS "supervisor_name",
        "awc_location_months"."supervisor_site_code" AS "supervisor_site_code",
        "awc_location_months"."block_id" AS "block_id",
        "awc_location_months"."block_name" AS "block_name",
        "awc_location_months"."block_site_code" AS "block_site_code",
        "awc_location_months"."district_id" AS "district_id",
        "awc_location_months"."district_name" AS "district_name",
        "awc_location_months"."district_site_code" AS "district_site_code",
        "awc_location_months"."state_id" AS "state_id",
        "awc_location_months"."state_name" AS "state_name",
        "awc_location_months"."state_site_code" AS "state_site_code",
        "awc_location_months"."block_map_location_name" AS "block_map_location_name",
        "awc_location_months"."district_map_location_name" AS "district_map_location_name",
        "awc_location_months"."state_map_location_name" AS "state_map_location_name",
        "awc_location_months"."aggregation_level" AS "aggregation_level",
        "awc_location_months"."month" AS "month",
        "awc_location_months"."month_display" AS "month_display",
        "awc_location_months"."contact_phone_number" AS "contact_phone_number",
        "agg_child_health"."gender" AS "gender",
        "agg_child_health"."age_tranche" AS "age_tranche",
        "agg_child_health"."caste" AS "caste",
        "agg_child_health"."disabled" AS "disabled",
        "agg_child_health"."minority" AS "minority",
        "agg_child_health"."resident" AS "resident",
        COALESCE("agg_child_health"."valid_in_month", 0) AS "valid_in_month",
        COALESCE("agg_child_health"."valid_all_registered_in_month", 0) AS "valid_all_registered_in_month",
        COALESCE("agg_child_health"."nutrition_status_weighed", 0) AS "nutrition_status_weighed",
        COALESCE("agg_child_health"."nutrition_status_unweighed", 0) AS "nutrition_status_unweighed",
        COALESCE("agg_child_health"."nutrition_status_normal", 0) AS "nutrition_status_normal",
        COALESCE("agg_child_health"."nutrition_status_moderately_underweight", 0) AS "nutrition_status_moderately_underweight",
        COALESCE("agg_child_health"."nutrition_status_severely_underweight", 0) AS "nutrition_status_severely_underweight",
        COALESCE("agg_child_health"."wer_eligible", 0) AS "wer_eligible",
        COALESCE("agg_child_health"."height_measured_in_month", 0) AS "height_measured_in_month",
        COALESCE("agg_child_health"."height_eligible", 0) AS "height_eligible",
        COALESCE("agg_child_health"."wasting_moderate", 0) AS "wasting_moderate",
        COALESCE("agg_child_health"."wasting_severe", 0) AS "wasting_severe",
        COALESCE("agg_child_health"."wasting_normal", 0) AS "wasting_normal",
        COALESCE("agg_child_health"."wasting_moderate_v2", 0) AS "wasting_moderate_v2",
        COALESCE("agg_child_health"."wasting_severe_v2", 0) AS "wasting_severe_v2",
        COALESCE("agg_child_health"."wasting_normal_v2", 0) AS "wasting_normal_v2",
        COALESCE("agg_child_health"."stunting_moderate", 0) AS "stunting_moderate",
        COALESCE("agg_child_health"."stunting_severe", 0) AS "stunting_severe",
        COALESCE("agg_child_health"."stunting_normal", 0) AS "stunting_normal",
        COALESCE("agg_child_health"."zscore_grading_hfa_moderate", 0) AS "zscore_grading_hfa_moderate",
        COALESCE("agg_child_health"."zscore_grading_hfa_severe", 0) AS "zscore_grading_hfa_severe",
        COALESCE("agg_child_health"."zscore_grading_hfa_normal", 0) AS "zscore_grading_hfa_normal",
        COALESCE("agg_child_health"."pnc_eligible", 0) AS "pnc_eligible",
        COALESCE("agg_child_health"."thr_eligible", 0) AS "thr_eligible",
        COALESCE("agg_child_health"."rations_21_plus_distributed", 0) AS "rations_21_plus_distributed",
        COALESCE("agg_child_health"."pse_eligible", 0) AS "pse_eligible",
        COALESCE("agg_child_health"."pse_attended_16_days", 0) AS "pse_attended_16_days",
        COALESCE("agg_child_health"."born_in_month", 0) AS "born_in_month",
        COALESCE("agg_child_health"."low_birth_weight_in_month", 0) AS "low_birth_weight_in_month",
        COALESCE("agg_child_health"."bf_at_birth", 0) AS "bf_at_birth",
        COALESCE("agg_child_health"."ebf_eligible", 0) AS "ebf_eligible",
        COALESCE("agg_child_health"."ebf_in_month", 0) AS "ebf_in_month",
        COALESCE("agg_child_health"."ebf_no_info_recorded", 0) AS "ebf_no_info_recorded",
        COALESCE("agg_child_health"."cf_initiation_in_month", 0) AS "cf_initiation_in_month",
        COALESCE("agg_child_health"."cf_initiation_eligible", 0) AS "cf_initiation_eligible",
        COALESCE("agg_child_health"."cf_eligible", 0) AS "cf_eligible",
        COALESCE("agg_child_health"."cf_in_month", 0) AS "cf_in_month",
        COALESCE("agg_child_health"."cf_diet_diversity", 0) AS "cf_diet_diversity",
        COALESCE("agg_child_health"."cf_diet_quantity", 0) AS "cf_diet_quantity",
        COALESCE("agg_child_health"."cf_demo", 0) AS "cf_demo",
        COALESCE("agg_child_health"."cf_handwashing", 0) AS "cf_handwashing",
        COALESCE("agg_child_health"."counsel_increase_food_bf", 0) AS "counsel_increase_food_bf",
        COALESCE("agg_child_health"."counsel_manage_breast_problems", 0) AS "counsel_manage_breast_problems",
        COALESCE("agg_child_health"."counsel_ebf", 0) AS "counsel_ebf",
        COALESCE("agg_child_health"."counsel_adequate_bf", 0) AS "counsel_adequate_bf",
        COALESCE("agg_child_health"."counsel_pediatric_ifa", 0) AS "counsel_pediatric_ifa",
        COALESCE("agg_child_health"."counsel_play_cf_video", 0) AS "counsel_play_cf_video",
        COALESCE("agg_child_health"."fully_immunized_eligible", 0) AS "fully_immunized_eligible",
        COALESCE("agg_child_health"."fully_immunized_on_time", 0) AS "fully_immunized_on_time",
        COALESCE("agg_child_health"."fully_immunized_late", 0) AS "fully_immunized_late",
        COALESCE("agg_child_health"."weighed_and_height_measured_in_month", 0) AS "weighed_and_height_measured_in_month",
        COALESCE("agg_child_health"."weighed_and_born_in_month", 0) AS "weighed_and_born_in_month",
        "agg_child_health"."days_ration_given_child" AS "days_ration_given_child",
        COALESCE("agg_child_health"."zscore_grading_hfa_recorded_in_month", 0) AS "zscore_grading_hfa_recorded_in_month",
        COALESCE("agg_child_health"."zscore_grading_wfh_recorded_in_month", 0) AS "zscore_grading_wfh_recorded_in_month"
    FROM "public"."awc_location_months" "awc_location_months"
    LEFT JOIN "public"."agg_child_health" "agg_child_health" ON (
        ("awc_location_months"."month" = "agg_child_health"."month") AND
        ("awc_location_months"."aggregation_level" = "agg_child_health"."aggregation_level") AND
        ("awc_location_months"."state_id" = "agg_child_health"."state_id") AND
        ("awc_location_months"."district_id" = "agg_child_health"."district_id") AND
        ("awc_location_months"."block_id" = "agg_child_health"."block_id") AND
        ("awc_location_months"."supervisor_id" = "agg_child_health"."supervisor_id") AND
        ("awc_location_months"."awc_id" = "agg_child_health"."awc_id")
    );
