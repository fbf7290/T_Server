import threading
import Bybit
import time
import datetime
from dateutil.relativedelta import relativedelta

class EMA21(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.btcusd_ema_g = {"30":None, "15":None}
        self.ethusd_ema_g = {"30":None, "15":None}
        self.xrpusd_ema_g = {"30":None, "15":None}
        self.eosusd_ema_g = {"30":None, "15":None}

        self.alarm = {"BTCUSD": {"30M-EMA21":None, "15M-EMA21":None},
                      "ETHUSD": {"30M-EMA21":None, "15M-EMA21":None},
                      "XRPUSD": {"30M-EMA21":None, "15M-EMA21":None},
                      "EOSUSD": {"30M-EMA21":None, "15M-EMA21":None}}

        self.bybit = Bybit.Bybit(True)

        self.n = 21
        self.k = 2 / (self.n + 1)

    def cal_ema(self, data):
        ema_list = []
        i = 0
        g_list = []

        while True:
            sub_data = data[i:i + self.n]
            if len(sub_data) != self.n:
                break

            ema = float(sub_data[0]['close'])
            for p in sub_data[1:]:
                ema = float(p['close']) * self.k + ema * (1 - self.k)
            ema_list.append((sub_data[-1]['open_time'], ema))
            i += 1

        for i in range(len(ema_list[:-1])):
            g_list.append((ema_list[i + 1][0], ema_list[i + 1][1] - ema_list[i][1]))
        return g_list

    def get_alarm_data(self):
        data = []

        for coin, alarm in self.alarm.items():
            for t, d in alarm.items():
                if d == None:
                    continue
                data.append({"kind":coin, "data":{"index":t, "event":"Inflection-Point"}, "timestamp":d})

        return data

    def get_ema_g(self):
        return {"BTCUSD":self.btcusd_ema_g, "ETHUSD":self.ethusd_ema_g, "XRPUSD":self.xrpusd_ema_g, "EOSUSD":self.eosusd_ema_g}

    def main_func(self, ema_time, alarm_key):
        g_list = self.cal_ema(self.bybit.get_kline("BTCUSD", ema_time, int((datetime.datetime.now() - relativedelta(minutes=1320)).timestamp()), 200)['result'])
        self.btcusd_ema_g[ema_time] = g_list
        if g_list[-2][1] * g_list[-1][1] < 0:
            self.alarm["BTCUSD"][alarm_key] = g_list[-1][0]
        else:
            self.alarm["BTCUSD"][alarm_key] = None
        time.sleep(1)

        g_list = self.cal_ema(self.bybit.get_kline("ETHUSD", ema_time, int((datetime.datetime.now() - relativedelta(minutes=1320)).timestamp()), 200)['result'])
        self.ethusd_ema_g[ema_time] = g_list
        if g_list[-2][1] * g_list[-1][1] < 0:
            self.alarm["ETHUSD"][alarm_key] = datetime.datetime.now().timestamp()
        else:
            self.alarm["ETHUSD"][alarm_key] = None
        time.sleep(1)

        g_list = self.cal_ema(self.bybit.get_kline("XRPUSD", ema_time, int((datetime.datetime.now() - relativedelta(minutes=1320)).timestamp()), 200)['result'])
        self.xrpusd_ema_g[ema_time] = g_list
        if g_list[-2][1] * g_list[-1][1] < 0:
            self.alarm["XRPUSD"][alarm_key] = datetime.datetime.now().timestamp()
        else:
            self.alarm["XRPUSD"][alarm_key] = None
        time.sleep(1)

        g_list = self.cal_ema(self.bybit.get_kline("EOSUSD", ema_time, int((datetime.datetime.now() - relativedelta(minutes=1320)).timestamp()), 200)['result'])
        self.eosusd_ema_g[ema_time] = g_list
        if g_list[-2][1] * g_list[-1][1] < 0:
            self.alarm["EOSUSD"][alarm_key] = datetime.datetime.now().timestamp()
        else:
            self.alarm["EOSUSD"][alarm_key] = None
        time.sleep(1)


    def run(self):
        while True:
            self.main_func("30", "30M-EMA21")
            self.main_func("15", "15M-EMA21")

            print(self.btcusd_ema_g)

            time.sleep(60)


if __name__ == "__main__":
    kline = EMA21()
    kline.start()


