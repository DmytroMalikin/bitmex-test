import errno
import hashlib
import hmac
import json
import time
import urllib
from threading import Event, Thread

import websocket
from channels.generic.websocket import WebsocketConsumer

from bitmex_api.models import Account

BITMEX_URL = "wss://testnet.bitmex_api.com"
ENDPOINT = "/realtime"
METHOD = "GET"


def bitmex_signature(api_secret, verb, url, nonce, body=None):
    data = ''

    if body:
        data = json.dumps(body, separators=(',', ':'))

    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.path
    if parsed_url.query:
        path = path + '?' + parsed_url.query

    message = (verb + path + str(nonce) + data).encode('utf-8')
    print(f"Signing: {message}")

    signature = hmac.new(api_secret.encode('utf-8'), message, digestmod=hashlib.sha256).hexdigest()
    print(f"Signature: {signature}")

    return signature


class BitmexConsumer(WebsocketConsumer):
    ws_client = None
    account = None

    def bitmex_ws_receive(self):
        while self.event.is_set():
            try:
                message = self.ws_client.recv()
                proxy_data = json.loads(message)
                data = proxy_data.get('data')

                if proxy_data and data:
                    price = data[0].get('markPrice', None)
                    message = {
                        'timestamp': data[0]['timestamp'],
                        'account': self.account.name,
                        'symbol': data[0]['symbol'],
                        'price': price
                    }

                    print(message)
                    self.send(text_data=json.dumps(message))

            except json.decoder.JSONDecodeError:
                print("Couldn't decode JSON")

            except OSError as e:
                if e.errno == errno.EBADF:
                    pass

    def connect(self):
        try:
            account_name = self.scope['url_route']['kwargs']['uri']
            self.account = Account.objects.get(name=account_name)
            print('Connected to WS')
        except Account.DoesNotExist as e:
            print("Such account doesn't exist")
        else:
            self.accept()

    def disconnect(self, close_code):
        print('Disconnected from WS')

        self.event.clear()
        self.ws_client.close()

    def receive(self, text_data, **kwargs):
        data = json.loads(text_data)
        print(data)

        if data['action'] == 'subscribe':
            expires = int(time.time()) + 5

            signature = bitmex_signature(self.account.api_secret, METHOD, ENDPOINT, expires)
            self.ws_client = websocket.create_connection(f"{BITMEX_URL}{ENDPOINT}"
                                                         f"?api-expires={expires}"
                                                         f"&api-signature={signature}"
                                                         f"&api-key={self.account.api_key}")
            self.ws_client.send(json.dumps({"op": "subscribe", "args": "position"}))

            self.event = Event()
            self.event.set()
            Thread(target=self.bitmex_ws_receive, args=()).start()

        if data['action'] == 'unsubscribe':
            self.ws_client.send(json.dumps({"op": "unsubscribe", "args": "position"}))
            self.event.clear()
            self.ws_client.close()
