#!/usr/bin/python3
import argparse
import uuid
import requests

def send_typing(args):
    message_id = str(uuid.uuid4())
    headers = {
        "id": message_id,
        "Source-Id": args.business_id,
        "Destination-Id": args.destination_id
    }
    payload = {
        "body": "message %s" % message_id,
        "sourceId": args.business_id,
        "destinationId": args.destination_id,
        "v": 1,
        "type": "typing_%s" % args.typing,
        "id": message_id
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
    parser.add_argument('--typing', default='start')
    args = parser.parse_args()

    send_typing(args)


