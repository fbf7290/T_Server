from flask import Flask, request,jsonify
import sys
import json
import threading
from AlarmData import *
import os, sys, Logging, queue
import KLine
import KLineBinance
import datetime

# host = "localhost"
host ="0.0.0.0"
port = 80
app = Flask(__name__)
app.secret_key = "secret"

alarm_manager = AlarmDataManager()

alarm_manager_binance = AlarmDataManager()

log_queue = queue.Queue(-1)
logger = Logging.Logger(log_queue)
logger.start()

kline = KLine.KLine()
kline.start()

kline_binance = KLineBinance.KLine()
kline_binance.start()

alarm_data = []
alarm_data_binance = []





@app.route('/tradingview/alarm/binance', methods=['POST'])
def tradingview_alarm_binance():
    global alarm_data_binance

    data = request.get_json()

    now = datetime.datetime.now().timestamp()
    data['timestamp'] = now
    alarm_data_binance = [data] + alarm_data_binance

    # 1분 이상된 알람 삭제
    for index, data in enumerate(alarm_data_binance):
        if now-60>data['timestamp']:
            alarm_data_binance = alarm_data_binance[:index]

    kind = data['kind']
    data = data['data']

    alarm_manager.append_alarm(kind, data)

    return " "


@app.route('/alarm/binance')
def get_alarm_binance():
    global alarm_data_binance

    now = datetime.datetime.now().timestamp()

    for index, data in enumerate(alarm_data_binance):
        if now-60>data['timestamp']:
            alarm_data_binance = alarm_data_binance[:index]

    return json.dumps(alarm_data_binance)



@app.route('/delete/binance')
def test_delete_alarm_binance():
    global alarm_data_binance
    alarm_data_binance = []
    return " "




@app.route('/tradingview/alarm', methods=['POST'])
def tradingview_alarm():
    global alarm_data

    data = request.get_json()
    print(data)
    now = datetime.datetime.now().timestamp()
    data['timestamp'] = now
    alarm_data = [data] + alarm_data

    # 1분 이상된 알람 삭제
    for index, data in enumerate(alarm_data):
        if now-60>data['timestamp']:
            alarm_data = alarm_data[:index]

    #kind = data['kind']
    #data = data['data']

    #alarm_manager.append_alarm(kind, data)

    return " "

@app.route('/alarm')
def get_alarm():
    global alarm_data

    now = datetime.datetime.now().timestamp()

    for index, data in enumerate(alarm_data):
        if now-60>data['timestamp']:
            alarm_data = alarm_data[:index]

    return json.dumps(alarm_data)



@app.route('/delete')
def test_delete_alarm():
    global alarm_data
    alarm_data = []
    return " "


@app.route('/alarm/<kind>')
def get_alarm_by_kind(kind):
    alarm = alarm_manager.get_alarm(kind)
    if alarm == None:
        result = {"result":False}
    else:
        result = {"result":True, "timestamp":alarm.get_timestamp(), "data":alarm.get_data()}
    return json.dumps(result)


@app.route('/kline')
def get_kline():
    data = kline.get_data()
    return json.dumps(data)

@app.route('/kline/binance')
def get_kline_binance():
    data = kline_binance.get_data()
    return json.dumps(data)


@app.route('/heartbeat')
def heartbeat():
    return " "

if __name__ == "__main__":
    app.run(host,port)