#!/usr/bin/python3
import argparse
import uuid
import requests

def _encrypt(data):
    import os
    from Crypto.Cipher import AES
    from Crypto.Util import Counter
    import base64

    key = os.urandom(32)

    encoded_key = b"00%s" % base64.b16encode(key)
    ctr = Counter.new(128, initial_value=0)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    encrypted = cipher.encrypt(data)
    return encrypted, encoded_key

def _pre_upload(args, nencrypted):
    headers = {
        "Source-Id": args.business_id,
        "MMCS-Size": str(nencrypted)
    }
    url = "https://api.alcmeon.com/bzc/preUpload"
    response = requests.get(url, headers = headers, auth = (args.company_id, args.secret))
    return response.json()

def _upload(args, pre_upload, encrypted):
    response = requests.post(pre_upload['upload-url'], data = encrypted)
    return response.json()

def _send(args, key, nencrypted, pre_upload, uploaded):
    message_id = str(uuid.uuid4())
    headers = {
        "id": message_id,
        "Source-Id": args.business_id,
        "Destination-Id": args.destination_id
    }
    payload = {
        "id": message_id,
        "type": "text",
        "sourceId": args.business_id,
        "destinationId": args.destination_id,
        "v": 1,
        "body": u"before \uFFFC after",
        "attachments": [{
            "name": 'filename.png',
            "mimeType": 'image/png',
            "size": nencrypted,
            "signature-base64": uploaded['singleFile']['fileChecksum'],
            "url": pre_upload['mmcs-url'],
            "owner": pre_upload['mmcs-owner'],
            "key": key
        }]
    }
    url = "https://api.alcmeon.com/bzc/message"
    response = requests.post(url, headers = headers, json = payload, auth = (args.company_id, args.secret))
    return response


def send_attachment(args):
    with open(args.png, 'rb') as f:
        data = f.read()
    encrypted, key = _encrypt(data)

    pre = _pre_upload(args, len(encrypted))

    uploaded = _upload(args, pre, encrypted)
    print('send')
    response = _send(args, key, len(encrypted), pre, uploaded)
    print(response.status_code, response.text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--company-id', required=True)
    parser.add_argument('--secret', required=True)
    parser.add_argument('--business-id', required=True)
    parser.add_argument('--destination-id', required=True)
    parser.add_argument('--png', required=True, default=None)
    args = parser.parse_args()

    send_attachment(args)


