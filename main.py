import pandas as pd
from temp import get_temp
from writer import func_write
import time
import os
import pyaudio
import numpy as np
import threading
import subprocess
from datetime import datetime
from python_tsl2591 import tsl2591

max_data=[]
lux_data=[]

CHUNK=1024*2 # マイクによって変わる。上手くいかない場合色々試してください
RATE=48000 # 事前に確認したサンプリング周波数
save_name="/home/pi/Desktop/user_env_data.csv"

if not os.path.exists(save_name):
        cmd = 'echo datetime,temperature,humidity,sound,lux >> '+save_name
        res = subprocess.check_call(cmd, shell=True )
p=pyaudio.PyAudio()

tsl = tsl2591()


stream=p.open(format = pyaudio.paInt16,
        channels = 1,
        rate = RATE,
        frames_per_buffer = CHUNK,
        input = True,
        output = True)

def audio_trans(input):
    frames=(np.frombuffer(input,dtype="int16"))
    max_data.append(max(frames))
    return

def sendlog(): # 定期的に呼び出される
    global max_data
    global lux_data
    if len(max_data) != 0: # 初回実行時だけ無視
        mic_ave=int(sum(max_data)/len(max_data)) #10秒間のマイク受信音量の平均値を出す
        max_data=[]
        now = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        temp,hum = get_temp()
        lux = tsl.get_current()["lux"]
        cmd = 'echo {},{},{},{},{}>> {}'.format( now,temp,hum,mic_ave,lux,save_name)
        res = subprocess.check_call(cmd, shell=True )
        print ('datetime:{} temperature:{} humidity:{} sound:{} lux:{}'.format( now,temp,hum,mic_ave,lux ) )
      
    t=threading.Timer(10,sendlog) #10秒ごとにsendlogを実行
    t.start()

t=threading.Thread(target=sendlog)

t.start()

print ("mic on")

while stream.is_active():
    input = stream.read(CHUNK)
    input = audio_trans(input)

stream.stop_stream()
stream.close()
p.terminate()

print ("Stop Streaming")


