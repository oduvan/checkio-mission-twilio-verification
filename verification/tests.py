"""
TESTS is a dict with all of your tests.
Keys for this will be the categories' names.
Each test is a dict with
    "input" -- input data for a user function
    "answer" -- your right answer
    "explanation" -- not necessarily a key, it's used for an additional info in animation.
"""


init_code = """
if not "send_token" in USER_GLOBAL:
    raise NotImplementedError("Where is 'send_token'?")
if not "check_token" in USER_GLOBAL:
    raise NotImplementedError("Where is 'check_token'?")
send_token = USER_GLOBAL['send_token']
check_token = USER_GLOBAL['check_token']
"""

run_test = """
import twilio
from twilio.rest.verify.v2.service.verification import VerificationInstance
from twilio.rest.verify.v2.service.verification_check import VerificationCheckInstance
from unittest import mock

with mock.patch('twilio.rest.verify.v2.service.verification.VerificationList.create'
) as mock_verification_create:    
    with mock.patch('twilio.rest.verify.v2.service.verification_check.VerificationCheckList.create'
    ) as mock_verification_check_create:
                
        def mock_verification_side_effect(*args, **kwargs):
            if kwargs.get('channel') != 'sms':
                raise ValueError('Wrong Channel')
            verification_payload = dict(
                status='pending',
                sid='your_sid',
                service_sid=mock_verification_create._solution['service_sid'],
                account_sid='your_account_sid',
                to=kwargs['to'],
                channel=kwargs['channel'],
                valid=False,
                amount=None,
                payee=None,
                date_created='2015-07-30T20:00:00Z',
                date_updated='2015-07-30T20:00:00Z',
                lookup=dict(carrier=dict(error_code=None,name="Carrier Name",mobile_country_code='310',mobile_network_code='150',type='mobile')),
                url='https://verify.twilio.com/v2/Services/VAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Verifications/VEXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'   
            )
            return VerificationInstance(
                mock_verification_create._version,
                verification_payload,
                service_sid=mock_verification_create._solution['service_sid'],
            )
        mock_verification_create.side_effect = mock_verification_side_effect

        def mock_verification_check_side_effect(*args, **kwargs):
            verification_check_payload = dict(
                status='approved',
                sid='your_sid',
                service_sid=mock_verification_check_create._solution['service_sid'],
                account_sid='your_account_sid',
                to=kwargs['to'],
                channel='sms',
                valid=True,
                amount=None,
                payee=None,
                date_created='2015-07-30T20:00:00Z',
                date_updated='2015-07-30T20:00:00Z',   
            )
            return VerificationCheckInstance(
                mock_verification_check_create._version,
                verification_check_payload,
                service_sid=mock_verification_check_create._solution['service_sid'],
            )
        mock_verification_check_create.side_effect = mock_verification_check_side_effect
        
        RET['code_result'] = {}

        if not mock_verification_create.called and not mock_verification_check_create.called:
            raise ValueError('Expected twilio client to be used')
"""


def prepare_test(test, answer):
    return {
        "test_code": {"python-3": init_code + run_test.format(test)},
        "show": {"python-3": test},
        "answer": answer
    }


TESTS = {
    "1. Basics": [
        prepare_test("send_token('+15017122661', 'sms')", 'pending'),
        prepare_test("check_token('+15017122661', '123456')", 'approved'),
        prepare_test("send_token('+15017122661', 'email')", 'pending'),
    ],
}