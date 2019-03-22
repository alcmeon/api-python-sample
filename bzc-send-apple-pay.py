#!/usr/bin/python3
import argparse
import uuid
import requests
import hashlib

ALCMEON_PAYMENT_GATEWAY_URL = "https://demo.alcmeon.com/bzc/paymentService"

def _get_merchant_session(args):
    payload = {
        "merchantIdentifier": hashlib.sha256(args.merchant_id.encode('utf-8')).hexdigest(),
        "displayName": args.merchant_name,
        "initiative": "messaging",
        "initiativeContext": ALCMEON_PAYMENT_GATEWAY_URL 
    }

    response = requests.post('https://apple-pay-gateway.apple.com/paymentservices/paymentSession', 
        json=payload, 
        cert=args.merchant_certificate
    )
    response.raise_for_status()
    return response.json()


def send_apple_pay(args):
    session = _get_merchant_session(args)

    request_id = str(uuid.uuid4())
    message_id = str(uuid.uuid4())

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
            "receivedMessage": {"title": "Tote bag"},
            "bid": "com.apple.messages.MSMessageExtensionBalloonPlugin:0000000000:com.apple.icloud.apps.messages.business.extension",
            "data": {
                "requestIdentifier": request_id,
                "mspVersion": "1.0",
                "payment": {
                    "paymentRequest": {
                        "lineItems": [{
                                "label": "Tote bag",
                                "amount": "10.00",
                                "type": "final"
                        }],
                        "total": {
                            "label": "Your Total",
                            "amount": "10.00",
                            "type": "final"
                        },
                        "applePay": {
                            "merchantIdentifier": args.merchant_id,
                            "supportedNetworks": ["visa"],
                            "merchantCapabilities": ["supportsDebit"]
                        },
                        "merchantName": args.merchant_name,
                        "countryCode": "FR",
                        "currencyCode": "EUR",
                        "requiredBillingContactFields": [],
                        "requiredShippingContactFields": []
                    },
                    "merchantSession": session,
                    "endpoints": {
                        "paymentGatewayUrl": ALCMEON_PAYMENT_GATEWAY_URL
                    }
                }
            }
        }
    }
    url = "https://api.alcmeon.com/bzc/message"

    response = requests.post(url, auth=(args.company_id, args.secret), headers=headers, json=payload)
    print (response.status_code, response.text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--company-id', required=True)
    parser.add_argument('--secret', required=True)
    parser.add_argument('--business-id', required=True)
    parser.add_argument('--destination-id', required=True)
    parser.add_argument('--merchant-id', required=True)
    parser.add_argument('--merchant-name', required=True)
    parser.add_argument('--merchant-certificate', required=True)
    args = parser.parse_args()

    send_apple_pay(args)

