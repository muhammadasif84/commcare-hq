hqDefine("data_interfaces/js/case_rule_main", [
    'jquery',
    'data_interfaces/js/case_rule_criteria',
    'data_interfaces/js/case_rule_actions',
    'data_interfaces/js/make_read_only',
], function (
    $,
    caseRuleCriteria,
    caseRuleActions
) {

    $(function () {
        $("#rule-definition-form").submit(function () {
            var result = true;
            var criteria_model = caseRuleCriteria.get_criteria_model();

            if (criteria_model.selected_case_filter_id() !== 'select-one') {
                criteria_model.show_add_filter_warning(true);
                result = false;
            } else {
                criteria_model.show_add_filter_warning(false);
            }

            var actions_model = caseRuleActions.get_actions_model();
            if (actions_model.selected_case_action_id() !== 'select-one') {
                actions_model.show_add_action_warning(true);
                result = false;
            } else {
                actions_model.show_add_action_warning(false);
            }

            return result;
        });
    });

});
