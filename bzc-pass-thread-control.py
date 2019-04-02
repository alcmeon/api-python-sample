#!/usr/bin/python3
import argparse
import requests

def send_pass_thread_control(args):
    headers = {
        "Source-Id": args.business_id,
    }
    payload = {
        'recipient_id' : args.recipient_id,
        'new_owner_app_id' : 'primary',
        'metadata' : args.metadata
    }
    url = "https://api.alcmeon.com/bzc/pass-thread-control"

    response = requests.post(url, auth=(args.company_id, args.secret), headers=headers, json=payload)
    print(response.status_code, response.text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--company-id', required=True)
    parser.add_argument('--secret', required=True)
    parser.add_argument('--business-id', required=True)
    parser.add_argument('--recipient-id', required=True)
    parser.add_argument('--metadata', default=None)
    args = parser.parse_args()

    send_pass_thread_control()
