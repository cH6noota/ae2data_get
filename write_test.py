import pandas as pd

csv_path = "/home/pi/Pydir/sensor_data/data.csv"

data=pd.read_csv(csv_path)
last_index = len(data)

#data.loc[last_index] = [2, 3, 4]
new_data = pd.Series([3, 'Hoge', 1], index=data.columns)

data=data.append(new_data,ignore_index=True)
print(data)
data.to_csv(csv_path,index=False)

