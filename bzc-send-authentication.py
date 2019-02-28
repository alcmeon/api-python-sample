import argparse
import uuid
import requests

def send_text(args):
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
        "type": "text",
        "id": message_id
    }
    url = "https://bzc-proxy.alcmeon.com/bzc-proxy/api/1.0/companies/%s/message" % args.company_id

    response = requests.post(url, auth=(args.company_id, args.secret), headers=headers, json=payload)
    response.raise_for_status()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--company-id', required=True)
    parser.add_argument('--secret', required=True)
    parser.add_argument('--business-id', required=True)
    parser.add_argument('--destination-id', required=True)
    args = parser.parse_args()

    send_text(args)

