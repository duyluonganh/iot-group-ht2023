# -*- coding: utf-8 -*-
#!/usr/bin/env python
# This is where to insert your generated API keys (http://api.telldus.com/keys)
pubkey = "" # Public Key
privkey = "" # Private Key
token = "" # Token
secret = "" # Token Secret
import requests, json, hashlib, uuid, time
localtime = time.localtime(time.time())
timestamp = str(time.mktime(localtime))
nonce = uuid.uuid4().hex
oauthSignature = (privkey + "%26" + secret)

# GET-request
response = requests.get(
        url="https://pa-api.telldus.com/json/sensor/info",
        params={
                "id": "1547943570",
        },
        headers={
                "Authorization": 'OAuth oauth_consumer_key="{pubkey}", oauth_nonce="{nonce}", oauth_signature="{oauthSignature}", oauth_signature_method="PLAINTEXT", oauth_timestamp="{timestamp}", oauth_token="{token}", oauth_version="1.0"'.format(pubkey=pubkey, nonce=nonce, oauthSignature=oauthSignature, timestamp=timestamp, token=token),
                },
        )
# Output/response from GET-request
responseData = response.json()
print(responseData)