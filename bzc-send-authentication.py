#!/usr/bin/python3
import argparse
import uuid
import requests

def send_authentication(args):
    message_id = str(uuid.uuid4())
    request_id = str(uuid.uuid4())

    headers = {
        "id": message_id,
        "Source-Id": args.business_id,
        "Destination-Id": args.destination_id
    }

    payload = {
        "sourceId": args.business_id,
        "destinationId": args.destination_id,
        "v": 1,
        "id": message_id,
        "type": "interactive",
        "interactiveData": {
            "bid": "com.apple.messages.MSMessageExtensionBalloonPlugin:0000000000:com.apple.icloud.apps.messages.business.extension",
            "data": {
                "version": "1.0",
                "requestIdentifier": request_id,
                "authenticate": {
                    "oauth2": {
                        "responseType": "code",
                        "scope": ["email", "profile"],
                        "state": "security_token",
                        "responseEncryptionKey": "BFz948MTG3OQ0Q69JHUiBG7dZ3SMGU1s2bVG9HuyX/hEU4H0pQJUjm/j93uqyVOBM8+i0AlgDvPOZ+UJzy6YGmU=",
                        "clientSecret": "YourClientSecret"
                    }
                },
            },
            "receivedMessage": {
                "title": "Alcmeon Demo",
            }
        }
    }

    url = "https://api.alcmeon.com/bzc/authenticate"
    response = requests.post(url, auth=(args.company_id, args.secret), headers=headers, json=payload)
    print(response.status_code, response.text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--company-id', required=True)
    parser.add_argument('--secret', required=True)
    parser.add_argument('--business-id', required=True)
    parser.add_argument('--destination-id', required=True)
    args = parser.parse_args()

    send_authentication(args)

