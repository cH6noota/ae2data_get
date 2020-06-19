import pandas as pd
import datetime

csv_path = "/home/pi/Pydir/sensor_data/data.csv"
def func_write(temp,hum):
        #read data
        data=pd.read_csv(csv_path)
        #now time  get
        dt_now = datetime.datetime.now()
        dt_now = dt_now.strftime('%Y-%m-%d-%H-%M-%S')
        #create new line
        new_data = pd.Series([dt_now, temp, hum], index=data.columns)
        #append
        data=data.append(new_data,ignore_index=True)
        #write data
        data.to_csv(csv_path,index=False)

