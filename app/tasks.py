from time import time
import requests
from logging import getLogger
import logging

from .predict import predict

##from .feature_extraction.feature_extraction import get_all_features

logger = getLogger(__name__)
logger.setLevel(logging.DEBUG)



def get_all_features(user_id, interval):

    """
        Categories:
            - CALL_LOGS
            - CONTACTS
            - DEVICE_STATUS
            - MESSAGES


            "avg_airtime_spent": 3.625,                     MESSAGES
            "avg_bundles_balance": 10776.0,                 MESSAGES
            "avg_incoming_calls_duration": 5.0,             CALL_LOGS
            "avg_mobile_money_amount": 7.0,                 MESSAGES
            "avg_mobile_money_balance": 4028.0,             MESSAGES
            "avg_mobile_money_received_amount": 2028.0,     MESSAGES
            "avg_mobile_money_sent_amount": 1028.0,         MESSAGES
            "avg_outgoing_calls_duration": 5.0,             CALL_LOGS
            "avg_received_bank_amount": 800.0,              MESSAGES
            "avg_sent_bank_amount": 500.0,                  MESSAGES
            "has_another_loan": true,                       MESSAGES
            "has_bank_account": true,                       MESSAGES
            "has_mobile_banking": true,                     MESSAGES
            "no_of_apps": 50,                               DEVICE_STATUS
            "no_received_mobile_money_transactions": 200,   MESSAGES
            "no_sent_mobile_money_transactions": 150,       MESSAGES
            "number_of_contacts": 2000,                     CONTACTS
            "number_of_incoming_calls": 5046,               CALL_LOGS
            "number_of_missed_calls": 1400,                 CALL_LOGS
            "number_of_outgoing_calls": 4001,               CALL_LOGS
            "number_of_rejected_calls": 100,                CALL_LOGS
            "unique_call_contacts": 300,                    CALL_LOGS
            "unique_mobile_money_contacts": 350,            MESSAGES
            "education": 1,                                 BIO_DATA
            "employment": 0,                                BIO_DATA
            "marital": 1,                                   BIO_DATA
            "dependants": 1                                 BIO_DATA
    """


def predict_customer(user_id, interval):
    """
        Accepts user_id, callback url, number of days

    """
    features = {}
    try:
        user_data = get_all_features(user_id, interval)

        #Check if an error was encountered while getting features
        if user_data[0]:
            user_data = user_data[1]
            #Features must be in the specified order
            features = {
                'avg_airtime_spent': user_data['avg_airtime_spent'],
                'avg_bundles_balance': user_data['avg_bundles_balance'],
                'avg_incoming_calls_duration': user_data['avg_incoming_calls_duration'],
                'avg_mobile_money_amount': user_data['avg_mobile_money_amount'],
                'avg_mobile_money_balance': user_data['avg_mobile_money_balance'],
                'avg_mobile_money_received_amount': user_data['avg_mobile_money_received_amount'],
                'avg_mobile_money_sent_amount': user_data['avg_mobile_money_sent_amount'],
                'avg_outgoing_calls_duration': user_data['avg_outgoing_calls_duration'],
                'avg_received_bank_amount': user_data['avg_received_bank_amount'],
                'avg_sent_bank_amount': user_data['avg_sent_bank_amount'],
                'has_another_loan': user_data['has_another_loan'],
                'has_bank_account': user_data['has_bank_account'],
                'has_mobile_banking': user_data['has_mobile_banking'],
                'no_of_apps': user_data['no_of_apps'],
                'no_received_mobile_money_transactions': user_data['no_received_mobile_money_transactions'],
                'no_sent_mobile_money_transactions': user_data['no_sent_mobile_money_transactions'],
                'number_of_contacts': user_data['number_of_contacts'],
                'number_of_incoming_calls': user_data['number_of_incoming_calls'],
                'number_of_missed_calls': user_data['number_of_missed_calls'],
                'number_of_outgoing_calls': user_data['number_of_outgoing_calls'],
                'number_of_rejected_calls': user_data['number_of_rejected_calls'],
                'unique_call_contacts': user_data['unique_call_contacts'],
                'unique_mobile_money_contacts': user_data['unique_mobile_money_contacts'],
                'education': user_data['education'],
                'employment': user_data['employment'],
                'marital': user_data['marital'],
                'dependants': user_data['dependants']
            }
        else:
            return user_data

    
    # except Exception as exec:
    #     logger.exception(str(exec))
    #     return False, "An error occured while generating features for the user {}".format(user_id)

    try:
        prediction = predict(features)
        return True, prediction, features
    except Exception as exec:
        logger.exception(str(exec))
        return False, "Failed to score the user based on the features generated"

def predict_task(request_id, user_id, callback_url, interval):
    """
    """

    if callback_url is None:
        logging.warning("No callback_url found")
        return
    prediction = predict_customer(user_id, interval)

    if prediction[0]:
        result = {  
                    'request_id': request_id,
                    'status': 1,
                    'data': {
                        'parameters': prediction[2],
                        'result': prediction[1],
                    },
                    'timestamp': time()
                }
    else:
        result = ({
            'request_id': request_id,
            'status': -1,
            'error': prediction[1],
            'timestamp': time()
        })

    requests.post(callback_url, json=result)
