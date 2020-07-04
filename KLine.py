import threading
import Bybit
import time
import datetime
from dateutil.relativedelta import relativedelta

class KLine(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.btcusd = {"1":None, "5":None, "30":None, "60":None}
        self.ethusd = {"1":None, "5":None, "30":None, "60":None}
        self.xrpusd = {"1":None, "5":None, "30":None, "60":None}
        self.eosusd = {"1":None, "5":None, "30":None, "60":None}
        self.bybit = Bybit.Bybit(True)

    def cal_average(self, coin, interval, from_time):
        value = 0
        datas = self.bybit.get_kline(coin, interval, int((datetime.datetime.now() - relativedelta(minutes=from_time)).timestamp()))['result']
        for data in datas:
            value += float(data['close'])
        value = value / len(datas)
        return value

    def get_data(self):
        return {"btcusd":self.btcusd, "ethusd":self.ethusd, "xrpusd":self.xrpusd, "eosusd":self.eosusd}


    def run(self):
        while True:
            self.btcusd["1"] = self.cal_average("BTCUSD", "D", 43200)
            time.sleep(2)
            self.btcusd["5"] = self.cal_average("BTCUSD", "5", 150)
            time.sleep(2)
            self.btcusd["30"] = self.cal_average("BTCUSD", "30", 900)
            time.sleep(2)
            self.btcusd["60"] = self.cal_average("BTCUSD", "60", 1800)
            time.sleep(2)

            self.ethusd["1"] = self.cal_average("ETHUSD", "D", 43200)
            time.sleep(2)
            self.ethusd["5"] = self.cal_average("ETHUSD", "5", 150)
            time.sleep(2)
            self.ethusd["30"] = self.cal_average("ETHUSD", "30", 900)
            time.sleep(2)
            self.ethusd["60"] = self.cal_average("ETHUSD", "60", 1800)
            time.sleep(2)


            self.xrpusd["1"] = self.cal_average("XRPUSD", "D", 43200)
            time.sleep(2)
            self.xrpusd["5"] = self.cal_average("XRPUSD", "5", 150)
            time.sleep(2)
            self.xrpusd["30"] = self.cal_average("XRPUSD", "30", 900)
            time.sleep(2)
            self.xrpusd["60"] = self.cal_average("XRPUSD", "60", 1800)
            time.sleep(2)


            self.eosusd["1"] = self.cal_average("EOSUSD", "D", 43200)
            time.sleep(2)
            self.eosusd["5"] = self.cal_average("EOSUSD", "5", 150)
            time.sleep(2)
            self.eosusd["30"] = self.cal_average("EOSUSD", "30", 900)
            time.sleep(2)
            self.eosusd["60"] = self.cal_average("EOSUSD", "60", 1800)
            time.sleep(2)

            time.sleep(20)


if __name__ == "__main__":
    kline = KLine()
    kline.start()


