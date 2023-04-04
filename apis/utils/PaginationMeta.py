from rest_framework.pagination import PageNumberPagination
from apis.database_models.login_master import login_master
from apis.database_models.lookup_state import lookup_state
from apis.database_service.client_account_details_service import client_account_details_by_merchant_id
from apis.database_service.merchant_data_service import get_merchant_address_by_id
from apis.database_models.merchant_data import merchant_data
from ..serializers.merchant_serializer import merchant_data_serializer
from apis.database_models.verification import Verification


class PaginationMeta(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 10000


def get_custom_merchant_response(data):
    for i, merchant in enumerate(data, start=1):
        merchant_list = list(merchant.values())
        login_id = merchant_list[24]
        try:
            login = login_master.objects.get(loginMasterId=login_id)
            is_direct = "online" if login.isDirect else "offline"
            created_date = login.createdDate
        except Exception as e:
            is_direct = None
            created_date = None
        try:
            merchant_id = merchant_data.objects.get(loginMasterId=login_id).merchantId
            account_details = client_account_details_by_merchant_id(merchant_id)
            account_type = account_details.accountType
            branch = account_details.branch
        except Exception as e:
            account_type = None
            branch = None
        try:
            address = get_merchant_address_by_id(login_id)
            state_name = lookup_state.objects.get(stateId=address.state).stateName
        except Exception as e:
            state_name = None
        try:
            get_merchant_data = merchant_data.objects.filter(loginMasterId=login_id).values()[0]
            get_merchant_data['merchant_status'] = get_merchant_data.pop('status')
            merchant.update(get_merchant_data)
        except Exception as e:
            merchant.update({"MerchantData": None})
        merchant.update({"accountType": account_type})
        merchant.update({"branch": branch})
        merchant.update({"state_name": state_name})
        merchant.update({"isDirect": is_direct})
        merchant.update({"signUpDate": created_date})
        merchant.update({"sno": i})
    return data


def get_custom_offline_merchant_response(merchant_record):
    login_id_of_merchant = [record.loginMasterId for record in merchant_record]
    login_data = login_master.objects.filter(loginMasterId__in=login_id_of_merchant, isDirect=False)
    login_dict = {login.loginMasterId: login for login in login_data}
    matching_logins = []
    i = 1
    for merchant_info in merchant_record:
        if merchant_info.loginMasterId in login_dict:
            login_record = login_dict[merchant_info.loginMasterId]
            merchant_record_data = merchant_data_serializer(merchant_info).data
            is_direct = "online" if login_record.isDirect else "offline"
            merchant_record_data['isDirect'] = is_direct
            merchant_record_data['sno'] = i
            matching_logins.append(merchant_record_data)
            i += 1
    return matching_logins


def get_response_of_key_value_pair(data):
    for i, merchant in enumerate(data, start=1):
        merchant_list = list(merchant.values())
        login_id = merchant_list[25]
        try:
            login = login_master.objects.get(loginMasterId=login_id)
            is_direct = "online" if login.isDirect else "offline"
            created_date = login.createdDate
        except Exception as e:
            is_direct = None
            created_date = None
        try:
            merchant_id = merchant_data.objects.get(loginMasterId=login_id).merchantId
            account_details = client_account_details_by_merchant_id(merchant_id)
            account_type = account_details.accountType
            branch = account_details.branch
        except Exception as e:
            account_type = None
            branch = None
        try:
            address = get_merchant_address_by_id(login_id)
            state_name = lookup_state.objects.get(stateId=address.state).stateName
        except Exception as e:
            state_name = None
        try:
            get_verification_data = Verification.objects.filter(login_id=login_id).values()[0]
            get_verification_data['verification_status'] = get_verification_data.pop('status')
            merchant.update(get_verification_data)
        except Exception as e:
            merchant.update({"VerificationData": None})
        merchant.update({"accountType": account_type})
        merchant.update({"branch": branch})
        merchant.update({"state_name": state_name})
        merchant.update({"isDirect": is_direct})
        merchant.update({"signUpDate": created_date})
        merchant.update({"sno": i})
    return data
