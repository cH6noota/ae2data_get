import os
import pyaudio
import numpy as np
import threading
import subprocess
from datetime import datetime
max_data=[]
CHUNK=1024*2 # マイクによって変わる。上手くいかない場合色々試してください
RATE=48000 # 事前に確認したサンプリング周波数
save_name="sound.csv"

if not os.path.exists(save_name): 
        cmd = 'echo datetime,max_avarage >> '+save_name
        res = subprocess.check_call(cmd, shell=True ) 
p=pyaudio.PyAudio()



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
    if len(max_data) != 0: # 初回実行時だけ無視
        mic_ave=int(sum(max_data)/len(max_data)) #10秒間のマイク受信音量の平均値を出す
        max_data=[]
        now = datetime.now().strftime("%Y-%m-%dT%H-%M-%S,")
        cmd = 'echo '+now+str(mic_ave)+' >> '+save_name
        res = subprocess.check_call(cmd, shell=True )
        #print("スレッドの数: " + str(threading.activeCount())+threading.currentThread().getName()) #Thredingでプロセスが乱立しないかチェック用
        ## fluentdに最大音量値を渡す
        #json = '{'+'\"mic_max\":{0}'.format(mic_ave)+'}'
        #cmd = "echo '" + json + "' |  fluent-cat log.hoge"
        print ("mic_max{}".format(mic_ave) )
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
