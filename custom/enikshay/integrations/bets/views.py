"""
https://docs.google.com/document/d/1RPPc7t9NhRjOOiedlRmtCt3wQSjAnWaj69v2g7QRzS0/edit
"""
import datetime
import json

from dateutil import parser as date_parser
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from dimagi.utils.logging import notify_exception
from dimagi.utils.web import json_response
from dimagi.ext import jsonobject
from jsonobject.exceptions import BadValueError

from corehq import toggles
from corehq.apps.domain.decorators import login_or_digest_or_basic_or_apikey
from corehq.apps.hqcase.utils import bulk_update_cases
from corehq.apps.repeaters.views import AddCaseRepeaterView
from corehq.form_processor.exceptions import CaseNotFound
from corehq.form_processor.interfaces.dbaccessors import CaseAccessors


from custom.enikshay.case_utils import CASE_TYPE_VOUCHER, CASE_TYPE_EPISODE
from .const import BETS_EVENT_IDS


class ApiError(Exception):
    def __init__(self, msg, status_code):
        self.status_code = status_code
        super(ApiError, self).__init__(msg)


class FlexibleDateTimeProperty(jsonobject.DateTimeProperty):
    def _wrap(self, value):
        try:
            return date_parser.parse(value)
        except ValueError:
            return super(FlexibleDateTimeProperty, self)._wrap(value)


class PaymentUpdate(jsonobject.JsonObject):
    id = jsonobject.StringProperty(required=True)
    status = jsonobject.StringProperty(required=True, choices=['Success', 'Failure'])
    amount = jsonobject.DecimalProperty(required=False)
    payment_date = FlexibleDateTimeProperty(required=True)

    # TODO save these properties
    remarks = jsonobject.StringProperty(required=False)
    payment_mode = jsonobject.StringProperty(required=False)
    check_number = jsonobject.StringProperty(required=False)
    bank_name = jsonobject.StringProperty(required=False)

    @property
    def case_id(self):
        return self.id


class VoucherUpdate(PaymentUpdate):
    event_type = jsonobject.StringProperty(required=True, choices=['Voucher'])
    case_type = CASE_TYPE_VOUCHER

    @property
    def properties(self):
        if self.status == 'Success':
            return {
                'state': 'paid',
                'amount_fulfilled': self.amount,
                'date_fulfilled': self.payment_date,
            }
        else:
            return {
                'state': 'rejected',
                'reason_rejected': self.remarks,
                'date_rejected': self.payment_date,
            }


class IncentiveUpdate(PaymentUpdate):
    event_type = jsonobject.StringProperty(required=True, choices=['Incentive'])
    bets_parent_event_id = jsonobject.StringProperty(
        required=False, choices=BETS_EVENT_IDS)
    case_type = CASE_TYPE_EPISODE

    @property
    def properties(self):
        status_key = 'tb_incentive_{}_status'.format(self.bets_parent_event_id)
        if self.status == 'Success':
            amount_key = 'tb_incentive_{}_amount'.format(self.bets_parent_event_id)
            date_key = 'tb_incentive_{}_payment_date'.format(self.bets_parent_event_id)
            return {
                status_key: 'paid',
                amount_key: self.amount,
                date_key: self.payment_date,
            }
        else:
            date_key = 'tb_incentive_{}_rejection_date'.format(self.bets_parent_event_id)
            reason_key = 'tb_incentive_{}_rejection_reason'.format(self.bets_parent_event_id)
            return {
                status_key: 'rejected',
                date_key: self.payment_date,
                reason_key: self.remarks,
            }


def get_case(domain, case_id):
    case_accessor = CaseAccessors(domain)
    return case_accessor.get_case(case_id)


def _get_case_updates(request, domain):
    try:
        request_json = json.loads(request.body)
    except ValueError:
        raise ApiError(msg="Malformed JSON", status_code=400)

    if not isinstance(request_json.get('response', None), list):
        raise ApiError(msg='Expected json of the form `{"response": []}`', status_code=400)

    updates = []
    for event_json in request_json['response']:
        if event_json.get('event_type', None) not in ('Voucher', 'Incentive'):
            raise ApiError(msg="Malformed JSON", status_code=400)

        update_model = VoucherUpdate if event_json['event_type'] == 'Voucher' else IncentiveUpdate
        try:
            update = update_model.wrap(event_json)
        except BadValueError as e:
            raise ApiError(msg=e.message, status_code=400)
        try:
            # TODO move this to bulk?
            case = get_case(domain, update.case_id)
            if case.type != update.case_type:
                raise CaseNotFound()
        except CaseNotFound:
            raise ApiError(
                msg="No {} case found with that ID".format(update.case_type),
                status_code=404
            )
        updates.append(update)
    return updates


@require_POST
@csrf_exempt
@login_or_digest_or_basic_or_apikey()
@toggles.ENIKSHAY_API.required_decorator()
def payment_confirmation(request, domain):
    try:
        updates = _get_case_updates(request, domain)
    except ApiError as e:
        if not settings.UNIT_TESTING:
            notify_exception(request, "BETS sent the eNikshay API a bad request.")
        return json_response({"error": e.message}, status_code=e.status_code)

    bulk_update_cases(domain, [
        (update.case_id, update.properties, False)
        for update in updates
    ])
    return json_response({'status': "success"})


class ChemistBETSVoucherRepeaterView(AddCaseRepeaterView):
    urlname = 'chemist_bets_voucher_repeater'
    page_title = "BETS Chemist Vouchers"
    page_name = "BETS Chemist Vouchers (voucher case type)"


class LabBETSVoucherRepeaterView(AddCaseRepeaterView):
    urlname = 'lab_bets_voucher_repeater'
    page_title = "BETS Lab Vouchers"
    page_name = "BETS Lab Vouchers (voucher case type)"


class BETS180TreatmentRepeaterView(AddCaseRepeaterView):
    urlname = "bets_180_treatment_repeater"
    page_title = "MBBS+ Providers: 6 months (180 days) of private OR govt. FDCs with treatment outcome reported"
    page_name = "MBBS+ Providers: 6 months (180 days) of private OR govt. " \
                "FDCs with treatment outcome reported (episode case type)"


class BETSDrugRefillRepeaterView(AddCaseRepeaterView):
    urlname = "bets_drug_refill_repeater"
    page_title = "Patients: Cash transfer on subsequent drug refill"
    page_name = "Patients: Cash transfer on subsequent drug refill (episode case_type)"


class BETSSuccessfulTreatmentRepeaterView(AddCaseRepeaterView):
    urlname = "bets_successful_treatment_repeater"
    page_title = "Patients: Cash transfer on successful treatment completion"
    page_name = "Patients: Cash transfer on successful treatment completion (episode case type)"


class BETSDiagnosisAndNotificationRepeaterView(AddCaseRepeaterView):
    urlname = "bets_diagnosis_and_notification_repeater"
    page_title = "MBBS+ Providers: To provider for diagnosis and notification of TB case"
    page_name = "MBBS+ Providers: To provider for diagnosis and notification of TB case (episode case type)"


class BETSAYUSHReferralRepeaterView(AddCaseRepeaterView):
    urlname = "bets_ayush_referral_repeater"
    page_title = "AYUSH/Other provider: Registering and referral of a presumptive TB case in UATBC/e-Nikshay"
    page_name = "AYUSH/Other provider: Registering and referral of a presumptive TB " \
                "case in UATBC/e-Nikshay (episode case type)"
