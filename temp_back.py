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
        print( result.temperature )
        return result.temperature,result.humidity

if __name__ == '__main__':
    try:
        while True:
            #温湿度データ取得
            temperature,humidity = get_temp()

            #画面出力
            if temperature == 0:
                print("No data")
                continue
            print("Temperature = ",temperature,"C"," Humidity = ",humidity,"%")

            #指定された秒数スリープ
            time.sleep(1)

    except:
        print("Error")
        pass
