import threading
import Binance
import time
import datetime
from dateutil.relativedelta import relativedelta

class KLine(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.BTCUSDT = {"1":None, "5":None, "30":None, "60":None}
        self.ETHUSDT = {"1":None, "5":None, "30":None, "60":None}
        self.BCHUSDT = {"1":None, "5":None, "30":None, "60":None}
        self.XRPUSDT = {"1":None, "5":None, "30":None, "60":None}
        self.binance = Binance.Binance()

    def cal_average(self, coin, interval, from_time):
        value = 0
        datas = self.binance.get_kline(coin, interval)
        if not isinstance(datas, list):
            return 0

        for data in datas:
            value += float(data[4])
        value = value / len(datas)
        return value

    def get_data(self):
        return {"BTCUSDT":self.BTCUSDT, "ETHUSDT":self.ETHUSDT, "BCHUSDT":self.BCHUSDT, "XRPUSDT":self.XRPUSDT}


    def run(self):
        while True:
            self.BTCUSDT["1"] = self.cal_average("BTCUSDT", "1d", 43200)
            time.sleep(2)
            self.BTCUSDT["5"] = self.cal_average("BTCUSDT", "5m", 150)
            time.sleep(2)
            self.BTCUSDT["30"] = self.cal_average("BTCUSDT", "30m", 900)
            time.sleep(2)
            self.BTCUSDT["60"] = self.cal_average("BTCUSDT", "1h", 1800)
            time.sleep(2)

            self.ETHUSDT["1"] = self.cal_average("ETHUSDT", "1d", 43200)
            time.sleep(2)
            self.ETHUSDT["5"] = self.cal_average("ETHUSDT", "5m", 150)
            time.sleep(2)
            self.ETHUSDT["30"] = self.cal_average("ETHUSDT", "30m", 900)
            time.sleep(2)
            self.ETHUSDT["60"] = self.cal_average("ETHUSDT", "1h", 1800)
            time.sleep(2)


            self.BCHUSDT["1"] = self.cal_average("BCHUSDT", "1d", 43200)
            time.sleep(2)
            self.BCHUSDT["5"] = self.cal_average("BCHUSDT", "5m", 150)
            time.sleep(2)
            self.BCHUSDT["30"] = self.cal_average("BCHUSDT", "30m", 900)
            time.sleep(2)
            self.BCHUSDT["60"] = self.cal_average("BCHUSDT", "1h", 1800)
            time.sleep(2)


            self.XRPUSDT["1"] = self.cal_average("XRPUSDT", "1d", 43200)
            time.sleep(2)
            self.XRPUSDT["5"] = self.cal_average("XRPUSDT", "5", 150)
            time.sleep(2)
            self.XRPUSDT["30"] = self.cal_average("XRPUSDT", "30m", 900)
            time.sleep(2)
            self.XRPUSDT["60"] = self.cal_average("XRPUSDT", "1h", 1800)
            time.sleep(2)

            time.sleep(20)


if __name__ == "__main__":
    kline = KLine()
    kline.start()


