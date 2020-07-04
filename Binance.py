import hmac, hashlib
import requests
import time
from Global import *
import websocket
import threading
import json
import datetime

class Binance():

    def __init__(self):



        self.api_key = "CpnfCFe001boBo2QSF1ln2VUR3glPcXVaOz4qJNslHEn8rNmjn7EaQlhdOcCvzf6"
        self.api_secret = "tNgeKAgo8KSw8AL8eVoHslTXOor1g1kOC58ykCzqCz55l20sNi6iuegt96uT5wm5"

        self.host = "https://fapi.binance.com"


    def get_http_expires(self):
        # return int(float(self.get_server_time()['time_now'])*1000)
        path = "/fapi/v1/time"
        url = self.host + path

        result = requests.get(url)
        return result.json()['serverTime']


    def get_signature(self, req_params):
        val = '&'.join(
            [str(k) + "=" + str(v) for k, v in sorted(req_params.items()) if (k != 'sign') and (v is not None)])
        return str(hmac.new(bytes(self.api_secret, "utf-8"), bytes(val, "utf-8"), digestmod="sha256").hexdigest()), val


    # kline
    def get_kline(self, coin, interval, limit=30):
        path = "/fapi/v1/klines?"
        headers = {'Content-Type': 'application/json'}

        url = self.host + path + "symbol={}&interval={}&limit={}".format(coin, interval, limit)

        r = requests.get(url, headers=headers)
        return r.json()





if __name__ == "__main__":
    te = Binance()
    print(te.get_kline("BTCUSDT", "1m"))
    print(len(te.get_kline("BTCUSDT", "1m")))
    for a in te.get_kline("BTCUSDT", "1m"):
        print(a[4])

    # 1
    # m
    # 3
    # m
    # 5
    # m
    # 15
    # m
    # 30
    # m
    # 1
    # h
    # 2
    # h
    # 4
    # h
    # 6
    # h
    # 8
    # h
    # 12
    # h
    # 1dddasdssasdsad
    # d
    # 3
    # d
    # 1
    # w
    # 1
    # M