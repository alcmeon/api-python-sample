#!/usr/bin/python3
import argparse
import uuid
import requests

def send_time_picker(args):
    message_id = str(uuid.uuid4())
    request_id = str(uuid.uuid4())
    headers = {
        "id": message_id,
        "Source-Id": args.business_id,
        "Destination-Id": args.destination_id
    }
    payload = {
        "v": 1,
        "type": "interactive",
        "id": message_id,
        "sourceId": args.business_id,
        "destinationId": args.destination_id,
        "interactiveData": {
            "bid": "com.apple.messages.MSMessageExtensionBalloonPlugin:0000000000:com.apple.icloud.apps.messages.business.extension",
            "data": {
                "mspVersion": "1.0",
                "requestIdentifier": request_id,
                "event": {
                    "identifier": "1",
                    "title": "",
                    "timeslots": [
                        {
                            "duration": 3600,
                            "startTime": "2023-04-03T9:00+0000",
                            "identifier": "0"
                        },
                        {
                            "duration": 3600,
                            "startTime": "2023-04-03T19:00+0000",
                            "identifier": "1"
                        },
                    ]
                }
            },
            "receivedMessage": {"title" : "Please, choose a slot"}
        }
    }

    url = "https://api.alcmeon.com/bzc/message"

    response = requests.post(url, auth=(args.company_id, args.secret), headers=headers, json=payload)
    print(response.status_code, response.text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--company-id', required=True)
    parser.add_argument('--secret', required=True)
    parser.add_argument('--business-id', required=True)
    parser.add_argument('--destination-id', required=True)
    args = parser.parse_args()

    send_time_picker(args)

