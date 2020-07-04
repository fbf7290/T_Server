import time


class AlarmDataManager:

    def __init__(self):
        self.alarm_datas = {}
        self.alarm_kind = set(['BTCUSD',])



    def append_alarm(self, kind, data):
        if not kind in self.alarm_kind:
            return False
        self.alarm_datas[kind] = AlarmData(data)
        return True

    def get_alarm(self, kind):

        alarm = self.alarm_datas.get(kind)

        if alarm == None:
            print("alarm None")
            return None

        if alarm.valid_alarm():
            print("valid")
            return alarm
        else:
            print("not valid")
            self.alarm_datas[kind] = None
            return None


class AlarmData:
    def __init__(self, data=None):
        self.created_time = int(time.time())
        self.valid_time = 20         # alert 온지 valid_time 후면 alert 삭제
        self.data = data

    def valid_alarm(self):
        if int(time.time()) - self.created_time > self.valid_time:
            return False
        else:
            return True

    def get_data(self):
        return self.data

    def get_timestamp(self):
        return self.created_time
