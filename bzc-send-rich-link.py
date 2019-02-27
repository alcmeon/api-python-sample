import argparse
import uuid
import requests
import bzc
import base64

def send_rich_link(args, png):
    message_id = str(uuid.uuid4())
    headers = {
        "id": message_id,
        "Source-Id": args.business_id,
        "Destination-Id": args.destination_id
    }
    payload = {
        "richLinkData": {
            "url": "https://www.alcmeon.com/",
            "title": "Alcmeon",
            "assets": {
                "image": {
                    "data": base64.b64encode(png),
                    "mimeType": "image/png"
                }
            }
        },
        "sourceId": args.business_id,
        "destinationId": args.destination_id,
        "v": 1,
        "id": message_id,
        "type": "richLink"
    }

    response = requests.post(bzc.alcmeon_url(args, '/message'), auth=(args.company_id, args.secret), headers=headers, json=payload)
    response.raise_for_status()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--company-id', required=True)
    parser.add_argument('--secret', required=True)
    parser.add_argument('--business-id', required=True)
    parser.add_argument('--destination-id', required=True)
    parser.add_argument('--png', required=True)
    args = parser.parse_args()

    with open(args.png) as f:
        png = f.read()

    send_rich_link(args, png)

