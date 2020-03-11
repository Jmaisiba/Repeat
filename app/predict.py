from os.path import join, dirname, realpath
from sklearn.externals import joblib
import pandas as pd

MODEL_PATH = join(dirname(realpath(__file__)), 'models/xgboostv1.joblib')
#MODEL_PATH = './models/xgboostv1.joblib'

model = joblib.load(MODEL_PATH)

def predict(new_customer):
	"""
        new_customer should be a python dict

        education: {0: 'College/University', 1: 'Masters/Phd', 2: 'None', 3: 'Primary', 4: 'Secondary'} 
        employment: {0: 'Employed', 1: 'Self employed', 2: 'Student', 3: 'Student,Employed', 4: 'Student,Self employed', 5: 'Student,Unemployed', 6: 'Unemployed'} 
        marital: {0: 'married', 1: 'single'} 
        dependants:{0: '1', 1: '2 - 5', 2: 'None', 3: 'more than 5'}

        example customer
        {
            'avg_airtime_spent': 3.625,
            'avg_bundles_balance': 10776.0,
            'avg_incoming_calls_duration': 5.0, 
            'avg_mobile_money_amount': 7.0,
            'avg_mobile_money_balance': 4028.0,
            'avg_mobile_money_received_amount': 2028.0,
            'avg_mobile_money_sent_amount': 1028.0,
            'avg_outgoing_calls_duration': 5.0,
            'avg_received_bank_amount': 800.0,
            'avg_sent_bank_amount': 500.0,
            'has_another_loan': True,
            'has_bank_account': True, 
            'has_mobile_banking': True,
            'no_of_apps': 50,
            'no_received_mobile_money_transactions': 200,
            'no_sent_mobile_money_transactions': 150,
            'number_of_contacts': 2000,
            'number_of_incoming_calls': 5046,
            'number_of_missed_calls': 1400,
            'number_of_outgoing_calls': 4001,
            'number_of_rejected_calls': 100,
            'unique_call_contacts': 300,
            'unique_mobile_money_contacts': 350,
            'education': 1,
            'employment': 0,
            'marital': 1, 
            'dependants': 1
        }

        output
        {
            defaulter: True #customer will default
            probability: 82.20% #confidence level
        }

    """
    new_customer_data = pd.DataFrame(new_customer, index=[0])
    customer_class = model.predict(new_customer_data)
    customer_class_probability = model.predict_proba(new_customer_data)

    if customer_class[0] == 1:
        return {
                'defaulter': True,
                'probability': "%.2f%%" %(customer_class_probability.tolist()[0][0] * 100.0)
            }
    else:
        return {
                'defaulter': False,
                'probability': "%.2f%%" %(customer_class_probability.tolist()[0][0] * 100.0)
            }
