import hmac, hashlib
import requests
import time
from Global import *
import websocket
import threading
import json
import datetime



# {'data': [{'trailing_stop': '0', 'stop_loss': '0', 'timestamp': '2019-12-07T12:51:00.888Z', 'cum_exec_qty': 0, 'time_in_force': 'GoodTillCancel', 'last_exec_price': '0', 'cum_exec_fee': '0', 'take_profit': '0', 'order_link_id': '', 'leaves_qty': 1, 'price': '7539.5', 'symbol': 'BTCUSD', 'side': 'Buy', 'cum_exec_value': '0', 'qty': 1, 'order_status': 'New', 'order_type': 'Limit', 'order_id': 'fd0f48ee-c40c-475a-ab1e-6c48a9d950fa'}], 'topic': 'order'}
# {'data': [{'trailing_stop': '0', 'stop_loss': '0', 'timestamp': '2019-12-07T12:51:23.704Z', 'cum_exec_qty': 0, 'time_in_force': 'GoodTillCancel', 'last_exec_price': '0', 'cum_exec_fee': '0', 'take_profit': '0', 'order_link_id': '', 'leaves_qty': 0, 'price': '7539.5', 'symbol': 'BTCUSD', 'side': 'Buy', 'cum_exec_value': '0', 'qty': 1, 'order_status': 'Cancelled', 'order_type': 'Limit', 'order_id': 'fd0f48ee-c40c-475a-ab1e-6c48a9d950fa'}], 'topic': 'order'}
# {'data': [{'trailing_stop': '0', 'stop_loss': '0', 'timestamp': '2019-12-07T12:51:51.403Z', 'cum_exec_qty': 1, 'time_in_force': 'ImmediateOrCancel', 'last_exec_price': '7551.5', 'cum_exec_fee': '0.0000001', 'take_profit': '0', 'order_link_id': '', 'leaves_qty': 0, 'price': '7549', 'symbol': 'BTCUSD', 'side': 'Buy', 'cum_exec_value': '0.00013242', 'qty': 1, 'order_status': 'Filled', 'order_type': 'Market', 'order_id': '39964743-13c6-4caf-9fe6-387d68257297'}], 'topic': 'order'}
# {'data': [{'trailing_stop': '0', 'stop_loss': '0', 'timestamp': '2019-12-07T12:52:38.546Z', 'cum_exec_qty': 0, 'time_in_force': 'GoodTillCancel', 'last_exec_price': '0', 'cum_exec_fee': '0', 'take_profit': '0', 'order_link_id': '', 'leaves_qty': 1, 'price': '7551.5', 'symbol': 'BTCUSD', 'side': 'Sell', 'cum_exec_value': '0', 'qty': 1, 'order_status': 'New', 'order_type': 'Limit', 'order_id': 'e9f8fad8-0313-42ed-b455-2500c37513a9'}], 'topic': 'order'}
# {'data': [{'trailing_stop': '0', 'stop_loss': '0', 'timestamp': '2019-12-07T12:54:07.936Z', 'cum_exec_qty': 1, 'time_in_force': 'GoodTillCancel', 'last_exec_price': '7551.5', 'cum_exec_fee': '-0.00000003', 'take_profit': '0', 'order_link_id': '', 'leaves_qty': 0, 'price': '7551.5', 'symbol': 'BTCUSD', 'side': 'Sell', 'cum_exec_value': '0.00013242', 'qty': 1, 'order_status': 'Filled', 'order_type': 'Limit', 'order_id': 'e9f8fad8-0313-42ed-b455-2500c37513a9'}], 'topic': 'order'}
# {'data': [{'trailing_stop': '0', 'stop_loss': '0', 'timestamp': '2019-12-07T13:05:34.725Z', 'cum_exec_qty': 1, 'time_in_force': 'GoodTillCancel', 'last_exec_price': '7521.5', 'cum_exec_fee': '0.0000001', 'take_profit': '0', 'order_link_id': '', 'leaves_qty': 0, 'price': '7521.5', 'symbol': 'BTCUSD', 'side': 'Buy', 'cum_exec_value': '0.00013295', 'qty': 1, 'order_status': 'Filled', 'order_type': 'Limit', 'order_id': 'f785c58a-afd3-4bf3-8f77-947fc32d5cdd'}], 'topic': 'order'}




class Bybit():

    GET = "GET"
    POST = "POST"

    def __init__(self, test=False):


        self.api_key  = "46XJlDj69eYnzdFEJw"
        self.api_secret = "RIo33DYyJyZBye4YNiPCsntIgKhxhjGq1KeT"
        self.auth = False

        self.BTCUSD_PRICE = 0

        if test:
            self.host = 'https://api-testnet.bybit.com'
            self.websocket_host = 'wss://stream-testnet.bybit.com/realtime'
        else:
            self.host = 'https://api.bybit.com'
            self.websocket_host = 'wss://stream.bybit.com/realtime'


    def get_signature(self, req_params):
        val = '&'.join(
            [str(k) + "=" + str(v) for k, v in sorted(req_params.items()) if (k != 'sign') and (v is not None)])
        return str(hmac.new(bytes(self.api_secret, "utf-8"), bytes(val, "utf-8"), digestmod="sha256").hexdigest()), val


    def get_http_expires(self):
        return int(float(self.get_server_time()['time_now'])*1000)


    def get_server_time(self):
        path = "/v2/public/time?"
        # expires = self.get_http_expires()
        # req_params = {"api_key":self.api_key, "timestamp":expires}
        req_params = {"api_key":self.api_key}
        sign, query = self.get_signature(req_params)


        url = self.host+path+query+"&sign="+sign
        r = requests.get(url, timeout=5.0)
        return r.json()


    def get_api_key(self):
        path = "/open-api/api-key?"
        expires = self.get_http_expires()
        req_params = {"api_key":self.api_key, "timestamp":expires}
        sign, query = self.get_signature(req_params)


        url = self.host+path+query+"&sign="+sign
        r = requests.get(url, timeout=5.0)
        return r.json()


    # 코인 n봉 가격 불러오기
    # coin : BTCUSD, ETHUSD, XRPUSD, EOSUSD
    def get_kline(self, coin, interval, from_time, limit=100):
        #path = "/v2/public/kline/list/{}?".format(coin)
        path = "/v2/public/kline/list?"
        expires = self.get_http_expires()
        req_params = {"api_key": self.api_key, "symbol":coin, "from": from_time, "limit":limit, "interval":interval,  "timestamp": expires}
        sign, query = self.get_signature(req_params)

        url = self.host + path + query + "&sign=" + sign
        r = requests.get(url, timeout=5.0)
        return r.json()




if __name__ == "__main__":
    from PyQt5.QtWidgets import  QApplication
    import sys

    app = QApplication(sys.argv)
    bit = Bybit(True)
    print(datetime.datetime.now().timestamp())
    from dateutil.relativedelta import relativedelta
    print(bit.get_kline("BTCUSD", "D", int((datetime.datetime.now()-relativedelta(minutes=43200)).timestamp())))

    te = bit.get_kline("BTCUSD", "D", int((datetime.datetime.now()-relativedelta(minutes=43200)).timestamp()), 100)['result']
    print(len(te))

    #app.exec_()
