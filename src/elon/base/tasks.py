import json
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

PLAY_MOBILE_LOGIN = getattr(settings, "PLAY_MOBILE_LOGIN")
PLAY_MOBILE_PASSWORD = getattr(settings, "PLAY_MOBILE_PASSWORD")
PLAY_MOBILE_ENDPOINT = getattr(settings, "PLAY_MOBILE_ENDPOINT")


def send_code(phone, code, id_message):
    headers = {'content-type': 'application/json'}
    data = {
        'messages': [
            {
                'recipient': phone, 'message-id': id_message,
                'sms': {
                    'originator': 'Tezelon',
                    'content': {
                        'text': code
                    }
                }
            }
        ]
    }

    try:
        r = requests.post(PLAY_MOBILE_ENDPOINT, data=json.dumps(data),  headers=headers, auth=HTTPBasicAuth(PLAY_MOBILE_LOGIN, PLAY_MOBILE_PASSWORD))
        content = r.content
        print(content)
    except Exception as e:
        print("sent error: ~ %s" % e)
        return 0


