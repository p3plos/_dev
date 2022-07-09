import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("/home/l3ns/_dev/Python3.10.5_pipenv/"
                               "SDK/Firebase_PUSH_notification/"
                               "test-push-a37d1-firebase-adminsdk-ev24f"
                               "-35619dd57d.json")
firebase_admin.initialize_app(cred)
