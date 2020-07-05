import threading
import Bybit
import time
import datetime
from dateutil.relativedelta import relativedelta

class EMA21(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.btcusd_ema_g = {"30":None}
        self.ethusd_ema_g = {"30":None}
        self.xrpusd_ema_g = {"30":None}
        self.eosusd_ema_g = {"30":None}

        self.alarm = {"BTCUSD": {"30M-EMA21":None},
                      "ETHUSD": {"30M-EMA21":None},
                      "XRPUSD": {"30M-EMA21":None},
                      "EOSUSD": {"30M-EMA21":None}}

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
            g_list.append((ema_list[i + 1][0], ema_list[i][1] / ema_list[i + 1][1]))
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

    def run(self):
        while True:
            g_list = self.cal_ema(self.bybit.get_kline("BTCUSD", "30", int((datetime.datetime.now() - relativedelta(minutes=1320)).timestamp()), 200)['result'])
            self.btcusd_ema_g["30"] = g_list
            if g_list[-2][1] * g_list[-1][1] < 0:
                self.alarm["BTCUSD"]["30M-EMA21"] = g_list[-1][0]
            else:
                self.alarm["BTCUSD"]["30M-EMA21"] = None
            time.sleep(1)

            g_list = self.cal_ema(self.bybit.get_kline("ETHUSD", "30", int((datetime.datetime.now() - relativedelta(minutes=1320)).timestamp()), 200)['result'])
            self.ethusd_ema_g["30"] = g_list
            if g_list[-2][1] * g_list[-1][1] < 0:
                self.alarm["ETHUSD"]["30M-EMA21"] = datetime.datetime.now().timestamp()
            else:
                self.alarm["ETHUSD"]["30M-EMA21"] = None
            time.sleep(1)

            g_list = self.cal_ema(self.bybit.get_kline("XRPUSD", "30", int((datetime.datetime.now() - relativedelta(minutes=1320)).timestamp()), 200)['result'])
            self.xrpusd_ema_g["30"] = g_list
            if g_list[-2][1] * g_list[-1][1] < 0:
                self.alarm["XRPUSD"]["30M-EMA21"] = datetime.datetime.now().timestamp()
            else:
                self.alarm["XRPUSD"]["30M-EMA21"] = None
            time.sleep(1)

            g_list = self.cal_ema(self.bybit.get_kline("EOSUSD", "30", int((datetime.datetime.now() - relativedelta(minutes=1320)).timestamp()), 200)['result'])
            self.eosusd_ema_g["30"] = g_list
            if g_list[-2][1] * g_list[-1][1] < 0:
                self.alarm["EOSUSD"]["30M-EMA21"] = datetime.datetime.now().timestamp()
            else:
                self.alarm["EOSUSD"]["30M-EMA21"] = None
            time.sleep(1)

            time.sleep(60)


if __name__ == "__main__":
    kline = EMA21()
    kline.start()


