# coding: UTF-8
# RaspberryPiでDHT11センサーから温湿度データを取得
#https://qiita.com/mahko2/items/6f3755c40d130ffa5136
import time
from DHT11_Python import dht11
import RPi.GPIO as GPIO

#定義
#GPIO 14 as DHT11 data pin
Temp_sensor=14

#温湿度データ取得
def get_temp():

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    instance = dht11.DHT11(pin=Temp_sensor)

    while True:
        #データ取得
        result = instance.read()
        return result.temperature,result.humidity

