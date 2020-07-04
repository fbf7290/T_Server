import hmac, hashlib
import requests
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd


host = 'https://api-testnet.bybit.com'


def get_signature(req_params):
    val = '&'.join(
        [str(k) + "=" + str(v) for k, v in sorted(req_params.items()) if (k != 'sign') and (v is not None)])
    return str(hmac.new(bytes(API_KEY, "utf-8"), bytes(val, "utf-8"), digestmod="sha256").hexdigest()), val


def get_server_time():
    path = "/v2/public/time?"
    # expires = self.get_http_expires()
    # req_params = {"api_key":self.api_key, "timestamp":expires}
    req_params = {"api_key":API_KEY}
    sign, query = get_signature(req_params)


    url = host+path+query+"&sign="+sign
    r = requests.get(url, timeout=5.0)
    return r.json()



def get_http_expires():
    return int(float(get_server_time()['time_now']) * 1000)

def get_kline(coin, interval, from_time, limit=100):
    #path = "/v2/public/kline/list/{}?".format(coin)
    path = "/v2/public/kline/list?"
    expires = get_http_expires()
    req_params = {"api_key": API_KEY, "symbol":coin, "from": from_time, "limit":limit, "interval":interval,  "timestamp": expires}
    sign, query = get_signature(req_params)

    url = host + path + query + "&sign=" + sign
    r = requests.get(url, timeout=5.0)
    return r.json()


# coin에 대해서 from_time 부터 limit 개 interval 봉 가져옴
# https://bybit-exchange.github.io/bybit-official-api-docs/en/index.html#operation/query_kline 참고
data = get_kline("BTCUSD", "5", int((datetime.datetime.now() - relativedelta(minutes=1000)).timestamp()), 200)['result']
pd.DataFrame(data).to_excel("data.xlsx")